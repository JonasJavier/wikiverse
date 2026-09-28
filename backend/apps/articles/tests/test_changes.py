"""Change feeds: ``/api/changes/`` (DECISIONS §4), ``/api/watchlist/``,
``/api/users/{username}/contributions/`` (§17) and the RSS feed (§14).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import timedelta
from urllib.parse import parse_qs, urlsplit

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.articles.models import Article, Category, Revision, TalkMessage, TalkThread, Watch

pytestmark = pytest.mark.django_db

CHANGES_URL = "/api/changes/"

#: DECISIONS §4, in order.
ROW_FIELDS = [
    "kind",
    "id",
    "parent_id",
    "timestamp",
    "article",
    "user",
    "comment",
    "byte_size",
    "byte_delta",
    "is_minor",
    "is_page_creation",
    "is_bot",
    "is_current",
    "tags",
    "thread",
]


def revision(article, editor, *, at, content, parent=None, **fields) -> Revision:
    previous = parent.byte_size if parent else 0
    return Revision.objects.create(
        article=article,
        editor=editor,
        parent=parent,
        title=article.title,
        content=content,
        created_at=at,
        byte_delta=len(content.encode()) - previous,
        **fields,
    )


@pytest.fixture
def feed(db, user, other_user, category):
    """Two articles, four edits (one minor bot edit) and two talk posts.

    Timeline, newest first: m2 (-10m), r4 (-30m), r3 (-60m), m1 (-90m),
    r2 (-120m, minor, bot), r1 (-180m, page creation).
    """
    now = timezone.now()
    bot = User.objects.create_user("sweeper", "sweeper@example.com", "x", is_bot=True)
    science = Category.objects.create(name="Science", color="#123456")
    alpha = Article.objects.create(title="Alpha", content="a", category=category, author=user)
    beta = Article.objects.create(title="Beta", content="b", category=science, author=user)

    r1 = revision(
        alpha, user, at=now - timedelta(minutes=180), content="first", is_page_creation=True
    )
    r2 = revision(
        alpha,
        bot,
        at=now - timedelta(minutes=120),
        content="first.",
        parent=r1,
        is_minor=True,
        is_bot=True,
        tags=["bot"],
    )
    r3 = revision(
        alpha, other_user, at=now - timedelta(minutes=60), content="first. more", parent=r2
    )
    r4 = revision(beta, user, at=now - timedelta(minutes=30), content="beta", is_page_creation=True)

    thread = TalkThread.objects.create(
        article=alpha, title="Lead is too technical", created_by=other_user
    )
    m1 = TalkMessage.objects.create(
        thread=thread, author=other_user, body="Opening.", created_at=now - timedelta(minutes=90)
    )
    m2 = TalkMessage.objects.create(
        thread=thread,
        author=user,
        parent=m1,
        depth=1,
        body="Reply.",
        created_at=now - timedelta(minutes=10),
    )
    thread.touch()
    return {
        "now": now,
        "bot": bot,
        "alpha": alpha,
        "beta": beta,
        "science": science,
        "revisions": (r1, r2, r3, r4),
        "thread": thread,
        "messages": (m1, m2),
    }


def keys(rows) -> list[str]:
    return [f"{row['kind']}-{row['id']}" for row in rows]


# --------------------------------------------------------------------------- #
# Envelope and row shape
# --------------------------------------------------------------------------- #
def test_changes_envelope(api_client, feed):
    response = api_client.get(CHANGES_URL)
    assert response.status_code == 200
    assert set(response.data) == {"results", "next_before", "has_more"}
    assert response.data["has_more"] is False
    assert response.data["next_before"] is None


def test_changes_merge_edits_and_talk_newest_first(api_client, feed):
    r1, r2, r3, r4 = feed["revisions"]
    m1, m2 = feed["messages"]
    rows = api_client.get(CHANGES_URL).data["results"]
    assert keys(rows) == [
        f"talk-{m2.pk}",
        f"edit-{r4.pk}",
        f"edit-{r3.pk}",
        f"talk-{m1.pk}",
        f"edit-{r2.pk}",
        f"edit-{r1.pk}",
    ]
    for row in rows:
        assert list(row) == ROW_FIELDS


def test_edit_row_fields(api_client, feed, other_user):
    _r1, r2, r3, _r4 = feed["revisions"]
    rows = {row["id"]: row for row in api_client.get(CHANGES_URL, {"type": "edit"}).data["results"]}
    row = rows[r3.pk]
    assert row["kind"] == "edit"
    assert row["parent_id"] == r2.pk
    assert row["article"] == {"slug": "alpha", "title": "Alpha"}
    assert row["user"] == {"id": other_user.pk, "username": "other", "avatar": None}
    assert row["byte_size"] == len(b"first. more")
    assert row["byte_delta"] == len(b"first. more") - len(b"first.")
    assert row["thread"] is None
    assert row["is_current"] is True
    assert row["tags"] == []
    assert rows[r2.pk]["is_current"] is False
    assert rows[r2.pk]["is_minor"] is True and rows[r2.pk]["is_bot"] is True
    assert rows[r2.pk]["tags"] == ["bot"]


def test_talk_row_fields(api_client, feed, user):
    m1, m2 = feed["messages"]
    rows = {row["id"]: row for row in api_client.get(CHANGES_URL, {"type": "talk"}).data["results"]}
    reply = rows[m2.pk]
    assert reply["kind"] == "talk"
    assert reply["parent_id"] == m1.pk
    assert reply["byte_size"] is None and reply["byte_delta"] is None
    assert reply["thread"] == {"id": feed["thread"].pk, "title": "Lead is too technical"}
    assert reply["comment"] == "Lead is too technical"
    assert reply["user"]["username"] == user.username
    assert reply["is_current"] is False
    assert reply["is_page_creation"] is False
    assert rows[m1.pk]["is_page_creation"] is True  # a thread opener


def test_is_current_marks_each_articles_latest_revision_only(api_client, feed):
    _r1, _r2, r3, r4 = feed["revisions"]
    rows = api_client.get(CHANGES_URL, {"type": "edit"}).data["results"]
    assert {row["id"] for row in rows if row["is_current"]} == {r3.pk, r4.pk}


# --------------------------------------------------------------------------- #
# Filters (§4 URL -> API mapping)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(("kind", "expected"), [("edit", {"edit"}), ("talk", {"talk"})])
def test_type_filter(api_client, feed, kind, expected):
    rows = api_client.get(CHANGES_URL, {"type": kind}).data["results"]
    assert {row["kind"] for row in rows} == expected


def test_unknown_type_means_all(api_client, feed):
    rows = api_client.get(CHANGES_URL, {"type": "bogus"}).data["results"]
    assert len(rows) == 6


def test_user_filter(api_client, feed):
    _r1, _r2, r3, _r4 = feed["revisions"]
    m1, _m2 = feed["messages"]
    rows = api_client.get(CHANGES_URL, {"user": "other"}).data["results"]
    assert keys(rows) == [f"edit-{r3.pk}", f"talk-{m1.pk}"]


def test_minor_zero_hides_minor_edits(api_client, feed):
    _r1, r2, _r3, _r4 = feed["revisions"]
    rows = api_client.get(CHANGES_URL, {"minor": "0"}).data["results"]
    assert f"edit-{r2.pk}" not in keys(rows)
    assert len(rows) == 5


def test_bots_zero_hides_bot_edits_and_bot_talk(api_client, feed):
    _r1, r2, _r3, _r4 = feed["revisions"]
    TalkMessage.objects.create(thread=feed["thread"], author=feed["bot"], body="Bot note.")
    everything = api_client.get(CHANGES_URL).data["results"]
    assert len(everything) == 7
    rows = api_client.get(CHANGES_URL, {"bots": "0"}).data["results"]
    assert f"edit-{r2.pk}" not in keys(rows)
    assert all(not row["is_bot"] for row in rows)
    assert len(rows) == 5


def test_since_filter(api_client, feed):
    since = (feed["now"] - timedelta(minutes=45)).isoformat()
    rows = api_client.get(CHANGES_URL, {"since": since}).data["results"]
    assert len(rows) == 2  # m2 and r4


def test_days_filter(api_client, feed, user):
    old = revision(feed["beta"], user, at=feed["now"] - timedelta(days=20), content="ancient")
    everything = keys(api_client.get(CHANGES_URL).data["results"])
    assert f"edit-{old.pk}" in everything
    recent = keys(api_client.get(CHANGES_URL, {"days": 7}).data["results"])
    assert f"edit-{old.pk}" not in recent


def test_category_filter(api_client, feed):
    _r1, _r2, _r3, r4 = feed["revisions"]
    rows = api_client.get(CHANGES_URL, {"category": "science"}).data["results"]
    assert keys(rows) == [f"edit-{r4.pk}"]


def test_article_filter(api_client, feed):
    rows = api_client.get(CHANGES_URL, {"article": "beta"}).data["results"]
    assert {row["article"]["slug"] for row in rows} == {"beta"}


# --------------------------------------------------------------------------- #
# Cursor pagination
# --------------------------------------------------------------------------- #
def test_limit_and_before_cursor_walk_the_whole_feed(api_client, feed):
    expected = keys(api_client.get(CHANGES_URL).data["results"])
    seen: list[str] = []
    params = {"limit": 2}
    for _page in range(10):
        data = api_client.get(CHANGES_URL, params).data
        assert len(data["results"]) <= 2
        seen += keys(data["results"])
        if not data["has_more"]:
            assert data["next_before"] is None
            break
        assert data["next_before"] == data["results"][-1]["timestamp"]
        params = {"limit": 2, "before": data["next_before"]}
    assert seen == expected


def test_default_limit_is_50_and_capped_at_100(api_client, article, user):
    base = timezone.now() - timedelta(hours=5)
    Revision.objects.bulk_create(
        [
            Revision(
                article=article,
                editor=user,
                title="Django",
                content=str(index),
                created_at=base + timedelta(seconds=index),
            )
            for index in range(120)
        ]
    )
    default = api_client.get(CHANGES_URL).data
    assert len(default["results"]) == 50
    assert default["has_more"] is True
    capped = api_client.get(CHANGES_URL, {"limit": 500}).data
    assert len(capped["results"]) == 100
    assert capped["has_more"] is True


def test_has_more_counts_both_sides(api_client, feed):
    # limit + 1 from *each* side: with limit=5 there are 6 rows in total.
    data = api_client.get(CHANGES_URL, {"limit": 5}).data
    assert len(data["results"]) == 5
    assert data["has_more"] is True


# --------------------------------------------------------------------------- #
# Visibility
# --------------------------------------------------------------------------- #
def test_draft_changes_are_hidden_from_other_readers(api_client, feed, user):
    Article.objects.filter(pk=feed["alpha"].pk).update(is_published=False)
    anonymous = APIClient().get(CHANGES_URL).data["results"]
    assert {row["article"]["slug"] for row in anonymous} == {"beta"}

    author = APIClient()
    author.force_authenticate(user=user)
    own = author.get(CHANGES_URL).data["results"]
    assert {row["article"]["slug"] for row in own} == {"alpha", "beta"}


def test_deleted_article_changes_are_hidden(api_client, feed, user):
    feed["alpha"].soft_delete(by=user)
    rows = api_client.get(CHANGES_URL).data["results"]
    assert {row["article"]["slug"] for row in rows} == {"beta"}


def test_deleted_talk_messages_are_not_changes(api_client, feed):
    _m1, m2 = feed["messages"]
    m2.soft_delete()
    rows = api_client.get(CHANGES_URL, {"type": "talk"}).data["results"]
    assert f"talk-{m2.pk}" not in keys(rows)


# --------------------------------------------------------------------------- #
# Watchlist
# --------------------------------------------------------------------------- #
def test_watchlist_lists_changes_to_watched_articles(feed, other_user):
    Watch.objects.create(user=other_user, article=feed["beta"])
    client = APIClient()
    client.force_authenticate(user=other_user)
    response = client.get("/api/watchlist/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    row = response.data["results"][0]
    assert list(row) == ROW_FIELDS
    assert row["article"]["slug"] == "beta"


def test_watchlist_filters(feed, other_user):
    Watch.objects.create(user=other_user, article=feed["alpha"])
    client = APIClient()
    client.force_authenticate(user=other_user)
    assert client.get("/api/watchlist/").data["count"] == 3
    assert client.get("/api/watchlist/", {"minor": "0"}).data["count"] == 2
    assert client.get("/api/watchlist/", {"bots": "0"}).data["count"] == 2
    since = (feed["now"] - timedelta(minutes=90)).isoformat()
    assert client.get("/api/watchlist/", {"since": since}).data["count"] == 1


def test_watchlist_is_private(feed, user, other_user):
    Watch.objects.create(user=other_user, article=feed["alpha"])
    client = APIClient()
    client.force_authenticate(user=user)
    assert client.get("/api/watchlist/").data["count"] == 0


def test_watchlist_page_size_is_50(auth_client, article, user):
    Watch.objects.create(user=user, article=article)
    base = timezone.now() - timedelta(hours=1)
    Revision.objects.bulk_create(
        [
            Revision(
                article=article,
                editor=user,
                title="Django",
                content="x",
                created_at=base + timedelta(seconds=i),
            )
            for i in range(55)
        ]
    )
    data = auth_client.get("/api/watchlist/").data
    assert data["count"] == 55
    assert len(data["results"]) == 50


# --------------------------------------------------------------------------- #
# Contributions (§17)
# --------------------------------------------------------------------------- #
def test_contributions_list_one_users_edits(api_client, feed):
    r1, _r2, _r3, r4 = feed["revisions"]
    response = api_client.get("/api/users/tester/contributions/")
    assert response.status_code == 200
    assert [row["id"] for row in response.data["results"]] == [r4.pk, r1.pk]
    assert all(list(row) == ROW_FIELDS for row in response.data["results"])
    assert {row["kind"] for row in response.data["results"]} == {"edit"}


def test_contributions_of_an_unknown_user_is_404(api_client, db):
    assert api_client.get("/api/users/nobody-here/contributions/").status_code == 404


def test_contributions_hide_drafts_from_other_readers(api_client, feed):
    Article.objects.filter(pk=feed["beta"].pk).update(is_published=False)
    rows = APIClient().get("/api/users/tester/contributions/").data["results"]
    assert {row["article"]["slug"] for row in rows} == {"alpha"}


def test_contributions_minor_filter(api_client, feed):
    assert api_client.get("/api/users/sweeper/contributions/").data["count"] == 1
    assert api_client.get("/api/users/sweeper/contributions/", {"minor": "0"}).data["count"] == 0


# --------------------------------------------------------------------------- #
# RSS (§14)
# --------------------------------------------------------------------------- #
def rss_items(response) -> list[ET.Element]:
    root = ET.fromstring(response.content)
    return root.findall("./channel/item")


def test_rss_feed(api_client, feed, settings):
    settings.PUBLIC_BASE_URL = "https://wiki.example.test"
    response = api_client.get("/api/feeds/changes.rss")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/rss+xml")
    root = ET.fromstring(response.content)
    assert root.find("./channel/link").text == "https://wiki.example.test/changes"
    items = rss_items(response)
    assert len(items) == 4  # edits only
    guids = [item.find("guid").text for item in items]
    r1, r2, r3, r4 = feed["revisions"]
    assert guids == [f"wikiverse:revision:{r.pk}" for r in (r4, r3, r2, r1)]
    assert items[0].find("title").text == "Beta (+4)"


def test_rss_links_are_public_spa_urls(api_client, feed, settings):
    settings.PUBLIC_BASE_URL = "https://wiki.example.test"
    r1, r2, r3, _r4 = feed["revisions"]
    links = {
        item.find("guid").text: item.find("link").text
        for item in rss_items(api_client.get("/api/feeds/changes.rss"))
    }
    # A page creation links to the article itself.
    assert links[f"wikiverse:revision:{r1.pk}"] == "https://wiki.example.test/wiki/alpha"
    # An edit links to the SPA diff route /wiki/:slug/diff?from=<id>&to=<id> (§14),
    # with a real query string the router can read.
    link = urlsplit(links[f"wikiverse:revision:{r3.pk}"])
    assert (link.scheme, link.netloc, link.path) == (
        "https",
        "wiki.example.test",
        "/wiki/alpha/diff",
    )
    assert parse_qs(link.query) == {"from": [str(r2.pk)], "to": [str(r3.pk)]}
    assert "testserver" not in str(links)


def test_rss_hides_drafts_and_honours_limit(api_client, feed):
    Article.objects.filter(pk=feed["alpha"].pk).update(is_published=False)
    items = rss_items(api_client.get("/api/feeds/changes.rss"))
    assert len(items) == 1
    Article.objects.filter(pk=feed["alpha"].pk).update(is_published=True)
    assert len(rss_items(api_client.get("/api/feeds/changes.rss", {"limit": 2}))) == 2
