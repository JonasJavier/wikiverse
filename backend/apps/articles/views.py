"""The encyclopedia API.

Three things in here are load-bearing and easy to break by "simplifying":

1. **Every list endpoint is a fixed number of queries.** The querysets come from
   :mod:`apps.articles.querysets`, which already carries the right
   ``select_related``/``defer``; a serializer field that reaches past them turns
   one query into one per row. ``is_current`` on a change row is the sharp case:
   it is a single correlated ``Subquery`` annotated on the feed, never a lookup
   per row.
2. **Writes are one transaction.** Saving the article, snapshotting the
   :class:`~apps.articles.models.Revision`, rebuilding the article's
   :class:`~apps.articles.models.ArticleLink` rows and refreshing the counters
   all commit together, because a half-written edit leaves "what links here"
   lying about the encyclopedia.
3. **PostgreSQL-only paths are chosen at call time.** ``is_postgres()`` is a
   function, not a module constant; the test suite runs on SQLite and production
   runs on PostgreSQL from the same artefact.
"""

from __future__ import annotations

import hashlib
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.db import transaction
from django.db.models import (
    BooleanField,
    Count,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    QuerySet,
    Subquery,
    Sum,
    Value,
)
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, NotFound, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView

from apps.articles.diff import PAYLOAD_VERSION, diff_revisions
from apps.articles.querysets import is_postgres
from apps.articles.search import (
    SUGGEST_MAX_TERM_LENGTH,
    did_you_mean,
    headline,
    normalize_ordering,
    safe_term,
    search_articles,
)
from apps.articles.search import suggest as suggest_titles
from apps.common.seo import spa_url
from apps.common.throttling import (
    DiffThrottle,
    PreviewThrottle,
    SearchThrottle,
    SuggestThrottle,
    WriteThrottle,
)

from .filters import ArticleFilter, SearchFilter
from .models import (
    Article,
    ArticleLink,
    Category,
    MainPageBlock,
    Redirect,
    Revision,
    TalkMessage,
    TalkThread,
    Watch,
)
from .permissions import (
    CanEditArticle,
    CanPostToTalk,
    IsMessageAuthorOrStaff,
    IsThreadOwnerOrStaff,
)
from .serializers import (
    ArticleDetailSerializer,
    ArticleInfoSerializer,
    ArticleListSerializer,
    ArticleStubSerializer,
    ArticleWriteSerializer,
    BacklinkSerializer,
    CategorySerializer,
    ChangeFeedSerializer,
    ChangeRowSerializer,
    DiffSerializer,
    MainPageSerializer,
    OnThisDaySerializer,
    PreviewSerializer,
    RevisionDetailSerializer,
    RevisionSerializer,
    SearchResponseSerializer,
    SearchResultSerializer,
    SiteStatsSerializer,
    SuggestionSerializer,
    TalkMessageSerializer,
    TalkMessageWriteSerializer,
    TalkThreadCreateSerializer,
    TalkThreadDetailSerializer,
    TalkThreadSerializer,
    TalkThreadUpdateSerializer,
    WantedPageSerializer,
    WatchSerializer,
)

# --------------------------------------------------------------------------- #
# Caching keys
# --------------------------------------------------------------------------- #
#: Bumped on every content write; every derived cache key embeds it, so
#: invalidation is one ``incr`` instead of a list of keys to remember.
STATS_EPOCH_KEY = "stats_epoch"
STATS_CACHE_TTL = 60 * 5
MAIN_PAGE_CACHE_TTL = 60 * 5
#: How long one identity's view of one article stops counting again.
VIEW_DEDUPE_TTL = 60 * 30

#: Legacy key name, kept because an existing test clears it by name.
STATS_CACHE_KEY = "site_stats"


def stats_epoch() -> int:
    """Current cache generation for everything derived from article content."""
    return cache.get_or_set(STATS_EPOCH_KEY, 1, None) or 1


def bump_stats_epoch() -> None:
    """Invalidate every derived cache in one write."""
    try:
        cache.incr(STATS_EPOCH_KEY)
    except ValueError:
        # The key expired or was never set; the next reader seeds it.
        cache.set(STATS_EPOCH_KEY, stats_epoch() + 1, None)
    cache.delete(STATS_CACHE_KEY)


def stats_cache_key() -> str:
    return f"site_stats:v2:{stats_epoch()}"


def main_page_cache_key() -> str:
    return f"main_page:v1:{stats_epoch()}"


# --------------------------------------------------------------------------- #
# Pagination (DECISIONS §10 — these numbers are the contract)
# --------------------------------------------------------------------------- #
class ArticlePagination(PageNumberPagination):
    """``/api/articles/`` and ``/api/search/``."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class RevisionPagination(PageNumberPagination):
    """``/api/articles/{slug}/revisions/`` — history is read in long runs."""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


class FeedPagination(PageNumberPagination):
    """``/api/watchlist/``, ``/api/users/{u}/contributions/``, category listings."""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def _int_param(raw: str | None) -> int | None:
    """An integer query parameter, or ``None`` when absent or unparseable.

    Returning ``None`` rather than raising keeps a hand-edited URL a 400 from the
    view instead of a 500 from ``get_object_or_404(pk="abc")``.
    """
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _bounded(value: int | None, default: int, *, low: int = 1, high: int = 100) -> int:
    if value is None:
        return default
    return max(low, min(value, high))


def _parse_since(request) -> Any:
    """``?since=<iso>`` or ``?days=N``, whichever the client sent."""
    raw = request.query_params.get("since")
    if raw:
        parsed = parse_datetime(raw)
        if parsed is not None:
            return parsed
    days = _int_param(request.query_params.get("days"))
    if days is not None:
        return timezone.now() - timedelta(days=_bounded(days, 7, low=1, high=365))
    return None


def _flag_off(request, name: str) -> bool:
    """``?minor=0`` / ``?bots=0`` — present and falsey means "hide these"."""
    raw = request.query_params.get(name)
    return raw is not None and raw.strip().lower() in {"0", "false", "no", "off"}


def latest_revision_subquery() -> Subquery:
    """Each article's newest revision id, correlated to the outer row.

    One subquery in the feed's own SQL is what makes ``is_current`` free; a
    ``revision.article.revisions.first()`` per row would be the N+1 that
    critique #22 warns about.
    """
    newest = (
        Revision.objects.filter(article_id=OuterRef("article_id"))
        .order_by("-created_at", "-id")
        .values("id")[:1]
    )
    return Subquery(newest)


def visible_talk_messages(user) -> QuerySet:
    """Non-deleted talk messages on articles ``user`` may read."""
    qs = (
        TalkMessage.objects.filter(is_deleted=False)
        .select_related("author", "thread", "thread__article")
        .defer("thread__article__content", "thread__article__infobox")
        .order_by("-created_at", "-id")
    )
    if user is not None and getattr(user, "is_staff", False):
        return qs
    base = Q(thread__article__is_published=True, thread__article__is_deleted=False)
    if user is not None and getattr(user, "is_authenticated", False):
        base |= Q(thread__article__author=user, thread__article__is_deleted=False)
    return qs.filter(base)


def thread_detail_queryset() -> QuerySet:
    """One talk thread with its messages, in three queries.

    The ``Prefetch`` carries its own ``select_related("author")``: without it the
    byline on every message is a separate query, which is the N+1 a threaded
    discussion makes most visible.
    """
    return TalkThread.objects.select_related(
        "article", "article__category", "created_by"
    ).prefetch_related(
        Prefetch(
            "messages",
            queryset=TalkMessage.objects.select_related("author").order_by("created_at", "id"),
        )
    )


def row_from_revision(revision: Revision) -> dict[str, Any]:
    """Map a revision onto the normative change row (DECISIONS §4)."""
    latest_id = getattr(revision, "latest_revision_id", None)
    return {
        "kind": "edit",
        "id": revision.id,
        "parent_id": revision.parent_id,
        "timestamp": revision.created_at,
        "article": {"slug": revision.article.slug, "title": revision.article.title},
        "user": revision.editor,
        "comment": revision.comment,
        "byte_size": revision.byte_size,
        "byte_delta": revision.byte_delta,
        "is_minor": revision.is_minor,
        "is_page_creation": revision.is_page_creation,
        "is_bot": revision.is_bot,
        "is_current": latest_id is not None and latest_id == revision.id,
        "tags": list(revision.tags or []),
        "thread": None,
    }


def row_from_message(message: TalkMessage) -> dict[str, Any]:
    """Map a talk message onto the same row shape.

    ``byte_size``/``byte_delta`` stay ``null`` — a talk post has no article byte
    count, and inventing one would put a fake ``+412`` in Recent changes.
    """
    article = message.thread.article
    return {
        "kind": "talk",
        "id": message.id,
        "parent_id": message.parent_id,
        "timestamp": message.created_at,
        "article": {"slug": article.slug, "title": article.title},
        "user": message.author,
        "comment": message.thread.title,
        "byte_size": None,
        "byte_delta": None,
        "is_minor": False,
        "is_page_creation": message.parent_id is None,
        "is_bot": bool(getattr(message.author, "is_bot", False)),
        "is_current": False,
        "tags": [],
        "thread": {"id": message.thread_id, "title": message.thread.title},
    }


def site_stats() -> dict[str, int]:
    """Aggregate counts, cached under the content epoch."""
    data = cache.get(stats_cache_key())
    if data is not None:
        return data
    published = Article.objects.published()
    totals = published.aggregate(views=Sum("view_count"), words=Sum("word_count"))
    data = {
        "articles": published.count(),
        "categories": Category.objects.count(),
        # ``author__isnull=True`` rows are legacy imports with no account; they
        # are not contributors and counting them inflates the number by one.
        "contributors": published.exclude(author__isnull=True).values("author").distinct().count(),
        "total_views": totals["views"] or 0,
        "words": totals["words"] or 0,
        "stubs": published.filter(is_stub=True).count(),
        "revisions": Revision.objects.count(),
        "talk_messages": TalkMessage.objects.filter(is_deleted=False).count(),
    }
    cache.set(stats_cache_key(), data, STATS_CACHE_TTL)
    return data


# --------------------------------------------------------------------------- #
# Categories
# --------------------------------------------------------------------------- #
@extend_schema(tags=["categories"])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Browse the category tree."""

    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    pagination_class = None
    filter_backends: list = []

    def get_queryset(self):
        return (
            Category.objects.select_related("parent")
            .annotate(
                article_count=Count(
                    "articles",
                    filter=Q(articles__is_published=True, articles__is_deleted=False),
                    distinct=True,
                )
            )
            .order_by("order", "name")
        )

    @extend_schema(
        responses=ArticleListSerializer(many=True),
        parameters=[OpenApiParameter("page", int), OpenApiParameter("page_size", int)],
    )
    @action(detail=True, methods=["get"], pagination_class=FeedPagination)
    def articles(self, request, slug=None):
        """Articles in this category, primary or additional (page size 50)."""
        category = self.get_object()
        queryset = (
            Article.objects.visible(request.user)
            .filter(Q(category=category) | Q(extra_categories=category))
            .distinct()
            .with_card_fields()
            .defer("infobox", "search_vector")
            .order_by("title")
        )
        page = self.paginate_queryset(queryset)
        serializer = ArticleListSerializer(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


# --------------------------------------------------------------------------- #
# Articles
# --------------------------------------------------------------------------- #
@extend_schema(tags=["articles"])
@extend_schema_view(
    list=extend_schema(responses=ArticleListSerializer(many=True)),
    create=extend_schema(request=ArticleWriteSerializer, responses=ArticleDetailSerializer),
    retrieve=extend_schema(responses=ArticleDetailSerializer),
    update=extend_schema(
        request=ArticleWriteSerializer,
        responses=ArticleDetailSerializer,
        description=(
            "PUT is a **partial replace**: every model-derived field is optional, so a "
            "PUT that omits `summary` keeps the stored value. Use PATCH when you mean "
            "partial; they behave identically, including the edit `comment`."
        ),
    ),
    partial_update=extend_schema(request=ArticleWriteSerializer, responses=ArticleDetailSerializer),
    destroy=extend_schema(
        description="Soft delete: the row and its revision history are kept and staff can restore it."
    ),
)
class ArticleViewSet(viewsets.ModelViewSet):
    """Articles, their history, talk pages, diffs and backlinks."""

    permission_classes = [CanEditArticle]
    lookup_field = "slug"
    filterset_class = ArticleFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["updated_at", "created_at", "view_count", "title", "word_count"]
    #: ``-id`` breaks ties so page 2 cannot repeat a row from page 1.
    ordering = ["-updated_at", "-id"]
    pagination_class = ArticlePagination
    # No bare HEAD on the detail route: a HEAD storm would otherwise inflate
    # view counts through a path that renders nothing.
    http_method_names = ["get", "post", "put", "patch", "delete", "options"]

    #: Unsafe actions billed to the ``write`` throttle scope.
    WRITE_ACTIONS = frozenset(
        {
            "create",
            "update",
            "partial_update",
            "destroy",
            "restore",
            "revert",
            "talk",
            "talk_messages",
        }
    )

    # ---- querysets ------------------------------------------------------- #
    def get_queryset(self):
        if self.action == "restore":
            # Explicitly unfiltered: a soft-deleted article is invisible to
            # every other action, so restore could never find its own target
            # through the visibility queryset (critique #25).
            return Article.objects.all()
        if self.action in {"retrieve", "update", "partial_update", "revert"}:
            return self._detail_queryset()
        if self.action == "list":
            return (
                Article.objects.visible(self.request.user)
                .with_card_fields()
                .defer("infobox", "search_vector")
            )
        return Article.objects.visible(self.request.user)

    def _detail_queryset(self):
        user = self.request.user
        queryset = (
            Article.objects.visible(user)
            .with_detail_fields()
            .annotate(talk_thread_total=Count("talk_threads", distinct=True))
        )
        if user is not None and user.is_authenticated:
            queryset = queryset.annotate(
                is_watched=Exists(Watch.objects.filter(user=user, article=OuterRef("pk")))
            )
        else:
            queryset = queryset.annotate(is_watched=Value(False, output_field=BooleanField()))
        return queryset

    def filter_queryset(self, queryset):
        """Filters and ordering apply to the collection only.

        ``?search=`` sets its own relevance ordering, so ``OrderingFilter``'s
        default (``-updated_at``) is skipped unless the client asked for an
        explicit ``?ordering=``. Otherwise every search would come back in
        reverse-chronological order and look broken.
        """
        if self.action != "list":
            return queryset
        params = self.request.query_params
        skip_ordering = bool(params.get("search")) and not params.get("ordering")
        for backend in self.filter_backends:
            if skip_ordering and backend is OrderingFilter:
                continue
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_object(self):
        """Resolve the slug, following a :class:`Redirect` on a read.

        Resolution is a **200 with `redirected_from` set**, not a 301: the reader
        stays on the URL they clicked, exactly like ``/wiki/JS`` on Wikipedia,
        and the client shows the "Redirected from JS" line.
        """
        try:
            return super().get_object()
        except Http404:
            if self.action not in {"retrieve", "preview"}:
                raise
            article = self._follow_redirect(self.kwargs.get(self.lookup_field, ""))
            if article is None:
                raise
            return article

    def _follow_redirect(self, slug: str) -> Article | None:
        redirect = (
            Redirect.objects.filter(from_slug=slug)
            .only("from_slug", "from_title", "target")
            .first()
        )
        if redirect is None:
            return None
        article = self.get_queryset().filter(pk=redirect.target_id).first()
        if article is None:
            return None
        article.redirected_from_title = redirect.from_title
        return article

    # ---- serializers / permissions / throttles --------------------------- #
    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        if self.action in {"create", "update", "partial_update"}:
            return ArticleWriteSerializer
        return ArticleDetailSerializer

    def get_permissions(self):
        if self.action == "restore":
            return [permissions.IsAdminUser()]
        if self.action == "watch":
            return [permissions.IsAuthenticated()]
        if self.action in {"talk", "talk_messages"}:
            return [CanPostToTalk()]
        return super().get_permissions()

    def get_throttles(self):
        if self.action == "diff":
            return [DiffThrottle()]
        if self.action == "preview":
            return [PreviewThrottle()]
        if (
            self.action in self.WRITE_ACTIONS
            and self.request.method not in permissions.SAFE_METHODS
        ):
            return [WriteThrottle()]
        return super().get_throttles()

    # ---- reads ----------------------------------------------------------- #
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self._count_view(instance)
        instance.latest_revision_row = (
            instance.revisions.select_related("editor").order_by("-created_at", "-id").first()
        )
        return Response(self.get_serializer(instance).data)

    def _count_view(self, article: Article) -> None:
        """One view per identity per 30 minutes.

        Two separate reasons for the guard, both measured on real wikis: a
        crawler pass would otherwise make every article look popular, and a
        reader scrolling back and forth between an article and its talk page
        would inflate its own count. ``cache.add`` is the atomic test-and-set, so
        two concurrent requests cannot both win.

        The increment is an ``F()`` ``UPDATE``, never ``instance.save()``:
        ``updated_at`` is ``auto_now``, so a save here would reorder the entire
        encyclopedia by "last edited" every time somebody read a page.
        """
        ident = BaseThrottle().get_ident(self.request) or "anonymous"
        if not cache.add(f"viewed:{article.pk}:{ident}", 1, VIEW_DEDUPE_TTL):
            return
        Article.objects.filter(pk=article.pk).update(view_count=F("view_count") + 1)
        article.view_count = (article.view_count or 0) + 1

    @extend_schema(responses=ArticleDetailSerializer)
    @action(detail=False, methods=["get"])
    def random(self, request):
        """One random readable article."""
        article = Article.objects.visible(request.user).with_detail_fields().order_by("?").first()
        if article is None:
            raise NotFound("No articles yet.")
        return Response(
            ArticleDetailSerializer(article, context=self.get_serializer_context()).data
        )

    @extend_schema(
        responses=ArticleListSerializer(many=True),
        parameters=[OpenApiParameter("limit", int, description="1–50, default 10")],
    )
    @action(detail=False, methods=["get"])
    def popular(self, request):
        """Most-viewed readable articles."""
        limit = _bounded(_int_param(request.query_params.get("limit")), 10, high=50)
        queryset = (
            Article.objects.visible(request.user)
            .with_card_fields()
            .defer("infobox", "search_vector")
            .order_by("-view_count", "-updated_at")[:limit]
        )
        return Response(
            ArticleListSerializer(queryset, many=True, context=self.get_serializer_context()).data
        )

    @extend_schema(responses=SiteStatsSerializer)
    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def stats(self, request):
        """Aggregate site statistics (cached under the content epoch)."""
        return Response(SiteStatsSerializer(site_stats()).data)

    @extend_schema(
        operation_id="articles_revisions_list",
        responses=RevisionSerializer(many=True),
        parameters=[OpenApiParameter("page", int), OpenApiParameter("page_size", int)],
    )
    @action(detail=True, methods=["get"], pagination_class=RevisionPagination)
    def revisions(self, request, slug=None):
        """Edit history, newest first, page size 50."""
        article = self.get_object()
        queryset = (
            article.revisions.select_related("editor")
            .defer("content", "apparatus")
            .order_by("-created_at", "-id")
        )
        page = self.paginate_queryset(queryset)
        serializer = RevisionSerializer(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)

    @extend_schema(operation_id="articles_revisions_retrieve", responses=RevisionDetailSerializer)
    @action(
        detail=True,
        methods=["get"],
        url_path="revisions/(?P<revision_id>[0-9]+)",
        url_name="revision-detail",
    )
    def revision_detail(self, request, slug=None, revision_id=None):
        """One revision in full — the "old version of this page" read."""
        article = self.get_object()
        revision = get_object_or_404(article.revisions.select_related("editor"), pk=revision_id)
        return Response(
            RevisionDetailSerializer(revision, context=self.get_serializer_context()).data
        )

    @extend_schema(
        responses=DiffSerializer,
        parameters=[
            OpenApiParameter(
                "from", int, description="Revision id, or 0 for the page-creation diff."
            ),
            OpenApiParameter("to", int, description="Revision id; defaults to the latest."),
        ],
    )
    @action(detail=True, methods=["get"])
    def diff(self, request, slug=None):
        """Two-stage line/word diff between two revisions of this article."""
        article = self.get_object()
        revisions = article.revisions.select_related("editor")

        raw_to = request.query_params.get("to")
        raw_from = request.query_params.get("from")
        if raw_to not in (None, "") and _int_param(raw_to) is None:
            raise ValidationError({"to": "Must be a revision id."})
        if raw_from not in (None, "") and _int_param(raw_from) is None:
            raise ValidationError({"from": "Must be a revision id, or 0."})

        to_id = _int_param(raw_to)
        if to_id is None:
            to_revision = revisions.order_by("-created_at", "-id").first()
            if to_revision is None:
                raise NotFound("This article has no revisions yet.")
        else:
            to_revision = get_object_or_404(revisions, pk=to_id)

        older = revisions.filter(
            Q(created_at__lt=to_revision.created_at)
            | Q(created_at=to_revision.created_at, id__lt=to_revision.id)
        ).order_by("-created_at", "-id")
        newer = revisions.filter(
            Q(created_at__gt=to_revision.created_at)
            | Q(created_at=to_revision.created_at, id__gt=to_revision.id)
        ).order_by("created_at", "id")

        from_id = _int_param(raw_from)
        if raw_from in (None, ""):
            from_revision = (
                revisions.filter(pk=to_revision.parent_id).first()
                if to_revision.parent_id
                else older.first()
            )
        elif from_id == 0:
            from_revision = None
        else:
            from_revision = get_object_or_404(revisions, pk=from_id)

        prev_id = older.values_list("id", flat=True).first()
        next_id = newer.values_list("id", flat=True).first()

        key = f"diff:v{PAYLOAD_VERSION}:{from_revision.id if from_revision else 0}:{to_revision.id}"
        payload = cache.get(key) if next_id is not None else None
        if payload is None:
            payload = diff_revisions(
                from_revision.content if from_revision else "", to_revision.content
            )
            payload["article"] = ArticleStubSerializer(article).data
            payload["from_revision"] = self._diff_end(from_revision)
            payload["to_revision"] = self._diff_end(to_revision)
            payload["prev_id"] = prev_id
            payload["next_id"] = next_id
            payload["title_changed"] = bool(
                from_revision and from_revision.title != to_revision.title
            )
            payload["summary_changed"] = bool(
                from_revision and from_revision.summary != to_revision.summary
            )
            if next_id is not None:
                cache.set(key, payload, None)

        response = Response(payload)
        # A diff between two historical revisions can never change, so it is
        # immutable. A diff whose right-hand side is the *current* revision can:
        # ``next_id`` flips from null to a real id the moment somebody edits.
        response.headers["Cache-Control"] = (
            "public, max-age=31536000, immutable" if next_id is not None else "public, max-age=60"
        )
        return response

    @staticmethod
    def _diff_end(revision: Revision | None) -> dict[str, Any]:
        if revision is None:
            return {
                "id": None,
                "editor": None,
                "comment": "",
                "byte_size": None,
                "is_minor": False,
                "created_at": None,
            }
        editor = revision.editor
        return {
            "id": revision.id,
            "editor": (
                None
                if editor is None
                else {
                    "id": editor.id,
                    "username": editor.username,
                    "avatar": editor.avatar.url if editor.avatar else None,
                }
            ),
            "comment": revision.comment,
            "byte_size": revision.byte_size,
            "is_minor": revision.is_minor,
            "created_at": revision.created_at,
        }

    @extend_schema(responses=PreviewSerializer)
    @action(detail=True, methods=["get"])
    def preview(self, request, slug=None):
        """Hover-card payload: the gloss plus a 525-character plain extract."""
        article = self.get_object()
        response = Response(PreviewSerializer(article, context=self.get_serializer_context()).data)
        response.headers["Cache-Control"] = "public, max-age=300"
        return response

    @extend_schema(
        responses=BacklinkSerializer(many=True),
        parameters=[OpenApiParameter("page", int), OpenApiParameter("page_size", int)],
    )
    @action(detail=True, methods=["get"], pagination_class=FeedPagination)
    def backlinks(self, request, slug=None):
        """What links here."""
        article = self.get_object()
        visible = Article.objects.visible(request.user).values("pk")
        queryset = (
            ArticleLink.objects.filter(to_article=article, from_article__in=Subquery(visible))
            .exclude(from_article=article)
            .select_related("from_article", "from_article__category")
            .defer("from_article__content", "from_article__infobox")
            .order_by("from_article__title", "id")
        )
        page = self.paginate_queryset(queryset)
        rows = [{"source": link.from_article, "occurrences": link.occurrences} for link in page]
        return self.get_paginated_response(
            BacklinkSerializer(rows, many=True, context=self.get_serializer_context()).data
        )

    @extend_schema(responses=ArticleInfoSerializer)
    @action(detail=True, methods=["get"])
    def info(self, request, slug=None):
        """Page information (DECISIONS §17)."""
        article = self.get_object()
        links = article.outgoing_links.aggregate(
            total=Count("id"),
            red=Count("id", filter=Q(to_article__isnull=True)),
        )
        payload = {
            "slug": article.slug,
            "title": article.title,
            "byte_size": article.byte_size,
            "word_count": article.word_count,
            "read_time": article.read_time,
            "revision_count": article.revision_total,
            "contributor_count": article.contributor_total,
            "watcher_count": article.watcher_total,
            "backlink_count": article.backlink_total,
            "redirect_count": article.redirects.count(),
            "talk_thread_count": article.talk_threads.count(),
            "reference_count": article.references.count(),
            "outgoing_link_count": links["total"] or 0,
            "red_link_count": links["red"] or 0,
            "view_count": article.view_count,
            "page_type": article.page_type,
            "protection": article.protection,
            "is_stub": article.is_stub,
            "is_published": article.is_published,
            "author": article.author,
            "last_editor": article.last_editor,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
        }
        return Response(ArticleInfoSerializer(payload).data)

    # ---- talk ------------------------------------------------------------ #
    @extend_schema(
        methods=["GET"],
        responses=TalkThreadSerializer(many=True),
        parameters=[
            OpenApiParameter("resolved", bool),
            OpenApiParameter("page", int),
            OpenApiParameter("page_size", int),
        ],
    )
    @extend_schema(
        methods=["POST"],
        request=TalkThreadCreateSerializer,
        responses={201: TalkThreadDetailSerializer},
    )
    @action(detail=True, methods=["get", "post"], pagination_class=ArticlePagination)
    def talk(self, request, slug=None):
        """List this article's discussion threads, or open a new one."""
        article = self.get_object()
        if request.method == "POST":
            return self._create_thread(request, article)

        queryset = article.talk_threads.select_related("created_by").order_by(
            F("last_message_at").desc(nulls_last=True), "-created_at"
        )
        resolved = request.query_params.get("resolved")
        if resolved is not None:
            queryset = queryset.filter(
                is_resolved=resolved.strip().lower() in {"1", "true", "yes", "on"}
            )
        page = self.paginate_queryset(queryset)
        serializer = TalkThreadSerializer(page, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)

    def _create_thread(self, request, article: Article) -> Response:
        serializer = TalkThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data["title"]
        # ``uniq_talkthread_article_title`` would otherwise surface as an
        # IntegrityError and a 500. A duplicate title on the same talk page is a
        # user mistake, so it gets a field-level 400 that names the collision.
        if article.talk_threads.filter(title=title).exists():
            raise ValidationError({"title": "This talk page already has a thread with that title."})
        with transaction.atomic():
            thread = TalkThread.objects.create(
                article=article,
                title=title,
                created_by=request.user,
            )
            TalkMessage.objects.create(
                thread=thread, author=request.user, body=serializer.validated_data["body"], depth=0
            )
            thread.touch()
        thread = thread_detail_queryset().get(pk=thread.pk)
        return Response(
            TalkThreadDetailSerializer(thread, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(request=TalkMessageWriteSerializer, responses={201: TalkMessageSerializer})
    @action(
        detail=True,
        methods=["post"],
        url_path="talk/(?P<thread_id>[0-9]+)/messages",
        url_name="talk-messages",
    )
    def talk_messages(self, request, slug=None, thread_id=None):
        """Reply in a thread. ``parent`` threads the reply; depth is capped at 4."""
        article = self.get_object()
        thread = get_object_or_404(article.talk_threads, pk=thread_id)
        permission = CanPostToTalk()
        if not permission.allows_thread(request, thread):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise ValidationError({"detail": "This thread is locked; only staff may post to it."})

        serializer = TalkMessageWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data.get("parent")
        if parent is not None and parent.thread_id != thread.pk:
            raise ValidationError({"parent": "That message belongs to a different thread."})

        with transaction.atomic():
            message = TalkMessage.objects.create(
                thread=thread,
                parent=parent,
                author=request.user,
                body=serializer.validated_data["body"],
                # Clamped, not rejected: a reader replying to the deepest post in
                # a long thread should not get a validation error, they should
                # get a reply that renders at the maximum indent.
                depth=0 if parent is None else min(parent.depth + 1, TalkMessage.MAX_DEPTH),
            )
            thread.touch()
        return Response(
            TalkMessageSerializer(message, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )

    # ---- watching -------------------------------------------------------- #
    @extend_schema(methods=["POST"], request=None, responses={201: WatchSerializer})
    @extend_schema(methods=["DELETE"], responses={204: None})
    @action(detail=True, methods=["post", "delete"])
    def watch(self, request, slug=None):
        """Add or remove this article from the caller's watchlist. Idempotent."""
        article = self.get_object()
        if request.method == "POST":
            Watch.objects.get_or_create(user=request.user, article=article)
            article.recount()
            return Response({"watching": True}, status=status.HTTP_201_CREATED)
        Watch.objects.filter(user=request.user, article=article).delete()
        article.recount()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ---- writes ---------------------------------------------------------- #
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = self.perform_create(serializer)
        detail = self._detail_queryset().get(pk=article.pk)
        detail.latest_revision_row = (
            detail.revisions.select_related("editor").order_by("-created_at", "-id").first()
        )
        return Response(
            ArticleDetailSerializer(detail, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        article = self.perform_update(serializer)
        detail = self._detail_queryset().get(pk=article.pk)
        detail.latest_revision_row = (
            detail.revisions.select_related("editor").order_by("-created_at", "-id").first()
        )
        return Response(ArticleDetailSerializer(detail, context=self.get_serializer_context()).data)

    def perform_create(self, serializer) -> Article:
        comment, is_minor = self._edit_meta(serializer)
        with transaction.atomic():
            article = serializer.save(author=self.request.user, last_editor=self.request.user)
            self._snapshot(
                article, comment=comment or "Created the article", is_minor=is_minor, created=True
            )
            ArticleLink.rebuild_for(article)
            # A brand-new article may already be the target of red links that
            # other articles have been carrying since before it existed.
            ArticleLink.attach_target(article)
            article.recount()
        bump_stats_epoch()
        return article

    def perform_update(self, serializer) -> Article:
        instance = serializer.instance
        before = self._fingerprint(instance)
        comment, is_minor = self._edit_meta(serializer)
        with transaction.atomic():
            article = serializer.save(last_editor=self.request.user)
            if self._fingerprint(article) != before:
                self._snapshot(
                    article,
                    comment=comment or "Edited the article",
                    is_minor=is_minor,
                    created=False,
                )
                ArticleLink.rebuild_for(article)
                article.recount()
        bump_stats_epoch()
        return article

    def perform_destroy(self, instance: Article) -> None:
        """Soft delete: history and other contributors' work survive."""
        instance.soft_delete(by=self.request.user)
        bump_stats_epoch()

    @extend_schema(request=None, responses=ArticleDetailSerializer)
    @action(detail=True, methods=["post"])
    def restore(self, request, slug=None):
        """Undo a soft delete. Staff only."""
        article = self.get_object()
        article.restore()
        bump_stats_epoch()
        detail = (
            Article.objects.all()
            .with_detail_fields()
            .annotate(
                talk_thread_total=Count("talk_threads", distinct=True),
                is_watched=Value(False, output_field=BooleanField()),
            )
            .get(pk=article.pk)
        )
        return Response(ArticleDetailSerializer(detail, context=self.get_serializer_context()).data)

    @extend_schema(
        request=None,
        responses=ArticleDetailSerializer,
        parameters=[
            OpenApiParameter("revision", int, OpenApiParameter.QUERY, required=False),
        ],
        description=(
            "Restore an earlier revision's title, summary, content and infobox as a **new** "
            "revision. Nothing is deleted; the reverted-away text stays in history. Pass "
            "`revision` in the body or the query string."
        ),
    )
    @action(detail=True, methods=["post"])
    def revert(self, request, slug=None):
        """Roll an article back to an earlier revision, as a new revision."""
        article = self.get_object()
        body = request.data if hasattr(request.data, "get") else {}
        raw = body.get("revision")
        revision_id = _int_param(None if raw is None else str(raw)) or _int_param(
            request.query_params.get("revision")
        )
        if revision_id is None:
            raise ValidationError({"revision": "A revision id is required."})
        revision = get_object_or_404(article.revisions, pk=revision_id)
        comment = (body.get("comment") or "").strip()
        with transaction.atomic():
            article.title = revision.title
            article.summary = revision.summary
            article.content = revision.content
            apparatus = revision.apparatus if isinstance(revision.apparatus, dict) else {}
            if "infobox" in apparatus:
                article.infobox = apparatus["infobox"] or {}
            article.last_editor = request.user
            article.save()
            self._snapshot(
                article,
                comment=comment or f"Reverted to revision {revision.pk}",
                is_minor=False,
                created=False,
                tags=["revert"],
            )
            ArticleLink.rebuild_for(article)
            article.recount()
        bump_stats_epoch()
        detail = self._detail_queryset().get(pk=article.pk)
        return Response(ArticleDetailSerializer(detail, context=self.get_serializer_context()).data)

    # ---- revision plumbing ----------------------------------------------- #
    @staticmethod
    def _edit_meta(serializer) -> tuple[str, bool]:
        """Read ``comment``/``is_minor`` *before* the serializer strips them.

        They live in ``validated_data`` rather than on the model because they
        describe the edit, not the article; ``create()``/``update()`` pop them
        from the very dict this reads, so the order matters.
        """
        data = serializer.validated_data
        return (data.get("comment") or "").strip(), bool(data.get("is_minor"))

    @staticmethod
    def _fingerprint(article: Article) -> tuple:
        """What counts as a *content* change.

        An edit that only flips ``is_published`` or adds a watcher is not history
        worth a row, and a no-op save that minted a revision would fill the
        history page with empty diffs (survey 2.9).
        """
        return (
            article.title,
            article.summary,
            article.short_description,
            article.content,
            repr(article.infobox),
            tuple(reference.as_dict()["key"] for reference in article.references.all()),
            tuple(
                (reference.title, reference.url, reference.identifier)
                for reference in article.references.all()
            ),
        )

    def _snapshot(
        self,
        article: Article,
        *,
        comment: str,
        is_minor: bool,
        created: bool,
        tags: list[str] | None = None,
    ) -> Revision:
        """Write one history row and keep ``byte_delta`` honest.

        ``Revision.save()`` maintains ``byte_size`` but nothing maintains
        ``byte_delta``, ``parent``, ``is_page_creation`` or ``is_bot`` — this
        method owns all four. Any other code path that creates a ``Revision``
        directly (the admin inline, a fixture) writes a ``byte_delta`` of 0 and a
        null ``parent``, and Recent changes then reports "0 bytes".
        """
        editor = self.request.user
        parent = article.revisions.order_by("-created_at", "-id").first()
        revision = Revision.objects.create(
            article=article,
            parent=parent,
            editor=editor,
            title=article.title,
            summary=article.summary,
            content=article.content,
            comment=comment[:255],
            byte_delta=article.byte_size - (parent.byte_size if parent else 0),
            is_minor=is_minor,
            is_page_creation=created,
            is_bot=bool(getattr(editor, "is_bot", False)),
            tags=list(tags or []),
            apparatus={
                "references": [reference.as_dict() for reference in article.references.all()],
                "infobox": article.infobox,
                "categories": article.category_names(),
                "short_description": article.short_description,
            },
        )
        if editor is not None and getattr(editor, "is_authenticated", False):
            editor.recount_edits()
        return revision


# --------------------------------------------------------------------------- #
# Talk threads and messages (flat routes)
# --------------------------------------------------------------------------- #
@extend_schema(tags=["talk"])
@extend_schema_view(
    retrieve=extend_schema(responses=TalkThreadDetailSerializer),
    partial_update=extend_schema(
        request=TalkThreadUpdateSerializer, responses=TalkThreadDetailSerializer
    ),
)
class TalkThreadViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """``/api/talk/threads/{id}/`` — read a thread, resolve it, rename it, lock it."""

    permission_classes = [IsThreadOwnerOrStaff]
    serializer_class = TalkThreadDetailSerializer
    pagination_class = None
    filter_backends: list = []
    http_method_names = ["get", "patch", "options"]

    def get_queryset(self):
        return thread_detail_queryset().filter(
            article__in=Subquery(Article.objects.visible(self.request.user).values("pk"))
        )

    def get_throttles(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [WriteThrottle()]
        return super().get_throttles()

    def partial_update(self, request, *args, **kwargs):
        thread = self.get_object()
        serializer = TalkThreadUpdateSerializer(
            thread, data=request.data, partial=True, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        new_title = serializer.validated_data.get("title")
        if (
            new_title
            and TalkThread.objects.filter(article_id=thread.article_id, title=new_title)
            .exclude(pk=thread.pk)
            .exists()
        ):
            raise ValidationError({"title": "This talk page already has a thread with that title."})
        if "is_locked" in serializer.validated_data and not request.user.is_staff:
            # Field-level 400, not 403: the thread's creator *is* allowed to
            # change the thread, just not to lock it (same reasoning as
            # DECISIONS §15 for article protection).
            raise ValidationError({"is_locked": "Only staff may lock or unlock a thread."})
        serializer.save()
        return Response(
            TalkThreadDetailSerializer(
                self.get_queryset().get(pk=thread.pk), context=self.get_serializer_context()
            ).data
        )


@extend_schema(tags=["talk"])
@extend_schema_view(
    partial_update=extend_schema(
        request=TalkMessageWriteSerializer, responses=TalkMessageSerializer
    ),
    destroy=extend_schema(description="Soft delete: the row stays so the thread still reads."),
)
class TalkMessageViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """``/api/talk/messages/{id}/``."""

    permission_classes = [IsMessageAuthorOrStaff]
    serializer_class = TalkMessageSerializer
    pagination_class = None
    filter_backends: list = []
    http_method_names = ["patch", "delete", "options"]

    def get_queryset(self):
        return TalkMessage.objects.select_related("author", "thread", "thread__article").filter(
            thread__article__in=Subquery(Article.objects.visible(self.request.user).values("pk"))
        )

    def get_throttles(self):
        return [WriteThrottle()]

    def partial_update(self, request, *args, **kwargs):
        message = self.get_object()
        serializer = TalkMessageWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        body = serializer.validated_data.get("body")
        if body is None:
            raise ValidationError({"body": "Nothing to change."})
        message.body = body
        message.edited_at = timezone.now()
        message.save(update_fields=["body", "edited_at"])
        message.thread.touch()
        return Response(TalkMessageSerializer(message, context=self.get_serializer_context()).data)

    def perform_destroy(self, instance: TalkMessage) -> None:
        instance.soft_delete(by=self.request.user)
        instance.thread.touch()


# --------------------------------------------------------------------------- #
# Search
# --------------------------------------------------------------------------- #
@extend_schema(
    tags=["search"],
    responses=SearchResponseSerializer,
    parameters=[
        OpenApiParameter("q", str, description="The query. Blank returns the newest articles."),
        OpenApiParameter(
            "ordering",
            str,
            enum=["relevance", "newest", "oldest"],
            description="Default relevance.",
        ),
        OpenApiParameter("page", int),
        OpenApiParameter("page_size", int),
    ],
)
class SearchView(ListAPIView):
    """``GET /api/search/`` — the full results page, 20 per page."""

    serializer_class = SearchResultSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = ArticlePagination
    throttle_classes = [SearchThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SearchFilter

    @property
    def term(self) -> str:
        return safe_term(self.request.query_params.get("q"))

    def get_queryset(self):
        return (
            Article.objects.visible(self.request.user)
            .with_card_fields()
            .defer("infobox", "search_vector")
        )

    def filter_queryset(self, queryset):
        """Facets first, then ranking, then the headline annotation — in that order.

        ``ts_headline`` must be annotated last: compiling it needs a live
        PostgreSQL connection, and any annotation added after it would be
        evaluated against a queryset that already carries a
        ``compose_sql``-dependent expression.
        """
        queryset = super().filter_queryset(queryset)
        term = self.term
        queryset = search_articles(queryset, term, self.request.query_params.get("ordering"))
        if term and is_postgres():
            queryset = queryset.annotate(
                snippet=headline("content", term),
                title_snippet=headline("title", term, highlight_all=True),
            )
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        term = self.term
        response.data["query"] = term
        response.data["ordering"] = normalize_ordering(request.query_params.get("ordering"))
        # Only ever on the zero-result path: a correction shown next to results
        # reads as a bug, and it is a second query.
        response.data["did_you_mean"] = (
            did_you_mean(term, queryset=Article.objects.published())
            if term and not response.data.get("count")
            else None
        )
        return response


@extend_schema(
    tags=["search"],
    responses=SuggestionSerializer(many=True),
    parameters=[
        OpenApiParameter(
            "q", str, required=True, description="At least 2 characters; shorter returns []."
        )
    ],
)
class SuggestView(APIView):
    """``GET /api/search/suggest/`` — typeahead, hard-capped at 10 rows.

    Also serves the 404 page's "similar titles"; there is no separate endpoint
    for that (DECISIONS §2).
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [SuggestThrottle]

    def get(self, request):
        term = safe_term(request.query_params.get("q"), max_length=SUGGEST_MAX_TERM_LENGTH)
        digest = hashlib.sha256(term.casefold().encode("utf-8")).hexdigest()[:24]
        key = f"suggest:v1:{stats_epoch()}:{digest}"
        rows = cache.get(key)
        if rows is None:
            # The cap lives in ``search.suggest``; no ``limit`` parameter is
            # accepted here, so a client cannot widen it (DECISIONS §10).
            rows = suggest_titles(term)
            cache.set(key, rows, getattr(settings, "SEARCH_SUGGEST_TTL", 60))
        response = Response(SuggestionSerializer(rows, many=True).data)
        response.headers["Cache-Control"] = "public, max-age=60"
        return response


# --------------------------------------------------------------------------- #
# Change feeds
# --------------------------------------------------------------------------- #
@extend_schema(
    tags=["changes"],
    responses=ChangeFeedSerializer,
    parameters=[
        OpenApiParameter("type", str, enum=["all", "edit", "talk"], description="Default all."),
        OpenApiParameter("user", str, description="Contributor username."),
        OpenApiParameter("category", str, description="Category slug."),
        OpenApiParameter("article", str, description="Article slug."),
        OpenApiParameter("minor", str, description="minor=0 hides minor edits."),
        OpenApiParameter("bots", str, description="bots=0 hides bot edits."),
        OpenApiParameter("days", int, description="Window in days; default 7."),
        OpenApiParameter("since", str, description="ISO timestamp; overrides days."),
        OpenApiParameter("before", str, description="Cursor: the previous page's next_before."),
        OpenApiParameter("limit", int, description="1–100, default 50."),
    ],
)
class ChangesView(APIView):
    """``GET /api/changes/`` — recent changes, edits and talk posts merged.

    The envelope is a **timestamp cursor**, not a DRF paginator: Recent changes
    is an append-at-the-head feed, so page numbers shift under the reader and a
    ``COUNT(*)`` over every revision buys nothing.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = _bounded(_int_param(request.query_params.get("limit")), 50)
        kind = (request.query_params.get("type") or "all").strip().lower()
        if kind not in {"all", "edit", "talk"}:
            kind = "all"
        since = _parse_since(request)
        before = parse_datetime(request.query_params.get("before") or "") or None
        username = request.query_params.get("user") or None
        category = request.query_params.get("category") or None
        article = request.query_params.get("article") or None
        show_minor = not _flag_off(request, "minor")
        show_bots = not _flag_off(request, "bots")

        rows: list[dict[str, Any]] = []

        if kind in {"all", "edit"}:
            edits = Revision.objects.for_changes(
                user=username,
                viewer=request.user,
                category=category,
                article=article,
                since=since,
                before=before,
                minor=show_minor,
                bots=show_bots,
            ).annotate(latest_revision_id=latest_revision_subquery())
            # ``limit + 1`` from *each* side, not ``limit`` split between them:
            # a window where one kind dominates would otherwise return fewer
            # rows than asked for while still reporting has_more (critique #24).
            rows += [row_from_revision(revision) for revision in edits[: limit + 1]]

        if kind in {"all", "talk"}:
            posts = visible_talk_messages(request.user)
            if username:
                posts = posts.filter(author__username=username)
            if category:
                posts = posts.filter(thread__article__category__slug=category)
            if article:
                posts = posts.filter(thread__article__slug=article)
            if since is not None:
                posts = posts.filter(created_at__gte=since)
            if before is not None:
                posts = posts.filter(created_at__lt=before)
            if not show_bots:
                posts = posts.filter(author__is_bot=False)
            rows += [row_from_message(message) for message in posts[: limit + 1]]

        rows.sort(key=lambda row: (row["timestamp"], row["kind"], row["id"]), reverse=True)
        has_more = len(rows) > limit
        rows = rows[:limit]
        next_before = rows[-1]["timestamp"] if rows and has_more else None

        return Response(
            ChangeFeedSerializer(
                {"results": rows, "next_before": next_before, "has_more": has_more},
                context={"request": request},
            ).data
        )


@extend_schema(
    tags=["changes"],
    responses=ChangeRowSerializer(many=True),
    parameters=[
        OpenApiParameter("minor", str, description="minor=0 hides minor edits."),
        OpenApiParameter("bots", str, description="bots=0 hides bot edits."),
        OpenApiParameter("days", int),
        OpenApiParameter("since", str),
        OpenApiParameter("page", int),
        OpenApiParameter("page_size", int),
    ],
)
class WatchlistView(ListAPIView):
    """``GET /api/watchlist/`` — changes to the caller's watched articles, 50 per page.

    There is no ``type`` parameter: the queryset is revisions only, so
    ``type=talk`` would have nothing to return (critique #21).
    """

    serializer_class = ChangeRowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination
    filter_backends: list = []

    def get_queryset(self):
        queryset = Revision.objects.for_watchlist(self.request.user).annotate(
            latest_revision_id=latest_revision_subquery()
        )
        since = _parse_since(self.request)
        if since is not None:
            queryset = queryset.filter(created_at__gte=since)
        if _flag_off(self.request, "minor"):
            queryset = queryset.filter(is_minor=False)
        if _flag_off(self.request, "bots"):
            queryset = queryset.filter(is_bot=False)
        return queryset

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        rows = [row_from_revision(revision) for revision in page]
        return self.get_paginated_response(
            ChangeRowSerializer(rows, many=True, context={"request": request}).data
        )


@extend_schema(
    tags=["changes"],
    responses=ChangeRowSerializer(many=True),
    parameters=[
        OpenApiParameter("minor", str),
        OpenApiParameter("bots", str),
        OpenApiParameter("days", int),
        OpenApiParameter("since", str),
        OpenApiParameter("page", int),
        OpenApiParameter("page_size", int),
    ],
)
class ContributionsView(ListAPIView):
    """``GET /api/users/{username}/contributions/`` — one contributor's edits."""

    serializer_class = ChangeRowSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = FeedPagination
    filter_backends: list = []

    def get_queryset(self):
        from django.contrib.auth import get_user_model

        username = self.kwargs["username"]
        if not get_user_model().objects.filter(username=username).exists():
            raise NotFound("No such user.")
        queryset = Revision.objects.contributions(username, viewer=self.request.user).annotate(
            latest_revision_id=latest_revision_subquery()
        )
        since = _parse_since(self.request)
        if since is not None:
            queryset = queryset.filter(created_at__gte=since)
        if _flag_off(self.request, "minor"):
            queryset = queryset.filter(is_minor=False)
        if _flag_off(self.request, "bots"):
            queryset = queryset.filter(is_bot=False)
        return queryset

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        rows = [row_from_revision(revision) for revision in page]
        return self.get_paginated_response(
            ChangeRowSerializer(rows, many=True, context={"request": request}).data
        )


# --------------------------------------------------------------------------- #
# Main page, statistics, wanted pages
# --------------------------------------------------------------------------- #
@extend_schema(tags=["site"], responses=MainPageSerializer)
class MainPageView(APIView):
    """``GET /api/main-page/`` (DECISIONS §5). "In the news" is deliberately absent."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        payload = cache.get(main_page_cache_key())
        if payload is None:
            payload = MainPageSerializer(self._build(), context={"request": request}).data
            cache.set(main_page_cache_key(), payload, MAIN_PAGE_CACHE_TTL)
        return Response(payload)

    @staticmethod
    def _build() -> dict[str, Any]:
        featured_blocks = list(
            MainPageBlock.objects.filter(kind=MainPageBlock.Kind.FEATURED, is_active=True)
            .exclude(article__isnull=True)
            .select_related("article", "article__category")
            .order_by("position", "id")[:6]
        )
        articles = [
            block.article
            for block in featured_blocks
            if block.article.is_published and not block.article.is_deleted
        ]
        featured = articles[0] if articles else None
        if featured is None:
            # An empty MainPageBlock table must still produce a usable home
            # page, so fall back to the most-viewed article.
            featured = (
                Article.objects.published()
                .select_related("category")
                .order_by("-view_count", "-updated_at")
                .first()
            )
        dyk = list(
            MainPageBlock.objects.filter(kind=MainPageBlock.Kind.DYK, is_active=True)
            .order_by("position", "id")
            .values_list("body_markdown", flat=True)[:8]
        )
        otd = [
            OnThisDaySerializer.from_block(block)
            for block in MainPageBlock.objects.filter(
                kind=MainPageBlock.Kind.OTD, is_active=True
            ).order_by("position", "id")[:8]
        ]
        return {
            "featured": featured,
            "recently_featured": articles[1:],
            "dyk": dyk,
            "otd": otd,
            "stats": site_stats(),
        }


@extend_schema(tags=["site"], responses=SiteStatsSerializer)
class SiteStatsView(APIView):
    """``GET /api/stats/`` — the same payload as ``/api/articles/stats/``."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(SiteStatsSerializer(site_stats()).data)


@extend_schema(
    tags=["site"],
    responses=WantedPageSerializer(many=True),
    parameters=[OpenApiParameter("page", int), OpenApiParameter("page_size", int)],
)
class WantedPagesView(ListAPIView):
    """``GET /api/wanted/`` — the red links the most articles point at.

    One aggregate over ``ArticleLink``; the rows come back as dicts, so nothing
    is instantiated per row.
    """

    serializer_class = WantedPageSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = FeedPagination
    filter_backends: list = []

    def get_queryset(self):
        return (
            ArticleLink.objects.filter(to_article__isnull=True)
            .values("to_slug", "to_title")
            .annotate(incoming=Count("from_article_id", distinct=True))
            .order_by("-incoming", "to_title")
        )

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        rows = [
            {"slug": row["to_slug"], "title": row["to_title"], "incoming": row["incoming"]}
            for row in page
        ]
        return self.get_paginated_response(WantedPageSerializer(rows, many=True).data)


# --------------------------------------------------------------------------- #
# RSS
# --------------------------------------------------------------------------- #
class RecentChangesFeed(Feed):
    """``GET /api/feeds/changes.rss`` (DECISIONS §14).

    Absolute URLs come from ``PUBLIC_BASE_URL``, never from the request: nginx
    rewrites ``Host`` to the Railway service domain, so a request-derived link
    would advertise the backend's internal hostname to every feed reader.
    """

    title = "Wikiverse — recent changes"
    description = "The most recent edits to Wikiverse articles."

    def get_object(self, request, *args, **kwargs) -> int:
        return _bounded(_int_param(request.GET.get("limit")), 50)

    def link(self, obj) -> str:
        return spa_url("/changes")

    def items(self, obj: int):
        return (
            Revision.objects.feed()
            .visible_to(None)
            .annotate(latest_revision_id=latest_revision_subquery())[:obj]
        )

    def item_title(self, item: Revision) -> str:
        sign = "+" if item.byte_delta >= 0 else "−"
        return f"{item.article.title} ({sign}{abs(item.byte_delta)})"

    def item_description(self, item: Revision) -> str:
        editor = item.editor.username if item.editor else "an anonymous contributor"
        return item.comment or f"Edited by {editor}."

    def item_author_name(self, item: Revision) -> str | None:
        return item.editor.username if item.editor else None

    def item_link(self, item: Revision) -> str:
        if item.parent_id:
            return spa_url(f"/wiki/{item.article.slug}/diff?from={item.parent_id}&to={item.pk}")
        return spa_url(f"/wiki/{item.article.slug}")

    def item_pubdate(self, item: Revision):
        return item.created_at

    def item_guid(self, item: Revision) -> str:
        return f"wikiverse:revision:{item.pk}"

    def item_guid_is_permalink(self, item: Revision) -> bool:
        return False
