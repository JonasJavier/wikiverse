"""Query sets for the wiki.

Every PostgreSQL-only expression sits behind :func:`is_postgres`, which is
evaluated at **call time** (``connection.vendor``), never at import time: the
same deployment artefact has to run against SQLite locally and in CI and
against PostgreSQL in production, and the migration graph must be identical on
both.

Never replace the gate with ``try/except DatabaseError``:
:class:`~django.contrib.postgres.search.SearchHeadline` raises
``AttributeError`` on SQLite, which that would not catch.
"""

from __future__ import annotations

from django.conf import settings
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    TrigramWordSimilarity,
)
from django.db import connection, models
from django.db.models import F, Q, Value
from django.db.models.functions import Greatest

#: ``similarity('postgersql', 'PostgreSQL') == 0.4667``, so 0.30 is the right
#: floor; 0.45 would already lose that correction.
TRIGRAM_FLOOR = 0.30

#: Fallback when ``settings.SEARCH_CONFIG`` is absent. Migration
#: ``articles/0004`` always creates a text search configuration with this name,
#: so it always resolves on PostgreSQL.
DEFAULT_SEARCH_CONFIG = "wikiverse_english"

#: Columns a card/list row needs. ``content`` is deliberately absent: it is the
#: single largest column and no list endpoint renders it.
CARD_DEFER = ("content",)


def is_postgres() -> bool:
    """True when the default connection is PostgreSQL."""
    return connection.vendor == "postgresql"


def search_config() -> str:
    """The text search configuration name used for every FTS expression."""
    return getattr(settings, "SEARCH_CONFIG", None) or DEFAULT_SEARCH_CONFIG


# --------------------------------------------------------------------------- #
# Articles
# --------------------------------------------------------------------------- #
class ArticleQuerySet(models.QuerySet):
    """Visibility, card projections and search for :class:`Article`."""

    # ---- visibility ------------------------------------------------------ #
    def published(self):
        """Publicly readable articles: published and not soft-deleted."""
        return self.filter(is_published=True, is_deleted=False)

    def visible(self, user=None):
        """Articles ``user`` is allowed to see.

        Staff see everything, including drafts and soft-deleted rows. A signed
        in user additionally sees their own drafts. Anonymous callers see only
        published, non-deleted articles.
        """
        if user is not None and getattr(user, "is_staff", False):
            return self
        base = Q(is_published=True, is_deleted=False)
        if user is not None and getattr(user, "is_authenticated", False):
            base |= Q(author=user, is_deleted=False)
        return self.filter(base)

    def deleted(self):
        """Soft-deleted articles, for the staff-only restore view."""
        return self.filter(is_deleted=True)

    # ---- projections ----------------------------------------------------- #
    def with_card_fields(self):
        """Everything a list/card row renders, and nothing more.

        One query, no N+1, and ``content`` deferred so a 50-row page does not
        transfer 50 Markdown bodies. ``read_time`` reads ``word_count``, not
        ``content``, which is what makes the defer safe.
        """
        return self.select_related("category", "author").defer(*CARD_DEFER)

    def with_detail_fields(self):
        """Relations a single-article read needs."""
        return self.select_related("category", "author", "last_editor").prefetch_related(
            "references", "extra_categories"
        )

    # ---- search ---------------------------------------------------------- #
    def search(self, term: str):
        """Rank-ordered search.

        PostgreSQL: weighted ``tsvector`` match, falling back to a ``pg_trgm``
        fuzzy retry when the strict query finds nothing. SQLite: ``icontains``
        with a constant ``rank`` so the wire shape never changes.
        """
        term = (term or "").strip()
        if not term:
            return self
        if not is_postgres():
            return self._search_fallback(term)

        query = SearchQuery(term, search_type="websearch", config=search_config())
        qs = (
            self.annotate(rank=SearchRank(F("search_vector"), query, normalization=Value(32)))
            .filter(search_vector=query)
            .order_by("-rank", "-view_count", "-updated_at")
        )
        if qs.exists():
            return qs
        return self.fuzzy(term)

    def fuzzy(self, term: str):
        """Typo-tolerant search.

        ``__trigram_similar`` (the ``%`` operator) is index-backed by the
        ``gin_trgm_ops`` indexes; ``TrigramWordSimilarity`` in the ``WHERE``
        clause is not, so the operator filters and the function only scores the
        survivors. On SQLite this degrades to the ``icontains`` path.
        """
        term = (term or "").strip()
        if not term:
            return self
        if not is_postgres():
            return self._search_fallback(term)
        return (
            self.filter(Q(title__trigram_similar=term) | Q(short_description__trigram_similar=term))
            .annotate(
                rank=Greatest(
                    TrigramWordSimilarity(term, "title"),
                    TrigramWordSimilarity(term, "short_description"),
                )
            )
            .filter(rank__gte=TRIGRAM_FLOOR)
            .order_by("-rank", "-view_count", "-updated_at")
        )

    def _search_fallback(self, term: str):
        """SQLite search. Same response shape, lower result quality."""
        return (
            self.annotate(rank=Value(0.0, output_field=models.FloatField()))
            .filter(
                Q(title__icontains=term)
                | Q(short_description__icontains=term)
                | Q(summary__icontains=term)
                | Q(content__icontains=term)
            )
            .order_by("-view_count", "-updated_at")
        )

    def with_snippet(self, term: str):
        """Annotate ``snippet``/``title_snippet`` with delimiter-marked matches.

        ``ts_headline`` is told to emit the control characters ``\\x02`` and
        ``\\x03`` rather than HTML tags; the serializer escapes the result and
        only then swaps them for ``<mark>``. That way ``ts_headline`` can never
        emit markup of its own. Call this last, and only on PostgreSQL.
        """
        term = (term or "").strip()
        if not is_postgres() or not term:
            return self
        query = SearchQuery(term, search_type="websearch", config=search_config())
        return self.annotate(
            snippet=SearchHeadline(
                "content",
                query,
                config=search_config(),
                start_sel="\x02",
                stop_sel="\x03",
                max_words=28,
                min_words=12,
                max_fragments=2,
                fragment_delimiter=" … ",
                short_word=3,
            ),
            title_snippet=SearchHeadline(
                "title",
                query,
                config=search_config(),
                start_sel="\x02",
                stop_sel="\x03",
                highlight_all=True,
            ),
        )

    def suggest(self, prefix: str, limit: int = 10):
        """Typeahead rows. Never touches ``content``, revisions or view counts."""
        prefix = (prefix or "").strip()
        if len(prefix) < 2:
            return self.none()
        base = self.published()
        if not is_postgres():
            return base.filter(title__icontains=prefix).order_by("-view_count", "title")[:limit]
        return (
            base.filter(Q(title__istartswith=prefix) | Q(title__trigram_similar=prefix))
            .annotate(similarity=TrigramWordSimilarity(prefix, "title"))
            .order_by("-similarity", "-view_count", "title")[:limit]
        )


# --------------------------------------------------------------------------- #
# Revisions
# --------------------------------------------------------------------------- #
class RevisionQuerySet(models.QuerySet):
    """Feeds over :class:`Revision`: recent changes, watchlist, contributions."""

    def feed(self):
        """Newest-first feed with every relation a change row renders.

        A single index scan backward over ``revision_recent`` plus ``LIMIT``;
        constant in table size. ``content`` is deferred because no feed row
        shows a body.
        """
        return (
            self.select_related("article", "article__category", "editor")
            .defer("content", "apparatus", "article__content", "article__infobox")
            .order_by("-created_at", "-id")
        )

    def visible_to(self, user=None):
        """Drop revisions whose article the caller may not read.

        Without this, revision bodies leak the full text of drafts and
        soft-deleted articles to anonymous callers.
        """
        if user is not None and getattr(user, "is_staff", False):
            return self
        base = Q(article__is_published=True, article__is_deleted=False)
        if user is not None and getattr(user, "is_authenticated", False):
            base |= Q(article__author=user, article__is_deleted=False)
        return self.filter(base)

    def for_changes(
        self,
        *,
        user=None,
        viewer=None,
        category=None,
        article=None,
        since=None,
        before=None,
        minor: bool = True,
        bots: bool = True,
    ):
        """Apply the ``/api/changes/`` filter set to :meth:`feed`.

        ``viewer`` is the requesting user (visibility); ``user`` is the
        contributor being filtered on (a username or a user instance).
        ``minor=False`` hides minor edits, ``bots=False`` hides bot edits —
        matching the ``hideMinor``/``hideBot`` URL controls.
        """
        qs = self.feed().visible_to(viewer)
        if user is not None:
            if isinstance(user, str):
                qs = qs.filter(editor__username=user)
            else:
                qs = qs.filter(editor=user)
        if category is not None:
            if isinstance(category, str):
                qs = qs.filter(article__category__slug=category)
            else:
                qs = qs.filter(article__category=category)
        if article is not None:
            if isinstance(article, str):
                qs = qs.filter(article__slug=article)
            else:
                qs = qs.filter(article=article)
        if since is not None:
            qs = qs.filter(created_at__gte=since)
        if before is not None:
            qs = qs.filter(created_at__lt=before)
        if not minor:
            qs = qs.filter(is_minor=False)
        if not bots:
            qs = qs.filter(is_bot=False)
        return qs

    def for_watchlist(self, user):
        """Changes to articles ``user`` watches.

        Uses an ``__in`` subquery rather than a join through ``watchers``: the
        join fans out one row per :class:`Watch` and would duplicate revisions
        the day a second watch flag appears.
        """
        from apps.articles.models import Watch

        if user is None or not getattr(user, "is_authenticated", False):
            return self.none()
        watched = Watch.objects.filter(user=user).values("article_id")
        return self.feed().visible_to(user).filter(article_id__in=models.Subquery(watched))

    def contributions(self, user, viewer=None):
        """One contributor's edits, newest first."""
        qs = self.feed().visible_to(viewer)
        if isinstance(user, str):
            return qs.filter(editor__username=user)
        return qs.filter(editor=user)
