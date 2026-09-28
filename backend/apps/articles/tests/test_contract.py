"""The article API's wire contract: shapes, paths and page sizes.

Paths are written out literally rather than reversed, because the paths are
themselves part of the contract (DECISIONS §2, §14, §17).
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.articles.models import (
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

pytestmark = pytest.mark.django_db

LIST_FIELDS = [
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
]

DETAIL_FIELDS = LIST_FIELDS + [
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
]

REVISION_FIELDS = [
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
]

INFO_FIELDS = {
    "slug",
    "title",
    "byte_size",
    "word_count",
    "read_time",
    "revision_count",
    "contributor_count",
    "watcher_count",
    "backlink_count",
    "redirect_count",
    "talk_thread_count",
    "reference_count",
    "outgoing_link_count",
    "red_link_count",
    "view_count",
    "page_type",
    "protection",
    "is_stub",
    "is_published",
    "author",
    "last_editor",
    "created_at",
    "updated_at",
}

STATS_FIELDS = {
    "articles",
    "categories",
    "contributors",
    "total_views",
    "revisions",
    "talk_messages",
    "words",
    "stubs",
}


def create_via_api(client, title: str, content: str, **extra) -> dict:
    response = client.post(
        "/api/articles/", {"title": title, "content": content, **extra}, format="json"
    )
    assert response.status_code == 201, response.data
    return response.data


def bulk_revisions(article: Article, editor, count: int) -> list[Revision]:
    base = timezone.now() - timedelta(days=1)
    return Revision.objects.bulk_create(
        [
            Revision(
                article=article,
                editor=editor,
                title=article.title,
                content=f"v{index}",
                comment=f"edit {index}",
                created_at=base + timedelta(seconds=index),
            )
            for index in range(count)
        ]
    )


# --------------------------------------------------------------------------- #
# List and detail
# --------------------------------------------------------------------------- #
def test_list_row_shape_never_carries_the_body(api_client, article):
    response = api_client.get("/api/articles/")
    row = response.data["results"][0]
    assert list(row) == LIST_FIELDS
    assert "content" not in row and "infobox" not in row
    assert set(row["author"]) == {"id", "username", "avatar"}
    assert row["category"]["slug"] == "programming"


def test_list_page_size_is_20(api_client, user):
    Article.objects.bulk_create(
        [
            Article(title=f"Page {index:02d}", slug=f"page-{index:02d}", content="x")
            for index in range(25)
        ]
    )
    first = api_client.get("/api/articles/")
    assert first.data["count"] == 25
    assert len(first.data["results"]) == 20
    assert len(api_client.get("/api/articles/", {"page": 2}).data["results"]) == 5
    assert len(api_client.get("/api/articles/", {"page_size": 7}).data["results"]) == 7


def test_detail_shape(api_client, article):
    response = api_client.get(f"/api/articles/{article.slug}/")
    assert response.status_code == 200
    assert list(response.data) == DETAIL_FIELDS
    assert response.data["redirected_from"] is None
    assert response.data["is_watched"] is False


def test_unknown_article_is_404(api_client):
    assert api_client.get("/api/articles/no-such-page/").status_code == 404


def test_categories_list_primary_first_without_duplicates(api_client, article, category):
    zoology = Category.objects.create(name="Zoology", color="#111111", order=0)
    astronomy = Category.objects.create(name="Astronomy", color="#222222", order=5)
    # The primary also appears among the extras; it must not be listed twice.
    article.extra_categories.set([astronomy, zoology, category])
    response = api_client.get(f"/api/articles/{article.slug}/")
    slugs = [row["slug"] for row in response.data["categories"]]
    assert slugs[0] == "programming"
    assert sorted(slugs[1:]) == ["astronomy", "zoology"]
    assert len(slugs) == 3
    assert set(response.data["categories"][0]) == {"slug", "name", "color"}


def test_categories_without_a_primary(api_client, user):
    article = Article.objects.create(title="Loose", content="x", author=user)
    extra = Category.objects.create(name="Extra")
    article.extra_categories.add(extra)
    response = api_client.get(f"/api/articles/{article.slug}/")
    assert [row["slug"] for row in response.data["categories"]] == ["extra"]


def test_create_accepts_extra_categories_by_slug(auth_client, category):
    extra = Category.objects.create(name="History of science")
    data = create_via_api(
        auth_client,
        "Scientific method",
        "Body.",
        category=category.slug,
        extra_categories=[extra.slug],
    )
    assert [row["slug"] for row in data["categories"]] == ["programming", "history-of-science"]


def test_create_response_is_the_detail_shape(auth_client):
    data = create_via_api(auth_client, "Fresh page", "Body text here.", comment="first")
    assert list(data) == DETAIL_FIELDS
    assert data["revision_count"] == 1
    assert data["latest_revision"]["comment"] == "first"
    assert set(data["latest_revision"]) == {
        "id",
        "editor",
        "comment",
        "byte_delta",
        "is_minor",
        "created_at",
    }


def test_slug_is_read_only(auth_client, article):
    response = auth_client.patch(
        f"/api/articles/{article.slug}/", {"slug": "renamed", "content": "x"}, format="json"
    )
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.slug == "django"


def test_short_title_is_rejected(auth_client):
    response = auth_client.post("/api/articles/", {"title": "ab", "content": "x"}, format="json")
    assert response.status_code == 400
    assert "title" in response.data


def test_invalid_infobox_is_rejected(auth_client):
    response = auth_client.post(
        "/api/articles/",
        {"title": "Bad box", "content": "x", "infobox": {"image": "https://x/y.png"}},
        format="json",
    )
    assert response.status_code == 400
    assert "infobox" in response.data


def test_duplicate_reference_keys_are_rejected(auth_client):
    reference = {"key": "curie1903", "title": "Nobel lecture"}
    response = auth_client.post(
        "/api/articles/",
        {"title": "Cited", "content": "x[^curie1903]", "references": [reference, reference]},
        format="json",
    )
    assert response.status_code == 400
    assert "references" in response.data


# --------------------------------------------------------------------------- #
# History
# --------------------------------------------------------------------------- #
def test_edits_create_revisions_newest_first(auth_client, other_client):
    created = create_via_api(auth_client, "History page", "One.", comment="create")
    slug = created["slug"]
    other_client.patch(
        f"/api/articles/{slug}/", {"content": "One. Two.", "comment": "grow"}, format="json"
    )
    other_client.patch(
        f"/api/articles/{slug}/",
        {"content": "One. Two!", "comment": "punctuation", "is_minor": True},
        format="json",
    )

    response = auth_client.get(f"/api/articles/{slug}/revisions/")
    assert response.data["count"] == 3
    rows = response.data["results"]
    assert list(rows[0]) == REVISION_FIELDS
    assert [row["comment"] for row in rows] == ["punctuation", "grow", "create"]
    assert rows[0]["is_minor"] is True
    assert rows[2]["is_page_creation"] is True and rows[2]["parent"] is None
    assert rows[1]["parent"] == rows[2]["id"]
    assert rows[0]["parent"] == rows[1]["id"]
    assert [row["byte_delta"] for row in rows] == [0, 5, 4]
    assert "content" not in rows[0]


def test_noop_edit_writes_no_revision(auth_client):
    created = create_via_api(auth_client, "Stable page", "Same.")
    response = auth_client.patch(
        f"/api/articles/{created['slug']}/",
        {"content": "Same.", "comment": "nothing"},
        format="json",
    )
    assert response.status_code == 200
    assert Revision.objects.filter(article__slug=created["slug"]).count() == 1


def test_revisions_page_size_is_50(api_client, article, user):
    bulk_revisions(article, user, 55)
    response = api_client.get(f"/api/articles/{article.slug}/revisions/")
    assert response.data["count"] == 55
    assert len(response.data["results"]) == 50
    assert response.data["next"] is not None


def test_revision_detail_carries_the_body(api_client, auth_client):
    created = create_via_api(auth_client, "Old versions", "First body.")
    revision = Revision.objects.get(article__slug=created["slug"])
    response = api_client.get(f"/api/articles/{created['slug']}/revisions/{revision.pk}/")
    assert response.status_code == 200
    assert list(response.data) == REVISION_FIELDS + ["content", "apparatus"]
    assert response.data["content"] == "First body."
    assert set(response.data["apparatus"]) == {
        "references",
        "infobox",
        "categories",
        "short_description",
    }


def test_revision_of_another_article_is_404(api_client, auth_client, article):
    other = create_via_api(auth_client, "Elsewhere", "x")
    foreign = Revision.objects.get(article__slug=other["slug"])
    response = api_client.get(f"/api/articles/{article.slug}/revisions/{foreign.pk}/")
    assert response.status_code == 404


def test_revert_restores_text_as_a_new_revision(auth_client):
    created = create_via_api(auth_client, "Revertible", "Original text.")
    slug = created["slug"]
    first = Revision.objects.get(article__slug=slug)
    auth_client.patch(f"/api/articles/{slug}/", {"content": "Vandalised."}, format="json")

    response = auth_client.post(
        f"/api/articles/{slug}/revert/", {"revision": first.pk}, format="json"
    )
    assert response.status_code == 200
    assert response.data["content"] == "Original text."
    newest = Revision.objects.filter(article__slug=slug).order_by("-created_at", "-id").first()
    assert newest.tags == ["revert"]
    assert Revision.objects.filter(article__slug=slug).count() == 3


def test_revert_needs_a_revision_id(auth_client, article):
    response = auth_client.post(f"/api/articles/{article.slug}/revert/", {}, format="json")
    assert response.status_code == 400
    assert "revision" in response.data


# --------------------------------------------------------------------------- #
# Page information and what links here (§17)
# --------------------------------------------------------------------------- #
def test_info_shape_and_counts(auth_client, api_client, other_user):
    created = create_via_api(
        auth_client,
        "Informative",
        "Links to [[Django]] and to [[Unwritten Thing]].[^a]",
        references=[{"key": "a", "title": "A source"}],
    )
    slug = created["slug"]
    Watch.objects.create(user=other_user, article=Article.objects.get(slug=slug))
    Article.objects.get(slug=slug).recount()

    response = api_client.get(f"/api/articles/{slug}/info/")
    assert response.status_code == 200
    assert set(response.data) == INFO_FIELDS
    assert response.data["revision_count"] == 1
    assert response.data["contributor_count"] == 1
    assert response.data["watcher_count"] == 1
    assert response.data["reference_count"] == 1
    assert response.data["outgoing_link_count"] == 2
    assert response.data["red_link_count"] == 2  # no "Django" article exists here
    assert response.data["protection"] == "open"
    assert response.data["author"]["username"] == "tester"


def test_backlinks_list_what_links_here(api_client, auth_client, article):
    create_via_api(auth_client, "Web frameworks", "[[Django]] and again [[Django|the framework]].")
    create_via_api(auth_client, "Unrelated", "No links at all.")
    response = api_client.get(f"/api/articles/{article.slug}/backlinks/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    row = response.data["results"][0]
    assert row["occurrences"] == 2
    assert row["source"]["slug"] == "web-frameworks"
    assert set(row["source"]) == {"slug", "title", "page_type", "category"}
    article.refresh_from_db()
    assert article.backlink_total == 1


def test_backlinks_hide_draft_sources_and_self_links(api_client, auth_client, article):
    draft = create_via_api(auth_client, "Draft linker", "[[Django]]", is_published=False)
    Article.objects.filter(pk=article.pk).update(content="Self link: [[Django]].")
    ArticleLink.rebuild_for(Article.objects.get(pk=article.pk))
    assert ArticleLink.objects.filter(from_article__slug=draft["slug"]).exists()
    assert APIClient().get(f"/api/articles/{article.slug}/backlinks/").data["count"] == 0


# --------------------------------------------------------------------------- #
# Red links (§19)
# --------------------------------------------------------------------------- #
def test_red_links_are_recorded_with_a_null_target(auth_client, article):
    created = create_via_api(auth_client, "Linker", "See [[Nonexistent Topic]] and [[Django]].")
    links = {
        link.to_slug: link
        for link in ArticleLink.objects.filter(from_article__slug=created["slug"])
    }
    assert set(links) == {"nonexistent-topic", "django"}
    red = links["nonexistent-topic"]
    assert red.to_article_id is None
    assert red.to_title == "Nonexistent Topic"
    assert red.is_red
    assert links["django"].to_article_id == article.pk


def test_red_links_turn_blue_when_the_article_is_written(auth_client, api_client):
    create_via_api(auth_client, "Linker", "See [[Nonexistent Topic]].")
    create_via_api(auth_client, "Second linker", "Also [[Nonexistent Topic]].")
    wanted = api_client.get("/api/wanted/").data["results"]
    assert wanted == [{"title": "Nonexistent Topic", "slug": "nonexistent-topic", "incoming": 2}]

    target = create_via_api(auth_client, "Nonexistent Topic", "Now it exists.")
    assert not ArticleLink.objects.filter(to_article__isnull=True).exists()
    assert api_client.get("/api/wanted/").data["results"] == []
    assert target["backlink_count"] == 2
    backlinks = api_client.get(f"/api/articles/{target['slug']}/backlinks/").data
    assert backlinks["count"] == 2


def test_wikilinks_in_the_infobox_are_links(auth_client):
    created = create_via_api(
        auth_client,
        "Boxed",
        "Body without links.",
        infobox={"rows": [{"kind": "row", "label": "Discoverer", "value": "[[Jan Ingenhousz]]"}]},
    )
    link = ArticleLink.objects.get(from_article__slug=created["slug"])
    assert (link.to_slug, link.to_article_id) == ("jan-ingenhousz", None)


# --------------------------------------------------------------------------- #
# Redirects
# --------------------------------------------------------------------------- #
def test_redirect_resolves_with_200_and_redirected_from(api_client, article):
    Redirect.objects.create(from_slug="dj", from_title="DJ", target=article)
    response = api_client.get("/api/articles/dj/")
    assert response.status_code == 200
    assert response.data["slug"] == "django"
    assert response.data["redirected_from"] == "DJ"


def test_redirect_is_followed_by_preview(api_client, article):
    Redirect.objects.create(from_slug="dj", from_title="DJ", target=article)
    response = api_client.get("/api/articles/dj/preview/")
    assert response.status_code == 200
    assert response.data["slug"] == "django"


def test_writes_never_follow_a_redirect(auth_client, article):
    Redirect.objects.create(from_slug="dj", from_title="DJ", target=article)
    response = auth_client.patch("/api/articles/dj/", {"content": "x"}, format="json")
    assert response.status_code == 404


def test_redirect_to_a_draft_is_404_for_readers(api_client, article):
    Article.objects.filter(pk=article.pk).update(is_published=False)
    Redirect.objects.create(from_slug="dj", from_title="DJ", target=article)
    assert APIClient().get("/api/articles/dj/").status_code == 404


def test_an_article_wins_over_a_redirect_of_the_same_slug(api_client, article, user):
    other = Article.objects.create(title="DJ", content="Disc jockey.", author=user)
    Redirect.objects.create(from_slug="dj", from_title="DJ", target=article)
    assert api_client.get("/api/articles/dj/").data["slug"] == other.slug


# --------------------------------------------------------------------------- #
# Watching (§17)
# --------------------------------------------------------------------------- #
def test_watch_and_unwatch(auth_client, article):
    url = f"/api/articles/{article.slug}/watch/"
    first = auth_client.post(url)
    assert first.status_code == 201
    assert first.data == {"watching": True}
    assert auth_client.post(url).status_code == 201  # idempotent
    assert Watch.objects.filter(article=article).count() == 1

    detail = auth_client.get(f"/api/articles/{article.slug}/").data
    assert detail["is_watched"] is True
    assert detail["watcher_count"] == 1
    assert APIClient().get(f"/api/articles/{article.slug}/").data["is_watched"] is False

    assert auth_client.delete(url).status_code == 204
    assert auth_client.delete(url).status_code == 204  # idempotent
    article.refresh_from_db()
    assert article.watcher_total == 0


def test_watching_does_not_touch_history(auth_client, article):
    auth_client.post(f"/api/articles/{article.slug}/watch/")
    assert article.revisions.count() == 0


# --------------------------------------------------------------------------- #
# Main page (§5) and statistics
# --------------------------------------------------------------------------- #
def test_main_page_shape_has_no_news(api_client, article):
    response = api_client.get("/api/main-page/")
    assert response.status_code == 200
    assert set(response.data) == {"featured", "recently_featured", "dyk", "otd", "stats"}
    assert set(response.data["stats"]) == STATS_FIELDS


def test_main_page_blocks(api_client, user):
    first = Article.objects.create(
        title="Featured one", content="**Featured one** is first.", author=user
    )
    second = Article.objects.create(title="Featured two", content="x", author=user)
    hidden = Article.objects.create(title="Hidden", content="x", author=user, is_published=False)
    MainPageBlock.objects.create(kind="featured", position=0, article=first)
    MainPageBlock.objects.create(kind="featured", position=1, article=hidden)
    MainPageBlock.objects.create(kind="featured", position=2, article=second)
    MainPageBlock.objects.create(kind="dyk", position=1, body_markdown="…that B?")
    MainPageBlock.objects.create(kind="dyk", position=0, body_markdown="…that A?")
    MainPageBlock.objects.create(kind="dyk", position=2, body_markdown="…retired", is_active=False)
    MainPageBlock.objects.create(
        kind="otd",
        position=0,
        body_markdown="Something happened.",
        event_year=1903,
        event_month=12,
        event_day=10,
    )

    data = api_client.get("/api/main-page/").data
    assert data["featured"]["slug"] == "featured-one"
    assert data["featured"]["extract"] == "Featured one is first."
    assert set(data["featured"]) == {
        "slug",
        "title",
        "page_type",
        "category",
        "short_description",
        "summary",
        "lead_image_url",
        "lead_image_alt",
        "extract",
    }
    assert [row["slug"] for row in data["recently_featured"]] == ["featured-two"]
    assert data["dyk"] == ["…that A?", "…that B?"]
    assert data["otd"] == [{"year": 1903, "month": 12, "day": 10, "body": "Something happened."}]


def test_main_page_falls_back_to_the_most_viewed_article(api_client, user):
    Article.objects.create(title="Quiet", content="x", author=user, view_count=3)
    Article.objects.create(title="Much read", content="x", author=user, view_count=300)
    data = api_client.get("/api/main-page/").data
    assert data["featured"]["slug"] == "much-read"
    assert data["recently_featured"] == []


def test_main_page_on_an_empty_wiki(api_client, db):
    data = api_client.get("/api/main-page/").data
    assert data["featured"] is None
    assert data["dyk"] == [] and data["otd"] == []


def test_stats_count_only_readable_content(api_client, user, other_user, category):
    Article.objects.create(title="Live", content="one two three", author=user, category=category)
    Article.objects.create(
        title="Stubby", content="four", author=other_user, is_stub=True, view_count=10
    )
    Article.objects.create(title="Draft", content="x", author=user, is_published=False)
    gone = Article.objects.create(title="Gone", content="x", author=user)
    gone.soft_delete(by=user)
    thread = TalkThread.objects.create(article=gone, title="t")
    TalkMessage.objects.create(thread=thread, author=user, body="kept")
    TalkMessage.objects.create(thread=thread, author=user, body="removed", is_deleted=True)

    for url in ("/api/stats/", "/api/articles/stats/"):
        data = api_client.get(url).data
        assert set(data) == STATS_FIELDS
        assert data["articles"] == 2
        assert data["contributors"] == 2
        assert data["stubs"] == 1
        assert data["words"] == 4
        assert data["total_views"] == 10
        assert data["categories"] == 1
        assert data["talk_messages"] == 1


# --------------------------------------------------------------------------- #
# Categories
# --------------------------------------------------------------------------- #
def test_category_listing_page_size_is_50_and_includes_secondary(api_client, category):
    Article.objects.bulk_create(
        [
            Article(
                title=f"Entry {index:02d}",
                slug=f"entry-{index:02d}",
                content="x",
                category=category,
            )
            for index in range(54)
        ]
    )
    secondary = Article.objects.create(title="Secondary member", content="x")
    secondary.extra_categories.add(category)

    response = api_client.get(f"/api/categories/{category.slug}/articles/")
    assert response.status_code == 200
    assert response.data["count"] == 55
    assert len(response.data["results"]) == 50
    page_two = api_client.get(f"/api/categories/{category.slug}/articles/", {"page": 2})
    assert "secondary-member" in {row["slug"] for row in page_two.data["results"]}


def test_category_article_count_ignores_drafts(api_client, category, user):
    Article.objects.create(title="Counted", content="x", category=category, author=user)
    Article.objects.create(
        title="Not counted", content="x", category=category, author=user, is_published=False
    )
    rows = {row["slug"]: row for row in api_client.get("/api/categories/").data}
    assert rows["programming"]["article_count"] == 1
