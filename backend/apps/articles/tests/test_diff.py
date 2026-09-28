"""The diff engine (pure, no database) and ``GET /api/articles/{slug}/diff/``
(DECISIONS §14).

The engine tests pin the payload's load-bearing invariants: reassembling the
ops of every row reproduces both sides byte for byte, line numbers are 1-based,
stats count UTF-8 bytes, and every safety valve reports ``truncated``.
"""

from __future__ import annotations

import pytest
from django.core.cache import cache

from apps.articles.diff import (
    PAYLOAD_VERSION,
    diff_revisions,
    normalise_newlines,
    split_lines,
    tokenise,
    word_ops,
)
from apps.articles.models import Article, Revision

OLD_DOC = (
    "## History\n"
    "PostgreSQL began as the POSTGRES project at Berkeley in 1986.\n"
    "\n"
    "It is maintained by a global community.\n"
    "Obsolete sentence.\n"
    "Unchanged tail line one.\n"
    "Unchanged tail line two.\n"
)
NEW_DOC = (
    "## History\n"
    "PostgreSQL began as the **POSTGRES** project at Berkeley in 1986, led by Michael Stonebraker.\n"
    "\n"
    "It is maintained by a global community.\n"
    "It was renamed in 1996.\n"
    "Unchanged tail line one.\n"
    "Unchanged tail line two — naïve café ✓.\n"
)

EVERYTHING = 10**6  # context wide enough that one hunk covers the whole document


def old_side(row: dict) -> str:
    return "".join(text for kind, text in row["ops"] if kind in {"=", "-"})


def new_side(row: dict) -> str:
    return "".join(text for kind, text in row["ops"] if kind in {"=", "+"})


def rebuild(payload: dict) -> tuple[str, str]:
    """Reassemble both documents from a full-context payload."""
    old_lines, new_lines = [], []
    for hunk in payload["hunks"]:
        for row in hunk["rows"]:
            if row["a"] is not None:
                old_lines.append(old_side(row))
            if row["b"] is not None:
                new_lines.append(new_side(row))
    return "\n".join(old_lines), "\n".join(new_lines)


# --------------------------------------------------------------------------- #
# Tokeniser and line splitting
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text",
    [
        "",
        "plain words here",
        "  leading and trailing  ",
        "tabs\tand nbsp",
        "punctuation!?,.;:—–…",
        "[[Wikilink|display]] and [^ref1] and **bold** and `code`",
        "Erdős number, naïve café, Mähren, 東京タワー, emoji ✓🙂",
        "a​zero-width",
    ],
)
def test_tokenise_round_trips(text):
    assert "".join(tokenise(text)) == text


def test_tokenise_keeps_words_whole():
    assert tokenise("naïve café, ok") == ["naïve", " ", "café", ",", " ", "ok"]


@pytest.mark.parametrize(
    ("text", "lines"),
    [
        ("", []),
        (None, []),
        ("a", ["a"]),
        ("a\nb\n", ["a", "b"]),
        ("a\nb\n\n", ["a", "b", ""]),
        ("a\r\nb\rc", ["a", "b", "c"]),
        ("form\x0cfeed\x0bvtab ls", ["form\x0cfeed\x0bvtab ls"]),
    ],
)
def test_split_lines(text, lines):
    assert split_lines(text) == lines


def test_normalise_newlines():
    assert normalise_newlines("a\r\nb\rc\n") == "a\nb\nc\n"
    assert normalise_newlines(None) == ""


# --------------------------------------------------------------------------- #
# Payload invariants
# --------------------------------------------------------------------------- #
def test_reassembling_every_op_reproduces_both_sources():
    payload = diff_revisions(OLD_DOC, NEW_DOC, context=EVERYTHING)
    old, new = rebuild(payload)
    assert old == OLD_DOC.removesuffix("\n")
    assert new == NEW_DOC.removesuffix("\n")
    assert old.encode("utf-8") == OLD_DOC.removesuffix("\n").encode("utf-8")
    assert new.encode("utf-8") == NEW_DOC.removesuffix("\n").encode("utf-8")


def test_every_row_satisfies_the_round_trip_invariant():
    old_lines = split_lines(OLD_DOC)
    new_lines = split_lines(NEW_DOC)
    payload = diff_revisions(OLD_DOC, NEW_DOC)
    rows = [row for hunk in payload["hunks"] for row in hunk["rows"]]
    assert rows
    for row in rows:
        assert row["t"] in {"=", "~", "+", "-"}
        if row["a"] is not None:
            assert old_side(row) == old_lines[row["a"] - 1]
        if row["b"] is not None:
            assert new_side(row) == new_lines[row["b"] - 1]
        assert all(text for _kind, text in row["ops"]), "ops never carry empty text"


def test_row_kinds_and_word_level_ops():
    payload = diff_revisions(OLD_DOC, NEW_DOC)
    rows = [row for hunk in payload["hunks"] for row in hunk["rows"]]
    by_kind = {}
    for row in rows:
        by_kind.setdefault(row["t"], []).append(row)
    modified = by_kind["~"][0]
    assert modified["a"] == 2 and modified["b"] == 2
    # Word-level, not line-level: the unchanged words stay "=".
    assert modified["ops"][:4] == [
        ["=", "PostgreSQL began as the "],
        ["+", "**"],
        ["=", "POSTGRES"],
        ["+", "**"],
    ]
    assert ["+", ", led by Michael Stonebraker"] in modified["ops"]
    removed = by_kind.get("-", [])
    replaced = [row for row in by_kind["~"] if row["a"] == 5]
    assert removed or replaced  # "Obsolete sentence." is gone either way


def test_stats_count_lines_and_utf8_bytes():
    old = "same\nold ü line\nremoved\n"
    new = "same\nnew ü line\n"
    payload = diff_revisions(old, new)
    assert payload["stats"] == {
        "lines_added": 0,
        "lines_removed": 1,
        "lines_changed": 1,
        "bytes_added": len("new ü line".encode()),
        "bytes_removed": len("old ü line".encode()) + len(b"removed"),
    }
    # UTF-8 bytes, not characters.
    assert payload["stats"]["bytes_added"] == 11


def test_identical_bodies_have_no_hunks():
    payload = diff_revisions(OLD_DOC, OLD_DOC)
    assert payload["hunks"] == []
    assert payload["created"] is False and payload["truncated"] is False
    assert set(payload["stats"].values()) == {0}


def test_crlf_only_changes_are_not_a_rewrite():
    assert diff_revisions("a\nb\n", "a\r\nb\r\n")["hunks"] == []


def test_page_creation_is_one_all_plus_hunk():
    payload = diff_revisions("", "first\nsecond\n")
    assert payload["created"] is True
    (hunk,) = payload["hunks"]
    assert (hunk["a_start"], hunk["a_lines"], hunk["b_start"], hunk["b_lines"]) == (1, 0, 1, 2)
    assert [row["t"] for row in hunk["rows"]] == ["+", "+"]
    assert [row["a"] for row in hunk["rows"]] == [None, None]
    assert [row["b"] for row in hunk["rows"]] == [1, 2]


def test_blank_lines_have_empty_ops():
    payload = diff_revisions("x\n", "x\n\ny\n", context=EVERYTHING)
    rows = payload["hunks"][0]["rows"]
    assert {"t": "+", "a": None, "b": 2, "ops": []} in rows


def test_context_limits_hunks_to_the_changed_region():
    old = "\n".join(f"line {n}" for n in range(1, 41))
    new = old.replace("line 20", "line twenty")
    (hunk,) = diff_revisions(old, new)["hunks"]
    assert hunk["a_start"] == 17  # three lines of context before line 20
    assert hunk["a_lines"] == hunk["b_lines"] == 7
    assert [row["t"] for row in hunk["rows"]] == ["=", "=", "=", "~", "=", "=", "="]


def test_two_distant_changes_make_two_hunks():
    old = "\n".join(f"line {n}" for n in range(1, 41))
    new = old.replace("line 5", "line five").replace("line 35", "line thirty-five")
    hunks = diff_revisions(old, new)["hunks"]
    assert len(hunks) == 2
    assert hunks[0]["a_start"] < hunks[1]["a_start"]


# --------------------------------------------------------------------------- #
# Safety valves
# --------------------------------------------------------------------------- #
def test_max_chars_valve():
    payload = diff_revisions("a" * 50, "b" * 50, max_chars=10)
    assert payload["truncated"] is True


def test_max_lines_valve():
    payload = diff_revisions("", "\n".join("x" for _ in range(20)), max_lines=5)
    assert payload["truncated"] is True
    assert sum(len(hunk["rows"]) for hunk in payload["hunks"]) == 5


def test_max_rows_valve_keeps_stats_accurate():
    new = "\n".join(f"row {n}" for n in range(30))
    payload = diff_revisions("", new, max_rows=4)
    assert payload["truncated"] is True
    assert sum(len(hunk["rows"]) for hunk in payload["hunks"]) == 4
    assert payload["stats"]["lines_added"] == 30


def test_max_row_tokens_valve_falls_back_to_whole_lines():
    ops, truncated = word_ops("one two three", "four five six", max_tokens=3)
    assert truncated is True
    assert ops == [["-", "one two three"], ["+", "four five six"]]
    payload = diff_revisions("one two three\n", "four five six\n", max_row_tokens=3)
    assert payload["truncated"] is True


def test_word_ops_equal_lines():
    assert word_ops("same text", "same text") == ([["=", "same text"]], False)


def test_payload_version_is_an_int():
    assert isinstance(PAYLOAD_VERSION, int)


# --------------------------------------------------------------------------- #
# The endpoint
# --------------------------------------------------------------------------- #
DIFF_FIELDS = {
    "article",
    "from_revision",
    "to_revision",
    "prev_id",
    "next_id",
    "created",
    "truncated",
    "title_changed",
    "summary_changed",
    "stats",
    "hunks",
}


@pytest.fixture
def history(db, auth_client):
    """An article with three revisions written through the API."""
    created = auth_client.post(
        "/api/articles/",
        {"title": "Diffable", "summary": "v1", "content": "Alpha.\n\nBeta.\n", "comment": "c1"},
        format="json",
    )
    slug = created.data["slug"]
    auth_client.patch(
        f"/api/articles/{slug}/",
        {"content": "Alpha.\n\nBeta gamma.\n", "comment": "c2"},
        format="json",
    )
    auth_client.patch(
        f"/api/articles/{slug}/",
        {"content": "Alpha.\n\nBeta gamma.\n\nDelta ö.\n", "summary": "v3", "comment": "c3"},
        format="json",
    )
    revisions = list(Revision.objects.filter(article__slug=slug).order_by("created_at", "id"))
    assert len(revisions) == 3
    return slug, revisions


def test_diff_between_two_revisions(api_client, history):
    slug, (r1, r2, _r3) = history
    response = api_client.get(f"/api/articles/{slug}/diff/", {"from": r1.pk, "to": r2.pk})
    assert response.status_code == 200
    data = response.data
    assert set(data) == DIFF_FIELDS
    assert data["article"]["slug"] == slug
    assert data["from_revision"]["id"] == r1.pk
    assert data["to_revision"]["id"] == r2.pk
    assert set(data["to_revision"]) == {
        "id",
        "editor",
        "comment",
        "byte_size",
        "is_minor",
        "created_at",
    }
    assert data["prev_id"] == r1.pk
    assert data["next_id"] == history[1][2].pk
    assert data["created"] is False
    assert data["stats"]["lines_changed"] == 1
    # Historical diffs never change, so they are cacheable forever.
    assert response.headers["Cache-Control"] == "public, max-age=31536000, immutable"


def test_diff_defaults_to_latest_against_its_parent(api_client, history):
    slug, (_r1, r2, r3) = history
    response = api_client.get(f"/api/articles/{slug}/diff/")
    assert response.data["to_revision"]["id"] == r3.pk
    assert response.data["from_revision"]["id"] == r2.pk
    assert response.data["next_id"] is None
    assert response.data["summary_changed"] is True
    assert response.data["title_changed"] is False
    # The current revision can still gain a successor: short cache only.
    assert response.headers["Cache-Control"] == "public, max-age=60"


def test_diff_from_zero_is_the_page_creation(api_client, history):
    slug, (r1, _r2, _r3) = history
    response = api_client.get(f"/api/articles/{slug}/diff/", {"from": 0, "to": r1.pk})
    assert response.status_code == 200
    assert response.data["created"] is True
    assert response.data["from_revision"]["id"] is None
    assert response.data["prev_id"] is None
    rows = [row for hunk in response.data["hunks"] for row in hunk["rows"]]
    assert {row["t"] for row in rows} == {"+"}


@pytest.mark.parametrize(("params", "field"), [({"from": "abc"}, "from"), ({"to": "latest"}, "to")])
def test_diff_rejects_non_numeric_ids(api_client, history, params, field):
    slug, _revisions = history
    response = api_client.get(f"/api/articles/{slug}/diff/", params)
    assert response.status_code == 400
    assert field in response.data


def test_diff_with_a_revision_of_another_article_is_404(api_client, history, article, user):
    slug, (r1, _r2, _r3) = history
    foreign = Revision.objects.create(article=article, editor=user, title="Django", content="x")
    assert (
        api_client.get(f"/api/articles/{slug}/diff/", {"from": foreign.pk, "to": r1.pk}).status_code
        == 404
    )
    assert api_client.get(f"/api/articles/{slug}/diff/", {"to": 999999}).status_code == 404


def test_diff_of_an_article_without_history_is_404(api_client, article):
    assert api_client.get(f"/api/articles/{article.slug}/diff/").status_code == 404


def test_diff_of_a_draft_is_hidden_from_readers(api_client, history):
    slug, _revisions = history
    Article.objects.filter(slug=slug).update(is_published=False)
    from rest_framework.test import APIClient

    assert APIClient().get(f"/api/articles/{slug}/diff/").status_code == 404


def test_historical_diff_is_cached_under_the_payload_version(api_client, history):
    slug, (r1, r2, _r3) = history
    api_client.get(f"/api/articles/{slug}/diff/", {"from": r1.pk, "to": r2.pk})
    assert cache.get(f"diff:v{PAYLOAD_VERSION}:{r1.pk}:{r2.pk}") is not None


# --------------------------------------------------------------------------- #
# byte_delta on the revisions themselves
# --------------------------------------------------------------------------- #
def test_revision_byte_sizes_and_deltas_are_utf8(history):
    _slug, (r1, r2, r3) = history
    sizes = [len(r.content.encode("utf-8")) for r in (r1, r2, r3)]
    assert [r.byte_size for r in (r1, r2, r3)] == sizes
    assert r1.byte_delta == sizes[0]
    assert r2.byte_delta == sizes[1] - sizes[0]
    assert r3.byte_delta == sizes[2] - sizes[1]
    # DRF trims the trailing newline; the appended "\n\nDelta ö." is 11 bytes
    # because "ö" is two of them.
    assert r3.content.endswith("\n\nDelta ö.")
    assert r3.byte_delta == 11
    assert [r.parent_id for r in (r1, r2, r3)] == [None, r1.pk, r2.pk]


def test_article_byte_size_counts_bytes_not_characters(db, user):
    article = Article.objects.create(title="Bytes", content="ööö", author=user)
    assert article.byte_size == 6
