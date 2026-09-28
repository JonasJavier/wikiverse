"""``/api/search/`` and ``/api/search/suggest/`` (DECISIONS §2, §3, §10).

Every test here runs on both backends. SQLite takes the ``icontains`` fallback
and PostgreSQL the ``tsvector``/``pg_trgm`` path; the assertions are written
against the wire contract, which is identical on both. The few behaviours only
PostgreSQL has (``<mark>`` from ``ts_headline``, typo tolerance, the trigger)
carry a vendor guard evaluated at test time.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.db import connection
from django.utils import timezone

from apps.articles.models import Article
from apps.articles.search import safe_headline_to_marked

pytestmark = pytest.mark.django_db

SEARCH_URL = "/api/search/"
SUGGEST_URL = "/api/search/suggest/"

#: DECISIONS §2, in serializer order.
RESULT_FIELDS = [
    "slug",
    "title",
    "title_snippet",
    "snippet",
    "rank",
    "category",
    "updated_at",
    "byte_size",
    "word_count",
]

ENVELOPE_FIELDS = {"count", "next", "previous", "results", "query", "ordering", "did_you_mean"}


def is_postgres() -> bool:
    return connection.vendor == "postgresql"


def postgres_only():
    """Skip unless the test database is PostgreSQL. Evaluated at call time."""
    if not is_postgres():
        pytest.skip("PostgreSQL-only behaviour")


def sqlite_only():
    if is_postgres():
        pytest.skip("SQLite fallback path only")


def make_article(title: str, *, author=None, **fields) -> Article:
    fields.setdefault("content", f"{title} is an article used by the search tests.")
    return Article.objects.create(title=title, author=author, **fields)


def strip_marks(value: str) -> str:
    return value.replace("<mark>", "").replace("</mark>", "")


# --------------------------------------------------------------------------- #
# Wire shape
# --------------------------------------------------------------------------- #
def test_search_envelope_and_result_fields(api_client, user, category):
    make_article("Xylophone", author=user, category=category, summary="A percussion instrument.")
    response = api_client.get(SEARCH_URL, {"q": "xylophone"})
    assert response.status_code == 200
    assert set(response.data) == ENVELOPE_FIELDS
    assert response.data["query"] == "xylophone"
    assert response.data["ordering"] == "relevance"
    assert response.data["did_you_mean"] is None
    assert response.data["count"] == 1
    row = response.data["results"][0]
    assert list(row) == RESULT_FIELDS
    assert row["slug"] == "xylophone"
    assert set(row["category"]) == {"slug", "name", "color"}
    assert isinstance(row["rank"], float)


def test_blank_query_behaves_like_a_listing(api_client, user):
    make_article("Alpha", author=user)
    make_article("Beta", author=user)
    response = api_client.get(SEARCH_URL)
    assert response.status_code == 200
    assert response.data["count"] == 2
    assert response.data["query"] == ""
    assert all(row["rank"] == 0.0 for row in response.data["results"])


def test_search_page_size_is_20(api_client, user):
    for index in range(25):
        make_article(f"Zephyr study {index:02d}", author=user)
    first = api_client.get(SEARCH_URL, {"q": "zephyr"})
    assert first.data["count"] == 25
    assert len(first.data["results"]) == 20
    assert first.data["next"] is not None
    second = api_client.get(SEARCH_URL, {"q": "zephyr", "page": 2})
    assert len(second.data["results"]) == 5


def test_search_hides_drafts_and_deleted_articles(api_client, user):
    make_article("Visible quasar", author=user)
    make_article("Draft quasar", author=user, is_published=False)
    gone = make_article("Deleted quasar", author=user)
    gone.soft_delete(by=user)
    response = api_client.get(SEARCH_URL, {"q": "quasar"})
    assert [row["slug"] for row in response.data["results"]] == ["visible-quasar"]


def test_title_match_outranks_body_match(api_client, user):
    make_article(
        "Marsupials of Australia",
        author=user,
        content="Marsupials include the kangaroo and, on Rottnest Island, the quokka.",
    )
    make_article("Quokka", author=user, content="A small wallaby-like animal.")
    response = api_client.get(SEARCH_URL, {"q": "quokka"})
    slugs = [row["slug"] for row in response.data["results"]]
    assert slugs[0] == "quokka"
    assert set(slugs) == {"quokka", "marsupials-of-australia"}


# --------------------------------------------------------------------------- #
# Sorting and date filters
# --------------------------------------------------------------------------- #
@pytest.fixture
def dated_articles(user):
    now = timezone.now()
    ages = {"Nebula old": 30, "Nebula middle": 10, "Nebula new": 1}
    made = {}
    for title, days in ages.items():
        article = make_article(title, author=user)
        Article.objects.filter(pk=article.pk).update(created_at=now - timedelta(days=days))
        made[title] = article
    return now, made


@pytest.mark.parametrize(
    ("ordering", "expected"),
    [
        ("newest", ["nebula-new", "nebula-middle", "nebula-old"]),
        ("oldest", ["nebula-old", "nebula-middle", "nebula-new"]),
    ],
)
def test_search_sort_newest_and_oldest(api_client, dated_articles, ordering, expected):
    response = api_client.get(SEARCH_URL, {"q": "nebula", "ordering": ordering})
    assert response.data["ordering"] == ordering
    assert [row["slug"] for row in response.data["results"]] == expected


def test_unknown_sort_falls_back_to_relevance(api_client, dated_articles):
    # "most edited" was cut (DECISIONS §2); a stale bookmark still gets results.
    response = api_client.get(SEARCH_URL, {"q": "nebula", "ordering": "most_edited"})
    assert response.status_code == 200
    assert response.data["ordering"] == "relevance"
    assert response.data["count"] == 3


def test_created_after_and_created_before_filters(api_client, dated_articles):
    now, _made = dated_articles
    after = api_client.get(
        SEARCH_URL, {"q": "nebula", "created_after": (now - timedelta(days=15)).isoformat()}
    )
    assert {row["slug"] for row in after.data["results"]} == {"nebula-middle", "nebula-new"}

    before = api_client.get(
        SEARCH_URL, {"q": "nebula", "created_before": (now - timedelta(days=15)).isoformat()}
    )
    assert {row["slug"] for row in before.data["results"]} == {"nebula-old"}


# --------------------------------------------------------------------------- #
# did_you_mean
# --------------------------------------------------------------------------- #
def test_did_you_mean_is_null_when_there_are_results(api_client, user):
    make_article("Photosynthesis", author=user)
    response = api_client.get(SEARCH_URL, {"q": "photosynthesis"})
    assert response.data["count"] == 1
    assert "did_you_mean" in response.data
    assert response.data["did_you_mean"] is None
    assert all("did_you_mean" not in row for row in response.data["results"])


def test_did_you_mean_offers_a_title_on_zero_results_sqlite(api_client, user):
    sqlite_only()
    make_article("Photosynthesis", author=user)
    response = api_client.get(SEARCH_URL, {"q": "Photosynthesys"})
    assert response.data["count"] == 0
    assert response.data["did_you_mean"] == "Photosynthesis"


def test_did_you_mean_is_null_for_noise(api_client, user):
    make_article("Photosynthesis", author=user)
    response = api_client.get(SEARCH_URL, {"q": "qqqqzzzz"})
    assert response.data["count"] == 0
    assert response.data["did_you_mean"] is None


# --------------------------------------------------------------------------- #
# Snippets are safe by construction (DECISIONS §3)
# --------------------------------------------------------------------------- #
def test_safe_headline_escapes_then_marks():
    raw = "\x02<b>hit</b>\x03 & <script>alert(\"x\")</script> 'q'"
    assert safe_headline_to_marked(raw) == (
        "<mark>&lt;b&gt;hit&lt;/b&gt;</mark> &amp; "
        "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &#x27;q&#x27;"
    )


def test_safe_headline_neutralises_an_author_typed_mark_tag():
    # A literal <mark onclick=…> typed by an author is text, not one of the two
    # tokens this function is allowed to emit.
    assert safe_headline_to_marked("<mark onclick=steal()>x</mark>") == (
        "&lt;mark onclick=steal()&gt;x&lt;/mark&gt;"
    )


@pytest.mark.parametrize("empty", [None, ""])
def test_safe_headline_empty(empty):
    assert safe_headline_to_marked(empty) == ""


@pytest.fixture
def hostile_article(user):
    return make_article(
        '<script>alert("t")</script> Xylophone',
        author=user,
        short_description="<img src=x onerror=alert(1)> xylophone gloss",
        summary='<a href="javascript:alert(2)">xylophone</a> summary',
        content=(
            "Xylophone <script>alert('c')</script> keys & mallets.\n\n"
            '<img src=x onerror="alert(3)"> The xylophone is played with mallets.'
        ),
    )


def test_search_snippets_carry_no_markup_but_mark(api_client, hostile_article):
    response = api_client.get(SEARCH_URL, {"q": "xylophone"})
    assert response.data["count"] == 1
    row = response.data["results"][0]
    for field in ("title_snippet", "snippet"):
        remainder = strip_marks(row[field])
        assert "<" not in remainder, (field, row[field])
        assert ">" not in remainder, (field, row[field])
        assert "<script" not in row[field].lower()
    # The raw title is data, served as-is for the client to render as text.
    assert row["title"] == hostile_article.title


def test_sqlite_snippets_are_the_escaped_fallback_fields(api_client, hostile_article):
    sqlite_only()
    row = api_client.get(SEARCH_URL, {"q": "xylophone"}).data["results"][0]
    assert row["title_snippet"] == ("&lt;script&gt;alert(&quot;t&quot;)&lt;/script&gt; Xylophone")
    assert row["snippet"] == (
        "&lt;a href=&quot;javascript:alert(2)&quot;&gt;xylophone&lt;/a&gt; summary"
    )


def test_postgres_snippets_highlight_matches_with_mark(api_client, hostile_article):
    postgres_only()
    row = api_client.get(SEARCH_URL, {"q": "xylophone"}).data["results"][0]
    assert "<mark>" in row["title_snippet"]
    assert "<mark>" in row["snippet"]
    assert row["snippet"].count("<mark>") == row["snippet"].count("</mark>")


# --------------------------------------------------------------------------- #
# PostgreSQL-only search quality
# --------------------------------------------------------------------------- #
def test_postgres_typo_tolerance(api_client, user):
    postgres_only()
    make_article("Photosynthesis", author=user, short_description="How plants make sugar")
    response = api_client.get(SEARCH_URL, {"q": "photosynthasis"})
    assert [row["slug"] for row in response.data["results"]] == ["photosynthesis"]


def test_postgres_trigger_refreshes_vector_on_short_description_only_edit(api_client, user):
    # DECISIONS §6: short_description must be in both the weighting and the
    # UPDATE OF list, or editing only the gloss would never be searchable.
    postgres_only()
    article = make_article("Basalt", author=user, short_description="A volcanic rock")
    assert api_client.get(SEARCH_URL, {"q": "zanzibarite"}).data["count"] == 0

    article.short_description = "Zanzibarite volcanic rock"
    article.save(update_fields=["short_description"])
    response = api_client.get(SEARCH_URL, {"q": "zanzibarite"})
    assert [row["slug"] for row in response.data["results"]] == ["basalt"]

    # A queryset UPDATE bypasses save() entirely; the trigger still fires.
    Article.objects.filter(pk=article.pk).update(short_description="Quillwortish rock")
    response = api_client.get(SEARCH_URL, {"q": "quillwortish"})
    assert [row["slug"] for row in response.data["results"]] == ["basalt"]


# --------------------------------------------------------------------------- #
# Typeahead
# --------------------------------------------------------------------------- #
def test_suggest_is_capped_at_ten(api_client, user):
    for index in range(15):
        make_article(f"Alpha {index:02d}", author=user)
    response = api_client.get(SUGGEST_URL, {"q": "alpha"})
    assert response.status_code == 200
    assert len(response.data) == 10


def test_suggest_ignores_a_client_limit(api_client, user):
    for index in range(15):
        make_article(f"Alpha {index:02d}", author=user)
    response = api_client.get(SUGGEST_URL, {"q": "alpha", "limit": 50, "page_size": 50})
    assert len(response.data) == 10


def test_suggest_row_shape(api_client, user):
    make_article("Alphabet", author=user, short_description="A set of letters")
    response = api_client.get(SUGGEST_URL, {"q": "alph"})
    assert response.data == [
        {"slug": "alphabet", "title": "Alphabet", "short_description": "A set of letters"}
    ]
    assert response.headers["Cache-Control"] == "public, max-age=60"


@pytest.mark.parametrize("term", ["", "a", " b "])
def test_suggest_needs_two_characters(api_client, user, term):
    make_article("Alphabet", author=user)
    assert api_client.get(SUGGEST_URL, {"q": term}).data == []


def test_suggest_puts_prefix_matches_first(api_client, user):
    Article.objects.create(title="The history of the alphabet", content="x", view_count=900)
    Article.objects.create(title="Alphabet", content="x", view_count=1)
    response = api_client.get(SUGGEST_URL, {"q": "alphabet"})
    assert response.data[0]["slug"] == "alphabet"


def test_suggest_hides_drafts(api_client, user):
    make_article("Alphabet", author=user, is_published=False)
    assert api_client.get(SUGGEST_URL, {"q": "alpha"}).data == []


# --------------------------------------------------------------------------- #
# DECISIONS §2: the flat paths are the only paths
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("path", ["/api/articles/search/", "/api/articles/suggest/"])
def test_nested_search_paths_do_not_exist(api_client, path):
    assert api_client.get(path, {"q": "x"}).status_code == 404


def test_an_article_titled_search_cannot_take_the_reserved_slug(user):
    article = Article.objects.create(title="Search", content="x", author=user)
    assert article.slug != "search"
    assert article.slug.startswith("search-")
