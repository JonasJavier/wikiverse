"""Read-only assertions about a database seeded from the shipped corpus.

The corpus is seeded **once per module** (outside the per-test transaction) and
flushed afterwards, so these checks cost one seed rather than one each. Every
test here only reads; anything that writes belongs in ``test_seed.py``.
"""

from __future__ import annotations

from io import StringIO
from urllib.parse import urlsplit

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command

from apps.articles.infobox import validate_infobox
from apps.articles.management.commands._seed_data import ARTICLES
from apps.articles.management.commands._seed_data.meta import PLANNED_TITLES
from apps.articles.management.commands.seed import MAX_REVISIONS, MIN_REVISIONS, SEED_TAG
from apps.articles.models import Article, ArticleLink, MainPageBlock, Redirect, Revision
from apps.common.utils import RESERVED_SLUGS, wiki_slug

pytestmark = [pytest.mark.django_db, pytest.mark.slow]

User = get_user_model()

CORPUS_TITLES = {article["title"] for article in ARTICLES}


@pytest.fixture(scope="module", autouse=True)
def seeded_corpus(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("seed", stdout=StringIO(), stderr=StringIO())
    yield
    with django_db_blocker.unblock():
        call_command("flush", interactive=False, verbosity=0)


def test_every_corpus_article_exists():
    slugs = set(Article.objects.values_list("slug", flat=True))
    assert slugs == {wiki_slug(title) for title in CORPUS_TITLES}
    assert Article.objects.filter(is_published=True, is_deleted=False).count() == len(ARTICLES)


def test_seed_creates_no_superuser_and_no_usable_password():
    assert not User.objects.filter(is_superuser=True).exists()
    assert not User.objects.filter(is_staff=True).exists()
    assert User.objects.exists()
    assert not any(user.has_usable_password() for user in User.objects.all())


def test_history_is_synthesised_within_bounds():
    for article in Article.objects.all():
        revisions = list(article.revisions.order_by("created_at", "id"))
        assert MIN_REVISIONS <= len(revisions) <= MAX_REVISIONS, article.slug
        assert article.revision_total == len(revisions)
        assert revisions[0].is_page_creation and revisions[0].parent_id is None
        assert revisions[-1].content == article.content, article.slug
        assert all(SEED_TAG in revision.tags for revision in revisions)
        for parent, child in zip(revisions, revisions[1:], strict=False):
            assert child.parent_id == parent.pk
            assert child.byte_delta == child.byte_size - parent.byte_size
        assert revisions[0].byte_delta == revisions[0].byte_size


def test_bot_edits_are_flagged_minor_and_bot():
    bot_revisions = Revision.objects.filter(editor__is_bot=True)
    assert bot_revisions.exists()
    assert not bot_revisions.filter(is_bot=False).exists()
    assert not bot_revisions.filter(is_minor=False).exists()


def test_red_links_are_recorded_with_a_null_target():
    red = ArticleLink.objects.filter(to_article__isnull=True)
    assert red.exists()
    for link in red:
        assert link.to_title in PLANNED_TITLES
        assert link.to_title not in CORPUS_TITLES
        assert link.to_slug == wiki_slug(link.to_title)


def test_blue_links_resolve_to_their_titles():
    blue = ArticleLink.objects.filter(to_article__isnull=False).select_related("to_article")
    assert blue.exists()
    for link in blue:
        assert link.to_article.slug == link.to_slug
        assert link.to_title in CORPUS_TITLES


def test_every_link_target_is_in_the_plan():
    targets = set(ArticleLink.objects.values_list("to_title", flat=True))
    assert targets <= PLANNED_TITLES | CORPUS_TITLES


def test_wanted_pages_endpoint_reports_red_links(api_client):
    response = api_client.get("/api/wanted/")
    assert response.status_code == 200
    assert response.data["count"] > 0
    assert all(row["title"] not in CORPUS_TITLES for row in response.data["results"])


def test_redirects_are_reachable_and_resolve(api_client):
    redirects = list(Redirect.objects.select_related("target"))
    assert redirects
    article_slugs = set(Article.objects.values_list("slug", flat=True))
    for redirect in redirects:
        assert redirect.from_slug not in RESERVED_SLUGS
        assert redirect.from_slug not in article_slugs
        assert redirect.target.is_published
    sample = redirects[0]
    response = api_client.get(f"/api/articles/{sample.from_slug}/")
    assert response.status_code == 200
    assert response.data["slug"] == sample.target.slug
    assert response.data["redirected_from"] == sample.from_title


def test_lead_images_stay_on_the_allowlist():
    allowed = {host.lower() for host in settings.LEAD_IMAGE_ALLOWED_HOSTS}
    with_images = Article.objects.exclude(lead_image_url="")
    assert with_images.exists()
    for article in with_images:
        parts = urlsplit(article.lead_image_url)
        assert parts.scheme == "https"
        assert parts.netloc.lower() in allowed
        assert article.lead_image_credit  # attribution is not optional (§1)


def test_every_infobox_is_valid():
    for infobox in Article.objects.values_list("infobox", flat=True):
        validate_infobox(infobox)


def test_main_page_is_populated(api_client):
    assert MainPageBlock.objects.filter(kind="featured").exists()
    data = api_client.get("/api/main-page/").data
    assert data["featured"] is not None
    assert data["featured"]["extract"]
    assert data["dyk"] and data["otd"]
    assert data["stats"]["articles"] == len(ARTICLES)


def test_categories_are_attached_primary_first(api_client):
    source = next(article for article in ARTICLES if article["categories"])
    response = api_client.get(f"/api/articles/{wiki_slug(source['title'])}/")
    names = [row["name"] for row in response.data["categories"]]
    assert names[0] == source["category"]
    assert set(names[1:]) == set(source["categories"]) - {source["category"]}


def test_seeded_search_finds_by_title(api_client):
    response = api_client.get("/api/search/", {"q": "photosynthesis"})
    assert response.status_code == 200
    assert response.data["results"][0]["slug"] == "photosynthesis"


def test_seeded_history_diffs_show_growth(api_client):
    response = api_client.get("/api/articles/photosynthesis/diff/", {"from": 0})
    assert response.status_code == 200
    assert response.data["created"] is True
