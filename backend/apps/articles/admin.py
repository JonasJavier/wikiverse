"""Admin registrations.

Every changelist that shows a related object either ``select_related``s it or
uses a raw id widget, so no page here is N+1. Article bodies and revision
bodies are the largest columns in the database and are never listed.
"""

from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import (
    Article,
    ArticleLink,
    Category,
    MainPageBlock,
    Redirect,
    Reference,
    Revision,
    TalkMessage,
    TalkThread,
    Watch,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "order", "icon", "color", "article_count")
    list_filter = ("parent",)
    list_select_related = ("parent",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    autocomplete_fields = ("parent",)
    ordering = ("order", "name")

    @admin.display(description="Articles", ordering="article_count")
    def article_count(self, obj: Category) -> int:
        return obj.article_count

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("parent")
            .annotate(article_count=Count("articles", distinct=True))
        )


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 0
    fields = ("order", "key", "title", "url", "authors", "published_on", "accessed_on")
    ordering = ("order", "id")


class RevisionInline(admin.TabularInline):
    model = Revision
    fk_name = "article"
    extra = 0
    can_delete = False
    fields = ("created_at", "editor", "title", "comment", "byte_size", "byte_delta", "is_minor")
    readonly_fields = fields
    ordering = ("-created_at",)
    raw_id_fields = ("editor",)
    show_change_link = True

    def has_add_permission(self, request, obj) -> bool:
        return False


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "page_type",
        "protection",
        "author",
        "is_published",
        "is_deleted",
        "is_stub",
        "byte_size",
        "revision_total",
        "view_count",
        "updated_at",
    )
    list_filter = (
        "is_published",
        "is_deleted",
        "page_type",
        "protection",
        "is_stub",
        "category",
        "created_at",
    )
    list_select_related = ("category", "author")
    search_fields = ("title", "slug", "short_description", "summary")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category", "author", "last_editor", "extra_categories")
    raw_id_fields = ("deleted_by",)
    readonly_fields = (
        "view_count",
        "byte_size",
        "word_count",
        "revision_total",
        "contributor_total",
        "watcher_total",
        "backlink_total",
        "created_at",
        "updated_at",
    )
    inlines = [ReferenceInline, RevisionInline]
    date_hierarchy = "created_at"
    actions = ["action_recount", "action_rebuild_links"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "short_description", "summary", "content")}),
        (
            "Classification",
            {
                "fields": (
                    "category",
                    "extra_categories",
                    "page_type",
                    "is_stub",
                    "protection",
                )
            },
        ),
        (
            "Lead image",
            {
                "fields": (
                    "lead_image_url",
                    "lead_image_alt",
                    "lead_image_caption",
                    "lead_image_credit",
                    "lead_image_license",
                    "lead_image_source_url",
                )
            },
        ),
        ("Infobox", {"fields": ("infobox",)}),
        ("People", {"fields": ("author", "last_editor")}),
        ("State", {"fields": ("is_published", "is_deleted", "deleted_at", "deleted_by")}),
        (
            "Counters",
            {
                "fields": (
                    "view_count",
                    "byte_size",
                    "word_count",
                    "revision_total",
                    "contributor_total",
                    "watcher_total",
                    "backlink_total",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_queryset(self, request):
        # Unfiltered on purpose: the admin is where a soft-deleted article is
        # found again, and hard delete lives here and nowhere else.
        return super().get_queryset(request).select_related("category", "author")

    @admin.action(description="Recount denormalised counters")
    def action_recount(self, request, queryset) -> None:
        for article in queryset:
            article.recount()
        self.message_user(request, f"Recounted {queryset.count()} article(s).")

    @admin.action(description="Rebuild extracted [[wikilinks]]")
    def action_rebuild_links(self, request, queryset) -> None:
        total = sum(ArticleLink.rebuild_for(article) for article in queryset)
        self.message_user(request, f"Stored {total} link(s).")


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("key", "article", "order", "title", "publisher", "accessed_on")
    list_filter = ("publisher",)
    list_select_related = ("article",)
    search_fields = ("key", "title", "authors", "publisher", "identifier", "article__title")
    raw_id_fields = ("article",)
    ordering = ("article", "order")


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ("from_slug", "from_title", "target", "created_by", "created_at")
    list_select_related = ("target", "created_by")
    search_fields = ("from_slug", "from_title", "target__title")
    autocomplete_fields = ("target",)
    raw_id_fields = ("created_by",)
    date_hierarchy = "created_at"


@admin.register(ArticleLink)
class ArticleLinkAdmin(admin.ModelAdmin):
    list_display = ("from_article", "to_title", "to_slug", "status", "occurrences")
    list_filter = (("to_article", admin.EmptyFieldListFilter),)
    list_select_related = ("from_article", "to_article")
    search_fields = ("to_title", "to_slug", "from_article__title")
    raw_id_fields = ("from_article", "to_article")

    @admin.display(description="Target")
    def status(self, obj: ArticleLink) -> str:
        if obj.to_article_id:
            return "resolved"
        return format_html("<b>red link</b>")


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "editor",
        "comment",
        "byte_size",
        "byte_delta",
        "is_minor",
        "is_page_creation",
        "is_bot",
        "created_at",
    )
    list_filter = ("is_minor", "is_page_creation", "is_bot", "created_at")
    list_select_related = ("article", "editor")
    search_fields = ("article__title", "comment", "editor__username")
    raw_id_fields = ("article", "editor", "parent")
    date_hierarchy = "created_at"
    readonly_fields = (
        "article",
        "parent",
        "editor",
        "title",
        "summary",
        "content",
        "byte_size",
        "byte_delta",
        "apparatus",
        "created_at",
    )


class TalkMessageInline(admin.TabularInline):
    model = TalkMessage
    extra = 0
    fields = ("created_at", "author", "parent", "depth", "body", "is_deleted")
    readonly_fields = ("created_at", "depth")
    raw_id_fields = ("author", "parent")
    ordering = ("created_at", "id")


@admin.register(TalkThread)
class TalkThreadAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "article",
        "message_count",
        "participant_count",
        "last_message_at",
        "is_resolved",
        "is_locked",
    )
    list_filter = ("is_resolved", "is_locked", "created_at")
    list_select_related = ("article", "created_by")
    search_fields = ("title", "article__title")
    autocomplete_fields = ("article",)
    raw_id_fields = ("created_by",)
    readonly_fields = ("message_count", "participant_count", "last_message_at", "updated_at")
    inlines = [TalkMessageInline]
    actions = ["action_touch"]

    @admin.action(description="Recount messages and participants")
    def action_touch(self, request, queryset) -> None:
        for thread in queryset:
            thread.touch()
        self.message_user(request, f"Recounted {queryset.count()} thread(s).")


@admin.register(TalkMessage)
class TalkMessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "author", "depth", "created_at", "edited_at", "is_deleted")
    list_filter = ("is_deleted", "depth", "created_at")
    list_select_related = ("thread", "thread__article", "author")
    search_fields = ("body", "author__username", "thread__title")
    raw_id_fields = ("thread", "parent", "author", "deleted_by")
    date_hierarchy = "created_at"


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")
    list_select_related = ("user", "article")
    search_fields = ("user__username", "article__title")
    raw_id_fields = ("user", "article")
    date_hierarchy = "created_at"


@admin.register(MainPageBlock)
class MainPageBlockAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "position",
        "article",
        "event_year",
        "event_month",
        "event_day",
        "is_active",
    )
    list_filter = ("kind", "is_active")
    list_select_related = ("article",)
    search_fields = ("body_markdown", "article__title")
    autocomplete_fields = ("article",)
    ordering = ("kind", "position")
