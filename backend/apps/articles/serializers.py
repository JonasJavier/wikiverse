"""Wire shapes for the encyclopedia API.

Field names and field *order* in this module are part of the contract:
``DECISIONS.md`` §2 fixes ``SearchResultSerializer``, §4 fixes
``ChangeRowSerializer``, and :meth:`apps.articles.models.Reference.as_dict`
fixes ``ReferenceSerializer``. A test in another agent's work asserts them, so
do not "tidy" a name.

Two rules worth stating once, because they are easy to undo:

* **Snippets never carry raw markup.** ``ts_headline`` output arrives delimited
  by the control characters ``\\x02``/``\\x03`` and goes through
  :func:`apps.articles.search.safe_headline_to_marked`, which escapes first and
  substitutes ``<mark>`` second. See that function's docstring for why the order
  is load-bearing.
* **List serializers never touch ``content``.** Every list queryset defers it,
  so a field that reads the body would turn one query into one per row.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.articles.markup import strip_markup
from apps.articles.search import safe_headline_to_marked

from .models import (
    Article,
    Category,
    MainPageBlock,
    Reference,
    Revision,
    TalkMessage,
    TalkThread,
)

#: Characters of plain text in a hover-card extract. The measured MediaWiki
#: Popups ``EXTRACT_LENGTH``.
EXTRACT_LENGTH = 525


def plain_extract(markdown: str | None, limit: int = EXTRACT_LENGTH) -> str:
    """Markdown stripped to plain text, cut on a word boundary at ``limit``."""
    text = " ".join(strip_markup(markdown or "").split())
    if len(text) <= limit:
        return text
    head = text[:limit]
    cut = head.rfind(" ")
    return f"{head[:cut] if cut > 0 else head}…"


# --------------------------------------------------------------------------- #
# People and categories
# --------------------------------------------------------------------------- #
class AuthorSerializer(serializers.Serializer):
    """The byline shape, embedded everywhere a user is named."""

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(read_only=True, allow_null=True)


class CategoryStubSerializer(serializers.ModelSerializer):
    """Just enough category to draw a chip (DECISIONS §9: colour is a bar, not a fill)."""

    class Meta:
        model = Category
        fields = ("slug", "name", "color")


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)
    parent = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "color",
            "icon",
            "order",
            "parent",
            "article_count",
        )
        read_only_fields = ("id", "slug", "article_count")


# --------------------------------------------------------------------------- #
# References
# --------------------------------------------------------------------------- #
class ReferenceSerializer(serializers.ModelSerializer):
    """Field list and order match :meth:`Reference.as_dict` exactly.

    ``Revision.apparatus["references"]`` stores the same shape, so a history
    entry replays with one shape rather than two.
    """

    class Meta:
        model = Reference
        fields = (
            "key",
            "order",
            "title",
            "url",
            "authors",
            "publisher",
            "published_on",
            "accessed_on",
            "identifier",
            "quote",
        )


# --------------------------------------------------------------------------- #
# Articles
# --------------------------------------------------------------------------- #
class ArticleStubSerializer(serializers.ModelSerializer):
    """A card-free reference to an article: enough to render a link."""

    category = CategoryStubSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ("slug", "title", "page_type", "category")


class ChangeArticleSerializer(serializers.Serializer):
    """``{slug, title}`` — the exact shape DECISIONS §4 gives a change row."""

    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)


class ArticleListSerializer(serializers.ModelSerializer):
    """Card/list row. Must never gain ``content`` or ``infobox`` — both are deferred."""

    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    read_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "summary",
            "category",
            "author",
            "page_type",
            "is_stub",
            "view_count",
            "word_count",
            "byte_size",
            "read_time",
            "lead_image_url",
            "created_at",
            "updated_at",
        )


class RevisionStubSerializer(serializers.ModelSerializer):
    """The "last edited by X" line on an article."""

    editor = AuthorSerializer(read_only=True)

    class Meta:
        model = Revision
        fields = ("id", "editor", "comment", "byte_delta", "is_minor", "created_at")


class ArticleDetailSerializer(ArticleListSerializer):
    """Full article read, including the Markdown body."""

    last_editor = AuthorSerializer(read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    categories = serializers.SerializerMethodField()
    revision_count = serializers.IntegerField(source="revision_total", read_only=True)
    contributor_count = serializers.IntegerField(source="contributor_total", read_only=True)
    watcher_count = serializers.IntegerField(source="watcher_total", read_only=True)
    backlink_count = serializers.IntegerField(source="backlink_total", read_only=True)
    talk_thread_count = serializers.IntegerField(source="talk_thread_total", read_only=True)
    is_watched = serializers.BooleanField(read_only=True, default=False)
    is_disambiguation = serializers.BooleanField(read_only=True)
    redirected_from = serializers.SerializerMethodField()
    latest_revision = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + (
            "content",
            "last_editor",
            "is_published",
            "protection",
            "is_disambiguation",
            "infobox",
            "references",
            "categories",
            "lead_image_alt",
            "lead_image_caption",
            "lead_image_credit",
            "lead_image_license",
            "lead_image_source_url",
            "revision_count",
            "contributor_count",
            "watcher_count",
            "backlink_count",
            "talk_thread_count",
            "is_watched",
            "redirected_from",
            "latest_revision",
        )

    @extend_schema_field(CategoryStubSerializer(many=True))
    def get_categories(self, obj: Article) -> list[dict[str, Any]]:
        """Every category, primary first (DECISIONS §13)."""
        rows = [obj.category] if obj.category_id else []
        rows += [c for c in obj.extra_categories.all() if c.pk != obj.category_id]
        return CategoryStubSerializer(rows, many=True).data

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_redirected_from(self, obj: Article) -> str | None:
        """The title the reader typed, when they arrived through a redirect."""
        return getattr(obj, "redirected_from_title", None)

    @extend_schema_field(RevisionStubSerializer(allow_null=True))
    def get_latest_revision(self, obj: Article) -> dict[str, Any] | None:
        revision = getattr(obj, "latest_revision_row", None)
        if revision is None:
            return None
        return RevisionStubSerializer(revision).data


class ArticleWriteSerializer(serializers.ModelSerializer):
    """Create/update. ``comment`` and ``is_minor`` belong to the *revision*.

    They stay in ``validated_data`` so the view can read them before
    :meth:`create`/:meth:`update` strips them, which is the only place that knows
    whether a revision is actually being written.
    """

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    extra_categories = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )
    references = ReferenceSerializer(many=True, required=False)
    comment = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=255,
        help_text="Edit summary stored on the revision.",
    )
    is_minor = serializers.BooleanField(
        write_only=True,
        required=False,
        default=False,
        help_text="Flags the revision as minor in Recent changes.",
    )

    #: Fields only the article's author or a staff member may change
    #: (DECISIONS §15 — rejected field-level with 400, never 403).
    PRIVILEGED_FIELDS = ("protection", "is_published")

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "summary",
            "content",
            "category",
            "extra_categories",
            "page_type",
            "is_stub",
            "protection",
            "infobox",
            "lead_image_url",
            "lead_image_alt",
            "lead_image_caption",
            "lead_image_credit",
            "lead_image_license",
            "lead_image_source_url",
            "is_published",
            "references",
            "comment",
            "is_minor",
        )
        # The slug is stable for the life of the article: a wiki that renames its
        # own URLs breaks every inbound link and every [[wikilink]] to it.
        read_only_fields = ("id", "slug")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            # PUT is a **partial replace**, by decision: every model-derived
            # field becomes optional once an instance exists, so a PUT that omits
            # ``summary`` keeps the stored value instead of blanking it. A wiki
            # edit form posts the section it edited, not the whole record, and a
            # true replace would silently destroy fields the editor never saw.
            # Creation keeps its required fields, so POST still needs a title.
            for field in self.fields.values():
                field.required = False

    # ---- validation ------------------------------------------------------ #
    def validate_title(self, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value

    def validate_lead_image_url(self, value: str) -> str:
        """Confine remote images to the CSP ``img-src`` allowlist (DECISIONS §7.4).

        The allowlist is deliberately the same two hosts as the Content Security
        Policy: an image the browser would refuse to load must not validate here,
        or the editor gets a silent broken image and no explanation.
        """
        if not value:
            return value
        allowed = [h.lower() for h in getattr(settings, "LEAD_IMAGE_ALLOWED_HOSTS", [])]
        parts = urlsplit(value)
        if parts.scheme != "https" or not parts.netloc:
            raise serializers.ValidationError("Lead image URL must be an absolute https:// URL.")
        if parts.netloc.lower() not in allowed:
            raise serializers.ValidationError(
                "Lead images must be hosted on one of: " + ", ".join(allowed) + "."
            )
        return value

    def validate_references(self, value: list[dict]) -> list[dict]:
        keys = [row.get("key") for row in value]
        duplicates = sorted({k for k in keys if keys.count(k) > 1})
        if duplicates:
            raise serializers.ValidationError(
                "Reference keys must be unique within an article; repeated: "
                + ", ".join(duplicates)
            )
        return value

    def validate(self, attrs: dict) -> dict:
        errors: dict[str, list[str]] = {}
        request = self.context.get("request")
        user = getattr(request, "user", None)
        instance = self.instance

        if instance is not None and not self._may_set_status(user, instance):
            for field in self.PRIVILEGED_FIELDS:
                if field in attrs and attrs[field] != getattr(instance, field):
                    errors[field] = [
                        f"Only the article's author or staff may change {field}. "
                        "Your edit to the article body is allowed; remove this field."
                    ]
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    @staticmethod
    def _may_set_status(user, instance: Article) -> bool:
        if user is None or not getattr(user, "is_authenticated", False):
            return False
        return bool(user.is_staff) or instance.author_id == user.id

    # ---- persistence ----------------------------------------------------- #
    def create(self, validated_data: dict) -> Article:
        validated_data.pop("comment", None)
        validated_data.pop("is_minor", None)
        references = validated_data.pop("references", None)
        article = super().create(validated_data)
        if references is not None:
            self._replace_references(article, references)
        return article

    def update(self, instance: Article, validated_data: dict) -> Article:
        validated_data.pop("comment", None)
        validated_data.pop("is_minor", None)
        references = validated_data.pop("references", None)
        article = super().update(instance, validated_data)
        if references is not None:
            self._replace_references(article, references)
        return article

    @staticmethod
    def _replace_references(article: Article, rows: list[dict]) -> None:
        """References are a set, not a log: replace them wholesale.

        Identity is ``(article, key)`` and the footnote markers in the body point
        at ``key``, so a partial merge would leave orphans that resolve to
        nothing.
        """
        article.references.all().delete()
        Reference.objects.bulk_create(
            [
                Reference(article=article, **{**row, "order": row.get("order") or index})
                for index, row in enumerate(rows)
            ]
        )


class ArticleInfoSerializer(serializers.Serializer):
    """``GET /api/articles/{slug}/info/`` — page information (DECISIONS §17)."""

    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    byte_size = serializers.IntegerField(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    revision_count = serializers.IntegerField(read_only=True)
    contributor_count = serializers.IntegerField(read_only=True)
    watcher_count = serializers.IntegerField(read_only=True)
    backlink_count = serializers.IntegerField(read_only=True)
    redirect_count = serializers.IntegerField(read_only=True)
    talk_thread_count = serializers.IntegerField(read_only=True)
    reference_count = serializers.IntegerField(read_only=True)
    outgoing_link_count = serializers.IntegerField(read_only=True)
    red_link_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    page_type = serializers.CharField(read_only=True)
    protection = serializers.CharField(read_only=True)
    is_stub = serializers.BooleanField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    author = AuthorSerializer(read_only=True, allow_null=True)
    last_editor = AuthorSerializer(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class PreviewSerializer(serializers.ModelSerializer):
    """``GET /api/articles/{slug}/preview/`` — the hover card.

    ``extract`` is plain text, not Markdown: the card is one paragraph in a
    tooltip, and shipping Markdown would mean running the whole renderer (and its
    wikilink resolution) inside a hover.
    """

    extract = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "short_description",
            "extract",
            "lead_image_url",
            "lead_image_alt",
            "page_type",
            "is_stub",
        )

    @extend_schema_field(serializers.CharField())
    def get_extract(self, obj: Article) -> str:
        return plain_extract(obj.content)


class BacklinkSerializer(serializers.Serializer):
    """One "what links here" row."""

    source = ArticleStubSerializer(read_only=True)
    occurrences = serializers.IntegerField(read_only=True)


class WantedPageSerializer(serializers.Serializer):
    """A red link several articles point at, ranked by how many."""

    title = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    incoming = serializers.IntegerField(read_only=True)


class WatchSerializer(serializers.Serializer):
    """``POST /api/articles/{slug}/watch/`` response."""

    watching = serializers.BooleanField(read_only=True)


# --------------------------------------------------------------------------- #
# Revisions and diffs
# --------------------------------------------------------------------------- #
class RevisionSerializer(serializers.ModelSerializer):
    """A history row. ``content`` and ``apparatus`` are deferred, so not here."""

    editor = AuthorSerializer(read_only=True)

    class Meta:
        model = Revision
        fields = (
            "id",
            "parent",
            "editor",
            "title",
            "summary",
            "comment",
            "byte_size",
            "byte_delta",
            "is_minor",
            "is_page_creation",
            "is_bot",
            "tags",
            "created_at",
        )


class RevisionDetailSerializer(RevisionSerializer):
    """One revision in full, for the "old version of this page" view."""

    class Meta(RevisionSerializer.Meta):
        fields = RevisionSerializer.Meta.fields + ("content", "apparatus")


class DiffStatsSerializer(serializers.Serializer):
    lines_added = serializers.IntegerField(read_only=True)
    lines_removed = serializers.IntegerField(read_only=True)
    lines_changed = serializers.IntegerField(read_only=True)
    bytes_added = serializers.IntegerField(read_only=True)
    bytes_removed = serializers.IntegerField(read_only=True)


class DiffRowSerializer(serializers.Serializer):
    t = serializers.ChoiceField(choices=["=", "~", "+", "-"], read_only=True)
    a = serializers.IntegerField(read_only=True, allow_null=True)
    b = serializers.IntegerField(read_only=True, allow_null=True)
    ops = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        read_only=True,
        help_text='Pairs of [kind, text] where kind is "=", "+" or "-".',
    )


class DiffHunkSerializer(serializers.Serializer):
    a_start = serializers.IntegerField(read_only=True)
    a_lines = serializers.IntegerField(read_only=True)
    b_start = serializers.IntegerField(read_only=True)
    b_lines = serializers.IntegerField(read_only=True)
    rows = DiffRowSerializer(many=True, read_only=True)


class DiffRevisionSerializer(serializers.Serializer):
    """The two ends of a diff, as the header renders them."""

    id = serializers.IntegerField(read_only=True, allow_null=True)
    editor = AuthorSerializer(read_only=True, allow_null=True)
    comment = serializers.CharField(read_only=True, allow_blank=True)
    byte_size = serializers.IntegerField(read_only=True, allow_null=True)
    is_minor = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, allow_null=True)


class DiffSerializer(serializers.Serializer):
    """``GET /api/articles/{slug}/diff/``.

    Schema-only: the payload is assembled by :mod:`apps.articles.diff` and the
    view, never by a model.
    """

    article = ArticleStubSerializer(read_only=True)
    from_revision = DiffRevisionSerializer(read_only=True)
    to_revision = DiffRevisionSerializer(read_only=True)
    prev_id = serializers.IntegerField(read_only=True, allow_null=True)
    next_id = serializers.IntegerField(read_only=True, allow_null=True)
    created = serializers.BooleanField(read_only=True)
    truncated = serializers.BooleanField(read_only=True)
    title_changed = serializers.BooleanField(read_only=True)
    summary_changed = serializers.BooleanField(read_only=True)
    stats = DiffStatsSerializer(read_only=True)
    hunks = DiffHunkSerializer(many=True, read_only=True)


# --------------------------------------------------------------------------- #
# Search
# --------------------------------------------------------------------------- #
class SearchResultSerializer(serializers.ModelSerializer):
    """Exactly the nine fields DECISIONS §2 names, in that order.

    ``snippet``/``title_snippet`` fall back to ``summary``/``title``: the
    ``ts_headline`` annotation exists only on PostgreSQL and only for a
    non-blank term, and a required field that silently disappears would break
    the whole test suite (which runs on SQLite).
    """

    title_snippet = serializers.SerializerMethodField()
    snippet = serializers.SerializerMethodField()
    rank = serializers.FloatField(read_only=True)
    category = CategoryStubSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "title_snippet",
            "snippet",
            "rank",
            "category",
            "updated_at",
            "byte_size",
            "word_count",
        )

    @extend_schema_field(serializers.CharField())
    def get_title_snippet(self, obj: Article) -> str:
        raw = getattr(obj, "title_snippet", None)
        return safe_headline_to_marked(raw) if raw else safe_headline_to_marked(obj.title)

    @extend_schema_field(serializers.CharField())
    def get_snippet(self, obj: Article) -> str:
        raw = getattr(obj, "snippet", None)
        if raw:
            return safe_headline_to_marked(raw)
        return safe_headline_to_marked(obj.summary or obj.short_description or "")


class SearchResponseSerializer(serializers.Serializer):
    """The search envelope, declared explicitly so the schema gate passes.

    ``did_you_mean`` is a top-level key on the page envelope, not a per-row
    field (DECISIONS §2).
    """

    count = serializers.IntegerField(read_only=True)
    next = serializers.CharField(read_only=True, allow_null=True)
    previous = serializers.CharField(read_only=True, allow_null=True)
    query = serializers.CharField(read_only=True, allow_blank=True)
    ordering = serializers.CharField(read_only=True)
    did_you_mean = serializers.CharField(read_only=True, allow_null=True)
    results = SearchResultSerializer(many=True, read_only=True)


class SuggestionSerializer(serializers.Serializer):
    """Typeahead row: the gloss, never a body snippet."""

    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    short_description = serializers.CharField(read_only=True, allow_blank=True)


# --------------------------------------------------------------------------- #
# Recent changes / watchlist / contributions
# --------------------------------------------------------------------------- #
class TalkThreadStubSerializer(serializers.Serializer):
    """``{id, title}`` — what a talk change row carries."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class ChangeRowSerializer(serializers.Serializer):
    """One row of Recent changes, Watchlist or Contributions.

    The field names are normative (DECISIONS §4) and the same React component
    renders all three feeds, so an edit row and a talk row must be the same
    shape. ``byte_size``/``byte_delta`` are null on talk rows and ``thread`` is
    null on edit rows; the UI draws the grey dash for the nulls.

    ``id`` is unique only *within* ``kind``; the React key is
    ``` `${kind}-${id}` ```.
    """

    kind = serializers.ChoiceField(choices=["edit", "talk"], read_only=True)
    id = serializers.IntegerField(read_only=True)
    parent_id = serializers.IntegerField(read_only=True, allow_null=True)
    timestamp = serializers.DateTimeField(read_only=True)
    article = ChangeArticleSerializer(read_only=True)
    user = AuthorSerializer(read_only=True, allow_null=True)
    comment = serializers.CharField(read_only=True, allow_blank=True)
    byte_size = serializers.IntegerField(read_only=True, allow_null=True)
    byte_delta = serializers.IntegerField(read_only=True, allow_null=True)
    is_minor = serializers.BooleanField(read_only=True)
    is_page_creation = serializers.BooleanField(read_only=True)
    is_bot = serializers.BooleanField(read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(), read_only=True)
    thread = TalkThreadStubSerializer(read_only=True, allow_null=True)


class ChangeFeedSerializer(serializers.Serializer):
    """The cursor envelope for ``/api/changes/``.

    Not a DRF paginator, so ``spectacular --fail-on-warn`` needs this declared
    explicitly (critique #24).
    """

    results = ChangeRowSerializer(many=True, read_only=True)
    next_before = serializers.DateTimeField(read_only=True, allow_null=True)
    has_more = serializers.BooleanField(read_only=True)


# --------------------------------------------------------------------------- #
# Talk
# --------------------------------------------------------------------------- #
class TalkMessageSerializer(serializers.ModelSerializer):
    """A talk message. ``body`` is ``null`` on a deleted message for non-staff."""

    author = AuthorSerializer(read_only=True)
    body = serializers.SerializerMethodField()

    class Meta:
        model = TalkMessage
        fields = (
            "id",
            "thread",
            "parent",
            "author",
            "body",
            "depth",
            "created_at",
            "edited_at",
            "is_deleted",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_body(self, obj: TalkMessage) -> str | None:
        """Withhold the text of a deleted message, keeping the row for the thread shape.

        Wikipedia strikes a removed comment rather than vanishing it, because a
        hole in a threaded discussion is unreadable. Staff still see the body so
        moderation is reviewable.
        """
        if not obj.is_deleted:
            return obj.body
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_staff", False):
            return obj.body
        return None


class TalkMessageWriteSerializer(serializers.ModelSerializer):
    """``POST .../messages/`` and ``PATCH /api/talk/messages/{id}/``."""

    class Meta:
        model = TalkMessage
        fields = ("body", "parent")
        extra_kwargs = {"parent": {"required": False, "allow_null": True}}

    def validate_body(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("A message needs a body.")
        return value


class TalkThreadSerializer(serializers.ModelSerializer):
    """Thread list row. Counts are denormalised, so no aggregate query."""

    created_by = AuthorSerializer(read_only=True)

    class Meta:
        model = TalkThread
        fields = (
            "id",
            "title",
            "created_by",
            "created_at",
            "updated_at",
            "last_message_at",
            "message_count",
            "participant_count",
            "is_resolved",
            "is_locked",
        )
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "last_message_at",
            "message_count",
            "participant_count",
        )


class TalkThreadDetailSerializer(TalkThreadSerializer):
    messages = TalkMessageSerializer(many=True, read_only=True)
    article = ArticleStubSerializer(read_only=True)

    class Meta(TalkThreadSerializer.Meta):
        fields = TalkThreadSerializer.Meta.fields + ("article", "messages")


class TalkThreadUpdateSerializer(serializers.ModelSerializer):
    """``PATCH /api/talk/threads/{id}/``.

    ``is_locked`` is accepted here and rejected in the view for non-staff, so the
    error is field-level rather than a blanket 403 on a thread its creator is
    otherwise allowed to change.
    """

    class Meta:
        model = TalkThread
        fields = ("title", "is_resolved", "is_locked")
        extra_kwargs = {
            "title": {"required": False},
            "is_resolved": {"required": False},
            "is_locked": {"required": False},
        }

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Thread title must be at least 3 characters.")
        return value


class TalkThreadCreateSerializer(serializers.Serializer):
    """Opening a thread posts its first message in the same call."""

    title = serializers.CharField(max_length=200)
    body = serializers.CharField()

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Thread title must be at least 3 characters.")
        return value

    def validate_body(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("A thread needs an opening message.")
        return value


# --------------------------------------------------------------------------- #
# Site statistics and the main page
# --------------------------------------------------------------------------- #
class SiteStatsSerializer(serializers.Serializer):
    """Aggregate counts for the main page and the footer."""

    articles = serializers.IntegerField(read_only=True)
    categories = serializers.IntegerField(read_only=True)
    contributors = serializers.IntegerField(read_only=True)
    total_views = serializers.IntegerField(read_only=True)
    revisions = serializers.IntegerField(read_only=True)
    talk_messages = serializers.IntegerField(read_only=True)
    words = serializers.IntegerField(read_only=True)
    stubs = serializers.IntegerField(read_only=True)


class FeaturedArticleSerializer(ArticleStubSerializer):
    """The main page hero: a stub plus the plain-text opening."""

    extract = serializers.SerializerMethodField()

    class Meta(ArticleStubSerializer.Meta):
        fields = ArticleStubSerializer.Meta.fields + (
            "short_description",
            "summary",
            "lead_image_url",
            "lead_image_alt",
            "extract",
        )

    @extend_schema_field(serializers.CharField())
    def get_extract(self, obj: Article) -> str:
        return plain_extract(obj.content)


class OnThisDaySerializer(serializers.Serializer):
    year = serializers.IntegerField(read_only=True, allow_null=True)
    month = serializers.IntegerField(read_only=True, allow_null=True)
    day = serializers.IntegerField(read_only=True, allow_null=True)
    body = serializers.CharField(read_only=True)

    @staticmethod
    def from_block(block: MainPageBlock) -> dict[str, Any]:
        return {
            "year": block.event_year,
            "month": block.event_month,
            "day": block.event_day,
            "body": block.body_markdown,
        }


class MainPageSerializer(serializers.Serializer):
    """``GET /api/main-page/`` (DECISIONS §5). "In the news" is cut."""

    featured = FeaturedArticleSerializer(read_only=True, allow_null=True)
    recently_featured = ArticleStubSerializer(many=True, read_only=True)
    dyk = serializers.ListField(child=serializers.CharField(), read_only=True)
    otd = OnThisDaySerializer(many=True, read_only=True)
    stats = SiteStatsSerializer(read_only=True)
