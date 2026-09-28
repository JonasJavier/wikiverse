"""``manage.py seed``, ``seed_e2e`` and the corpus validator (DECISIONS §8,
§18, §19).

A full seed of the shipped corpus takes a couple of seconds on SQLite; the tests
that run one are marked ``slow`` so ``-m "not slow"`` gives a quick loop. The
read-only assertions about a seeded database live in ``test_seed_corpus.py``,
which seeds once per module.
"""

from __future__ import annotations

import copy
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.articles.management.commands._seed_data import ARTICLES
from apps.articles.management.commands._seed_data.meta import PLANNED_TITLES
from apps.articles.management.commands.seed import SEED_TAG
from apps.articles.management.commands.seed_e2e import CATEGORY_NAME
from apps.articles.management.commands.validators import validate_corpus
from apps.articles.models import (
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
from apps.common.utils import wiki_slug

User = get_user_model()

CORPUS_TITLES = {article["title"] for article in ARTICLES}
E2E_SLUGS = {"e2e-read-me", "e2e-edit-me", "e2e-talk-me"}


def run(*args) -> str:
    """Run a management command quietly and return its stdout."""
    out = StringIO()
    call_command(*args, stdout=out, stderr=StringIO())
    return out.getvalue()


def model_counts() -> dict[str, int]:
    return {
        model.__name__: model.objects.count()
        for model in (
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
            User,
        )
    }


def revision_fingerprint() -> list[tuple]:
    return list(
        Revision.objects.order_by("article__slug", "created_at").values_list(
            "article__slug",
            "created_at",
            "byte_size",
            "byte_delta",
            "comment",
            "is_minor",
            "is_bot",
        )
    )


# --------------------------------------------------------------------------- #
# The corpus validator (no database)
# --------------------------------------------------------------------------- #
def test_shipped_corpus_is_valid():
    assert validate_corpus(ARTICLES) == []


def test_corpus_is_a_subset_of_the_plan():
    # 63 of 120 today; nothing may assume either number (DECISIONS §19).
    assert ARTICLES
    assert len(CORPUS_TITLES) == len(ARTICLES)
    assert CORPUS_TITLES <= PLANNED_TITLES


def _with(index: int, **changes) -> list[dict]:
    """One corpus article with ``changes`` applied, as a one-article corpus.

    Per-article rules need nothing else, and validating 63 articles per case
    would dominate the module's run time.
    """
    modified = copy.deepcopy(ARTICLES[index])
    modified.update(changes)
    return [modified]


def _first_with_image() -> int:
    return next(index for index, article in enumerate(ARTICLES) if article["image"])


def test_validator_accepts_a_red_link_to_a_planned_title():
    unwritten = sorted(PLANNED_TITLES - CORPUS_TITLES)[0]
    content = ARTICLES[0]["content"] + f"\n\nIt is also discussed under [[{unwritten}]]."
    assert validate_corpus(_with(0, content=content)) == []


def test_validator_rejects_a_link_outside_the_plan():
    content = ARTICLES[0]["content"] + "\n\nSee [[Totally Unplanned Subject]]."
    problems = validate_corpus(_with(0, content=content))
    assert len(problems) == 1
    assert problems[0].startswith(f"{ARTICLES[0]['title']}: [wikilink-planned]")
    assert "Totally Unplanned Subject" in problems[0]


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/portrait.jpg",
        "http://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
        "https://upload.wikimedia.org.evil.example/x.jpg",
    ],
)
def test_validator_enforces_the_image_host_allowlist(url):
    index = _first_with_image()
    image = {**ARTICLES[index]["image"], "url": url}
    problems = validate_corpus(_with(index, image=image))
    assert any("[image-host]" in problem for problem in problems), problems


@pytest.mark.parametrize(
    ("suffix", "rule"),
    [
        ("\n\n# A level-one heading", "no-h1"),
        ('\n\nInline <script>alert("x")</script> markup.', "no-raw-html"),
        ("\n\nAn unresolved citation.[^nosuchkey]", "footnote-resolves"),
        ("\n\n## See also\n\nHand-written.", "no-handwritten-sections"),
    ],
)
def test_validator_rejects_body_rule_breaks(suffix, rule):
    problems = validate_corpus(_with(0, content=ARTICLES[0]["content"] + suffix))
    assert any(f"[{rule}]" in problem for problem in problems), problems


def test_validator_rejects_an_image_inside_the_infobox():
    problems = validate_corpus(_with(0, infobox={"image": "https://upload.wikimedia.org/x.jpg"}))
    assert any("[infobox-shape]" in problem for problem in problems)


def test_validator_rejects_duplicate_titles():
    problems = validate_corpus([*ARTICLES, copy.deepcopy(ARTICLES[0])])
    assert any("[title-unique]" in problem for problem in problems)


def test_validator_rejects_unknown_keys():
    problems = validate_corpus(_with(0, colour="red"))
    assert any("[article-shape]" in problem and "colour" in problem for problem in problems)


# --------------------------------------------------------------------------- #
# seed: guards
# --------------------------------------------------------------------------- #
@pytest.fixture
def legacy_javascript(db):
    """Pre-cutover content: a corpus slug with no seed-tagged history."""
    legacy_admin = User.objects.create_user("admin", "admin@example.com", "x")
    article = Article.objects.create(
        title="JavaScript", content="Legacy demo text.", author=legacy_admin
    )
    Revision.objects.create(
        article=article, editor=legacy_admin, title="JavaScript", content="Legacy demo text."
    )
    return article


def test_seed_refuses_pre_cutover_content(legacy_javascript):
    before = model_counts()
    with pytest.raises(CommandError) as excinfo:
        run("seed")
    message = str(excinfo.value)
    assert "javascript" in message
    assert "manage.py seed --flush --force" in message
    assert model_counts() == before  # nothing was written
    legacy_javascript.refresh_from_db()
    assert legacy_javascript.content == "Legacy demo text."


def test_seed_flush_without_force_is_refused(legacy_javascript):
    with pytest.raises(CommandError, match="--flush --force"):
        run("seed", "--flush")
    assert Article.objects.get(slug="javascript").content == "Legacy demo text."


def test_seed_force_overwrites_in_place(legacy_javascript):
    run("seed", "--force", "--only", "javascript")
    article = Article.objects.get(slug="javascript")
    assert article.pk == legacy_javascript.pk
    assert article.content != "Legacy demo text."
    seeded = [r for r in article.revisions.all() if SEED_TAG in (r.tags or [])]
    assert len(seeded) >= 2


@pytest.mark.slow
def test_seed_flush_force_wipes_and_reseeds(legacy_javascript):
    run("seed", "--flush", "--force")
    assert Article.objects.count() == len(ARTICLES)
    article = Article.objects.get(slug="javascript")
    assert article.content != "Legacy demo text."
    assert all(SEED_TAG in (r.tags or []) for r in article.revisions.all())
    # Accounts survive a flush: authorship of kept history must not be rewritten.
    assert User.objects.filter(username="admin").exists()


def test_seed_check_writes_nothing(db):
    output = run("seed", "--check")
    assert "Corpus valid" in output
    assert Article.objects.count() == 0
    assert User.objects.count() == 0


def test_seed_only_rejects_an_unknown_slug(db):
    with pytest.raises(CommandError, match="no-such-article"):
        run("seed", "--only", "no-such-article")


# --------------------------------------------------------------------------- #
# seed: idempotency (§19 — deterministic, no now())
# --------------------------------------------------------------------------- #
@pytest.mark.slow
def test_seed_twice_on_an_empty_database_is_identical(db):
    first_output = run("seed")
    first_counts = model_counts()
    first_revisions = revision_fingerprint()

    second_output = run("seed")

    assert model_counts() == first_counts
    assert revision_fingerprint() == first_revisions
    summary = first_output[first_output.index("Seed complete") :]
    assert second_output[second_output.index("Seed complete") :] == summary
    assert first_counts["Article"] == len(ARTICLES)


def test_seed_only_is_idempotent_and_leaves_the_main_page_alone(db):
    run("seed", "--only", "photosynthesis")
    counts = model_counts()
    run("seed", "--only", "photosynthesis")
    assert model_counts() == counts
    assert counts["Article"] == 1
    assert counts["MainPageBlock"] == 0


# --------------------------------------------------------------------------- #
# seed_e2e (§18)
# --------------------------------------------------------------------------- #
def test_seed_e2e_contract(db):
    output = run("seed_e2e")
    assert set(Article.objects.values_list("slug", flat=True)) == E2E_SLUGS
    assert list(Category.objects.values_list("name", flat=True)) == [CATEGORY_NAME]
    for slug in E2E_SLUGS:
        article = Article.objects.get(slug=slug)
        revisions = list(article.revisions.order_by("created_at"))
        assert len(revisions) == 2
        assert revisions[0].is_page_creation and revisions[0].parent_id is None
        assert revisions[1].parent_id == revisions[0].pk
        assert revisions[1].content == article.content
        assert article.revision_total == 2
    assert not User.objects.filter(is_superuser=True).exists()
    assert not User.objects.filter(is_staff=True).exists()
    assert not any(user.has_usable_password() for user in User.objects.all())
    assert "No superuser was created" in output


def test_seed_e2e_fixture_details(db, api_client):
    run("seed_e2e")
    thread = TalkThread.objects.get(article__slug="e2e-talk-me")
    assert thread.message_count == 1
    link = ArticleLink.objects.get(from_article__slug="e2e-read-me")
    assert link.to_article.slug == "e2e-edit-me"
    response = api_client.get("/api/articles/e2e-edit-me/diff/")
    assert response.status_code == 200
    assert response.data["stats"]["lines_added"] > 0


def test_seed_e2e_is_idempotent(db):
    run("seed_e2e")
    counts = model_counts()
    run("seed_e2e")
    assert model_counts() == counts
    run("seed_e2e", "--flush")
    assert model_counts() == counts


def test_seed_e2e_slugs_are_not_corpus_slugs():
    assert not E2E_SLUGS & {wiki_slug(title) for title in CORPUS_TITLES}
