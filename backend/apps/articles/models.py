"""The wiki data model.

Shape of the graph:

* :class:`Category` — a shallow (two level) taxonomy.
* :class:`Article` — the page itself, plus its denormalised counters and the
  PostgreSQL ``search_vector``.
* :class:`Reference` — structured citations, addressed from the body by
  ``[^key]`` markers.
* :class:`Redirect` — an alias slug resolving to an article.
* :class:`ArticleLink` — extracted ``[[wikilinks]]``; powers "what links here"
  and red links.
* :class:`Revision` — the immutable history, one row per edit.
* :class:`TalkThread` / :class:`TalkMessage` — per-article discussion.
* :class:`Watch` — a private interest in an article.
* :class:`MainPageBlock` — editorial content for the front page.

Denormalised counters (``Article.revision_total`` and friends,
``TalkThread.message_count``, ``User.edit_count``) are maintained by the code
that mutates the underlying rows and repaired by ``manage.py rebuild_counts``;
each carries a ``recount``/``touch`` method that re-derives it from the
database, and that method is the single definition of what the counter means.
"""

from __future__ import annotations

import math

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Count, Max
from django.utils import timezone

from apps.common.utils import RESERVED_SLUGS, count_words, unique_slugify, wiki_slug

from .infobox import validate_infobox
from .markup import extract_wikilinks
from .querysets import ArticleQuerySet, RevisionQuerySet


class Category(models.Model):
    """A topic grouping for articles (e.g. Programming, Science)."""

    #: Two levels is all a general encyclopedia of this size needs, and it
    #: keeps the sidebar tree renderable without recursion.
    MAX_DEPTH = 2

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    color = models.CharField(
        max_length=7,
        default="#3b82f6",
        help_text="Hex color used for the category chip in the UI.",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Optional parent category. At most two levels deep.",
    )
    icon = models.CharField(
        max_length=40,
        blank=True,
        help_text="lucide-react icon name, e.g. 'atom'.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Manual sort key; ties fall back to name.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["order", "name"]
        indexes = [models.Index(fields=["parent", "order"], name="category_parent_order")]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            unique_slugify(self, self.name, max_length=90)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        """Reject self-parenting, cycles and nesting deeper than two levels.

        SQL cannot express this portably, so it is enforced here and mirrored in
        ``CategorySerializer.validate_parent``.
        """
        super().clean()
        if self.parent_id is None:
            return
        if self.pk is not None and self.parent_id == self.pk:
            raise ValidationError({"parent": "A category cannot be its own parent."})
        seen = {self.pk} if self.pk is not None else set()
        node = self.parent
        depth = 1
        while node is not None:
            if node.pk in seen:
                raise ValidationError({"parent": "That parent would create a category cycle."})
            seen.add(node.pk)
            depth += 1
            if depth > self.MAX_DEPTH:
                raise ValidationError(
                    {"parent": f"Categories may be nested at most {self.MAX_DEPTH} levels deep."}
                )
            node = node.parent

    @property
    def depth(self) -> int:
        """1 for a top-level category, 2 for a child."""
        return 1 if self.parent_id is None else 2


class Article(models.Model):
    """An encyclopedia article written in Markdown."""

    class PageType(models.TextChoices):
        ARTICLE = "article", "Article"
        DISAMBIGUATION = "disambiguation", "Disambiguation"
        LIST = "list", "List"

    class Protection(models.TextChoices):
        OPEN = "open", "Open — any signed-in user may edit"
        SEMI = "semi", "Semi-protected — established users only"
        FULL = "full", "Fully protected — staff only"

    #: Minimum ``User.edit_count`` to edit a semi-protected article.
    SEMI_PROTECT_MIN_EDITS = 5

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, db_index=True)
    short_description = models.CharField(
        max_length=120,
        blank=True,
        help_text="5-12 word gloss. Powers the typeahead row and the hover card.",
    )
    summary = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short description shown in cards and search results.",
    )
    content = models.TextField(help_text="Article body in Markdown.")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    extra_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="secondary_articles",
        help_text="Additional categories; the primary one stays in `category`.",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
    )
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_articles",
    )
    page_type = models.CharField(
        max_length=16,
        choices=PageType.choices,
        default=PageType.ARTICLE,
        db_index=True,
    )
    is_stub = models.BooleanField(
        default=False,
        help_text="Short article that explicitly asks for expansion.",
    )
    protection = models.CharField(
        max_length=12,
        choices=Protection.choices,
        default=Protection.OPEN,
    )
    infobox = models.JSONField(
        default=dict,
        blank=True,
        validators=[validate_infobox],
        help_text="Side panel rows. See apps/articles/infobox.py for the schema.",
    )
    lead_image_url = models.URLField(max_length=500, blank=True)
    lead_image_alt = models.CharField(max_length=200, blank=True)
    lead_image_caption = models.CharField(max_length=300, blank=True)
    lead_image_credit = models.CharField(
        max_length=200,
        blank=True,
        help_text="Attribution line. Rendered whenever it is non-empty.",
    )
    lead_image_license = models.CharField(max_length=80, blank=True)
    lead_image_source_url = models.URLField(max_length=500, blank=True)
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_articles",
    )
    view_count = models.PositiveIntegerField(default=0)
    byte_size = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="UTF-8 bytes of `content`, not characters.",
    )
    word_count = models.PositiveIntegerField(default=0, editable=False)
    revision_total = models.PositiveIntegerField(default=0, editable=False)
    contributor_total = models.PositiveIntegerField(default=0, editable=False)
    watcher_total = models.PositiveIntegerField(default=0, editable=False)
    backlink_total = models.PositiveIntegerField(default=0, editable=False)
    #: Weighted tsvector (title=A, short_description + summary=B, content=C).
    #  Maintained by a PostgreSQL BEFORE INSERT OR UPDATE trigger installed in
    #  articles/migrations/0004_search_infrastructure.py -- NOT by Python, so
    #  bulk_create, queryset.update(), the admin and raw SQL cannot bypass it.
    #  Always NULL on SQLite; see ArticleQuerySet.search() for that path.
    search_vector = SearchVectorField(null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["-updated_at"]),
            models.Index(fields=["-view_count"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["is_published", "-updated_at"], name="article_pub_updated"),
            models.Index(fields=["page_type", "-updated_at"], name="article_type_updated"),
            # Degrades to a plain btree index on SQLite: the schema editor
            # template there has no USING clause, so the model state and the
            # migration graph stay identical on both backends.
            GinIndex(fields=["search_vector"], name="article_search_gin"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(deleted_at__isnull=True) | models.Q(is_deleted=True),
                name="article_deleted_at_requires_flag",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            unique_slugify(self, self.title, max_length=220)
        self.byte_size = len((self.content or "").encode("utf-8"))
        self.word_count = count_words(self.content or "")
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = {*update_fields, "byte_size", "word_count"}
        super().save(*args, **kwargs)

    @property
    def read_time(self) -> int:
        """Estimated reading time in minutes (~200 wpm).

        Reads ``word_count``, never ``content`` — that is what lets every list
        endpoint defer the body.
        """
        return max(1, math.ceil((self.word_count or 1) / 200))

    @property
    def revision_count(self) -> int:
        """Number of revisions.

        Prefers the denormalised counter and falls back to a live ``COUNT`` when
        it has not been populated yet, so a fresh row never renders a wrong 0.
        """
        if self.revision_total:
            return self.revision_total
        return self.revisions.count()

    @property
    def is_disambiguation(self) -> bool:
        """``page_type`` is the single source of truth; this is the shorthand."""
        return self.page_type == self.PageType.DISAMBIGUATION

    def category_names(self) -> list[str]:
        """Category names with the primary one first, for the footer bar."""
        names = [self.category.name] if self.category_id else []
        names += [
            category.name
            for category in self.extra_categories.all()
            if category.pk != self.category_id
        ]
        return names

    def recount(self, *, save: bool = True) -> dict[str, int]:
        """Re-derive every denormalised counter from the database.

        This method *is* the definition of each counter; the incremental write
        paths and ``manage.py rebuild_counts`` must agree with it.
        """
        totals = {
            "revision_total": self.revisions.count(),
            "contributor_total": (
                self.revisions.exclude(editor__isnull=True).values("editor_id").distinct().count()
            ),
            "watcher_total": self.watchers.count(),
            "backlink_total": (
                ArticleLink.objects.filter(to_article=self)
                .exclude(from_article=self)
                .values("from_article_id")
                .distinct()
                .count()
            ),
        }
        for field, value in totals.items():
            setattr(self, field, value)
        if save and self.pk is not None:
            # update_fields keeps auto_now off the wire: recounting a counter
            # must not reorder the whole encyclopedia by updated_at.
            super().save(update_fields=list(totals))
        return totals

    def soft_delete(self, *, by=None) -> None:
        """Hide the article without destroying other contributors' history."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = by
        super().save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])

    def restore(self) -> None:
        """Undo :meth:`soft_delete`. Staff only, enforced in the view."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        super().save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])


class Reference(models.Model):
    """A structured citation belonging to one article.

    ``key`` matches a ``[^key]`` footnote marker in ``Article.content``, which
    is what fixes the citation's *position*; this row holds its *data*.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="references")
    key = models.SlugField(max_length=60, help_text="Short slug used by the [^key] marker.")
    order = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=600, blank=True)
    authors = models.CharField(max_length=300, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    published_on = models.CharField(
        max_length=40,
        blank=True,
        help_text="Free text: '1986', 'March 2019', 'n.d.'. Sources are irregular.",
    )
    accessed_on = models.DateField(null=True, blank=True)
    identifier = models.CharField(
        max_length=120,
        blank=True,
        help_text="One field for ISBN / DOI / arXiv / ISSN; the renderer prefix-sniffs it.",
    )
    quote = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["article", "key"], name="uniq_reference_article_key")
        ]
        indexes = [models.Index(fields=["article", "order"], name="reference_article_order")]

    def __str__(self) -> str:
        return f"[{self.key}] {self.title[:60]}"

    def as_dict(self) -> dict:
        """Canonical wire + history-snapshot shape.

        ``ReferenceSerializer`` emits exactly this and
        ``Revision.apparatus["references"]`` stores exactly this, so history is
        replayable with one shape rather than two.
        """
        return {
            "key": self.key,
            "order": self.order,
            "title": self.title,
            "url": self.url,
            "authors": self.authors,
            "publisher": self.publisher,
            "published_on": self.published_on,
            "accessed_on": self.accessed_on.isoformat() if self.accessed_on else None,
            "identifier": self.identifier,
            "quote": self.quote,
        }


class Redirect(models.Model):
    """A slug that resolves to another article. ``/wiki/js`` -> ``/wiki/javascript``.

    Resolution returns **200**, not 301: the SPA has to be told it was
    redirected so it can render the "(Redirected from X)" line, and a 301 can
    only carry the slug, never the original *title*.
    """

    from_slug = models.SlugField(max_length=220, unique=True)
    from_title = models.CharField(
        max_length=200,
        help_text="Display title, for the '(Redirected from X)' line.",
    )
    target = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="redirects")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_redirects",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["from_slug"]
        indexes = [models.Index(fields=["target"], name="redirect_target_idx")]

    def __str__(self) -> str:
        return f"{self.from_slug} -> {self.target_id}"

    def save(self, *args, **kwargs) -> None:
        if not self.from_slug and self.from_title:
            self.from_slug = wiki_slug(self.from_title)[:220]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        """Reject reserved, shadowing and chained redirects.

        Three ways a redirect can be born useless, none of which SQL can
        express: it can take a reserved slug, it can shadow a real article (the
        article always wins, so the row is unreachable), or it can point at a
        slug that is itself only a redirect (a chain the resolver will not
        follow). Mirrored in ``RedirectSerializer`` and in the seed validator.
        """
        super().clean()
        errors: dict[str, str] = {}
        slug = (self.from_slug or "").strip().lower()
        if not slug and self.from_title:
            slug = wiki_slug(self.from_title)
        if not slug:
            errors["from_slug"] = "A redirect needs a source slug."
        elif slug in RESERVED_SLUGS:
            errors["from_slug"] = f"'{slug}' is a reserved slug and would be unreachable."
        elif Article.objects.filter(slug=slug).exists():
            errors["from_slug"] = (
                f"An article already uses the slug '{slug}'; the article would always win."
            )
        if self.target_id and slug and slug == getattr(self.target, "slug", None):
            errors["from_slug"] = "A redirect cannot point at itself."
        if (
            self.target_id
            and Redirect.objects.filter(from_slug=getattr(self.target, "slug", ""))
            .exclude(pk=self.pk)
            .exists()
        ):
            errors["target"] = (
                "That target is itself a redirect source; redirect chains are not followed."
            )
        if errors:
            raise ValidationError(errors)


class ArticleLink(models.Model):
    """An internal ``[[wikilink]]`` extracted from an article body.

    ``to_title``/``to_slug`` are recorded even when no article matches, because
    that is what paints the link red and what ranks the "most wanted pages"
    report. ``to_article`` is filled in when the target exists and is what
    "what links here" joins on; it is attached automatically the moment a
    matching article is created (:meth:`attach_target`).
    """

    from_article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="outgoing_links",
    )
    to_article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_links",
    )
    to_slug = models.SlugField(max_length=220)
    to_title = models.CharField(max_length=200)
    occurrences = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["to_title"]
        constraints = [
            models.UniqueConstraint(
                fields=["from_article", "to_slug"], name="uniq_articlelink_from_to"
            )
        ]
        indexes = [
            models.Index(fields=["to_slug"], name="articlelink_to_slug"),
            models.Index(fields=["to_article"], name="articlelink_to_article"),
        ]

    def __str__(self) -> str:
        return f"{self.from_article_id} -> {self.to_slug}"

    @property
    def is_red(self) -> bool:
        """True when the target does not exist yet."""
        return self.to_article_id is None

    @classmethod
    def link_targets(cls, article: Article) -> dict[str, tuple[str, int]]:
        """``{slug: (title, occurrences)}`` for every link in ``article``.

        Infobox row values are scanned as well as the body, so a
        ``[[Jan Ingenhousz]]`` inside the side panel counts as a link.
        """
        found: dict[str, tuple[str, int]] = {}
        for title, _display in extract_wikilinks(article.content or ""):
            cls._tally(found, title)
        infobox = article.infobox if isinstance(article.infobox, dict) else {}
        for row in infobox.get("rows") or []:
            if not isinstance(row, dict):
                continue
            for title, _display in extract_wikilinks(str(row.get("value") or "")):
                cls._tally(found, title)
        return found

    @staticmethod
    def _tally(found: dict[str, tuple[str, int]], title: str) -> None:
        slug = wiki_slug(title)[:220]
        if not slug:
            return
        label, count = found.get(slug, (title, 0))
        found[slug] = (label, count + 1)

    @classmethod
    def rebuild_for(cls, article: Article) -> int:
        """Replace ``article``'s outgoing links. Returns how many were stored.

        Call inside the same transaction as the revision snapshot.
        """
        found = cls.link_targets(article)
        resolved = dict(
            Article.objects.filter(slug__in=found).values_list("slug", "pk") if found else []
        )
        with transaction.atomic():
            stale = set(
                cls.objects.filter(from_article=article)
                .exclude(to_article__isnull=True)
                .values_list("to_article_id", flat=True)
            )
            cls.objects.filter(from_article=article).delete()
            cls.objects.bulk_create(
                [
                    cls(
                        from_article=article,
                        to_article_id=resolved.get(slug),
                        to_slug=slug,
                        to_title=title,
                        occurrences=min(count, 32767),
                    )
                    for slug, (title, count) in found.items()
                ]
            )
            cls.refresh_backlink_totals(stale | set(resolved.values()))
        return len(found)

    @classmethod
    def attach_target(cls, article: Article) -> int:
        """Resolve red links that were waiting for ``article`` to exist."""
        updated = cls.objects.filter(to_slug=article.slug, to_article__isnull=True).update(
            to_article=article
        )
        if updated:
            cls.refresh_backlink_totals([article.pk])
        return updated

    @classmethod
    def refresh_backlink_totals(cls, article_ids) -> None:
        """Recompute ``Article.backlink_total`` for the given articles."""
        ids = {pk for pk in article_ids if pk}
        if not ids:
            return
        counts = dict(
            cls.objects.filter(to_article_id__in=ids)
            .exclude(from_article_id=models.F("to_article_id"))
            .values_list("to_article_id")
            .annotate(total=Count("from_article_id", distinct=True))
        )
        articles = list(Article.objects.filter(pk__in=ids).only("id", "backlink_total"))
        for article in articles:
            article.backlink_total = counts.get(article.pk, 0)
        if articles:
            Article.objects.bulk_update(articles, ["backlink_total"], batch_size=200)


class Revision(models.Model):
    """An immutable snapshot of an article at a point in time.

    A new revision is recorded every time an article is created or edited,
    giving the encyclopedia a full, browsable edit history.

    ``created_at`` is ``default=timezone.now`` rather than ``auto_now_add``
    because the seed writes backdated history. That also means timestamps are
    writable, so this is not an audit-grade trail.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="revisions")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="revisions",
    )
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    comment = models.CharField(
        max_length=255,
        blank=True,
        help_text="Edit summary describing what changed.",
    )
    byte_size = models.PositiveIntegerField(default=0)
    byte_delta = models.IntegerField(
        default=0,
        help_text="Bytes added or removed relative to the parent revision.",
    )
    is_minor = models.BooleanField(default=False, help_text="The 'm' flag in Recent changes.")
    is_page_creation = models.BooleanField(
        default=False,
        help_text="The 'N' flag in Recent changes.",
    )
    is_bot = models.BooleanField(default=False, help_text="The 'b' flag in Recent changes.")
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Short machine strings: 'seed', 'revert', 'api', 'import'. Never user text.",
    )
    apparatus = models.JSONField(
        default=dict,
        blank=True,
        help_text="Snapshot of what is not a plain column: references, infobox, page_type…",
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = RevisionQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["article", "-created_at"]),
            # A global newest-first scan: the composite index above cannot
            # serve it, and this is what makes Recent changes one index scan.
            models.Index(fields=["-created_at"], name="revision_recent"),
            models.Index(fields=["editor", "-created_at"], name="revision_editor_recent"),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.created_at:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs) -> None:
        self.byte_size = len((self.content or "").encode("utf-8"))
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = {*update_fields, "byte_size"}
        super().save(*args, **kwargs)


class TalkThread(models.Model):
    """One discussion topic on an article's talk page."""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="talk_threads")
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="talk_threads",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    message_count = models.PositiveIntegerField(default=0, editable=False)
    participant_count = models.PositiveIntegerField(default=0, editable=False)
    is_resolved = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-last_message_at", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["article", "title"], name="uniq_talkthread_article_title"
            )
        ]
        indexes = [
            models.Index(fields=["article", "-last_message_at"], name="talkthread_article_recent")
        ]

    def __str__(self) -> str:
        return f"{self.article_id}: {self.title}"

    def touch(self, *, save: bool = True) -> dict:
        """Re-derive ``message_count``, ``participant_count`` and
        ``last_message_at`` from the non-deleted messages.

        The thread list renders "Latest comment: 4 years ago · 12 comments", so
        a ``Count`` + ``Max`` per row would be an N+1 on a paginated list. Call
        this from every message create/edit/delete path.
        """
        aggregate = self.messages.filter(is_deleted=False).aggregate(
            total=Count("id"),
            participants=Count("author_id", distinct=True),
            latest=Max("created_at"),
        )
        self.message_count = aggregate["total"] or 0
        self.participant_count = aggregate["participants"] or 0
        self.last_message_at = aggregate["latest"]
        if save and self.pk is not None:
            self.save(
                update_fields=[
                    "message_count",
                    "participant_count",
                    "last_message_at",
                    "updated_at",
                ]
            )
        return aggregate


class TalkMessage(models.Model):
    """A comment in a thread. Nesting is capped; deletion is soft.

    Soft delete keeps the node: blanking ``body`` would destroy the audit trail
    and deleting the row would orphan every reply. The **serializer** decides
    what a given caller may see.
    """

    MAX_DEPTH = 4

    thread = models.ForeignKey(TalkThread, on_delete=models.CASCADE, related_name="messages")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="talk_messages",
    )
    body = models.TextField(max_length=8000)
    depth = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_talk_messages",
    )

    class Meta:
        ordering = ["created_at", "id"]
        indexes = [
            models.Index(fields=["thread", "created_at"], name="talkmessage_thread_time"),
            models.Index(fields=["author", "-created_at"], name="talkmessage_author_time"),
            models.Index(fields=["-created_at"], name="talkmessage_recent"),
        ]
        constraints = [
            # Hardcoded 4, not MAX_DEPTH: referencing the constant would make
            # makemigrations emit a diff every time the constant moves.
            models.CheckConstraint(condition=models.Q(depth__lte=4), name="talkmessage_depth_cap"),
        ]

    def __str__(self) -> str:
        who = self.author_id or "anonymous"
        return f"{who} in thread {self.thread_id} @ {self.created_at:%Y-%m-%d %H:%M}"

    def soft_delete(self, *, by=None) -> None:
        """Hide the body while keeping the node and its replies."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = by
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])


class Watch(models.Model):
    """A user's interest in an article. The watchlist feed is derived, not stored.

    Watching is a private preference, not a change to the wiki, so it never
    appears in any feed.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watches",
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="watchers")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "article"], name="uniq_watch_user_article")
        ]
        indexes = [models.Index(fields=["user", "-created_at"], name="watch_user_recent")]

    def __str__(self) -> str:
        return f"{self.user_id} watches {self.article_id}"


class MainPageBlock(models.Model):
    """Editorial content for the front page.

    "In the news" deliberately does not exist: a fabricated news feed on an
    encyclopedia demo reads as fake and would be stale the day after it ships.
    """

    class Kind(models.TextChoices):
        FEATURED = "featured", "Featured article"
        DYK = "dyk", "Did you know…"
        OTD = "otd", "On this day"

    kind = models.CharField(max_length=12, choices=Kind.choices, db_index=True)
    position = models.PositiveSmallIntegerField(default=0, help_text="Ordering within kind.")
    body_markdown = models.TextField(blank=True, help_text="Used by 'dyk' and 'otd'.")
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="main_page_blocks",
        help_text="Required for 'featured'.",
    )
    event_year = models.IntegerField(null=True, blank=True)
    event_month = models.PositiveSmallIntegerField(null=True, blank=True)
    event_day = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["kind", "position", "id"]
        indexes = [models.Index(fields=["kind", "position"], name="mainpageblock_kind_pos")]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(event_month__isnull=True)
                | models.Q(event_month__gte=1, event_month__lte=12),
                name="mainpageblock_month_range",
            ),
            models.CheckConstraint(
                condition=models.Q(event_day__isnull=True)
                | models.Q(event_day__gte=1, event_day__lte=31),
                name="mainpageblock_day_range",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.get_kind_display()} #{self.position}"

    def clean(self) -> None:
        """A featured block needs an article; dyk/otd need a body."""
        super().clean()
        errors: dict[str, str] = {}
        if self.kind == self.Kind.FEATURED and self.article_id is None:
            errors["article"] = "A featured block must point at an article."
        if self.kind in {self.Kind.DYK, self.Kind.OTD} and not (self.body_markdown or "").strip():
            errors["body_markdown"] = f"A '{self.kind}' block needs body text."
        if errors:
            raise ValidationError(errors)
