"""Crawler surfaces (DECISIONS §16): ``sitemap.xml``, ``robots.txt`` and the
per-article Open Graph shell at ``/og/wiki/<slug>/``.

Every absolute URL must come from ``PUBLIC_BASE_URL`` / ``PUBLIC_SITE_DOMAIN``,
never from the request ``Host`` (nginx rewrites it to the backend's own host).
"""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET

import pytest

from apps.articles.models import Article, Category, Redirect

pytestmark = pytest.mark.django_db

BASE = "https://wiki.example.test"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
IMAGE = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"


@pytest.fixture(autouse=True)
def public_site(settings):
    settings.PUBLIC_BASE_URL = BASE
    settings.PUBLIC_SITE_DOMAIN = "wiki.example.test"


def sitemap_locs(response) -> list[str]:
    root = ET.fromstring(response.content)
    return [node.text for node in root.findall("./sm:url/sm:loc", SITEMAP_NS)]


def meta(content: str, attr: str, name: str) -> str | None:
    match = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)">', content)
    return html.unescape(match.group(1)) if match else None


def json_ld(content: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.S)
    return [json.loads(block) for block in blocks]


# --------------------------------------------------------------------------- #
# sitemap.xml
# --------------------------------------------------------------------------- #
@pytest.fixture
def mixed_articles(user, category):
    Article.objects.create(title="Published page", content="x", author=user, category=category)
    Article.objects.create(title="Stub page", content="x", author=user, is_stub=True)
    Article.objects.create(
        title="Mercury disambiguation",
        content="x",
        author=user,
        page_type=Article.PageType.DISAMBIGUATION,
    )
    Article.objects.create(title="Möbius strip", content="x", author=user)
    Article.objects.create(title="Draft page", content="x", author=user, is_published=False)
    gone = Article.objects.create(title="Deleted page", content="x", author=user)
    gone.soft_delete(by=user)


def test_sitemap_lists_exactly_the_crawlable_articles(client, mixed_articles):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    articles = {loc for loc in sitemap_locs(response) if "/wiki/" in loc}
    assert articles == {
        f"{BASE}/wiki/published-page",
        f"{BASE}/wiki/stub-page",
        f"{BASE}/wiki/mercury-disambiguation",
        f"{BASE}/wiki/m%C3%B6bius-strip",
    }


def test_sitemap_uses_the_public_host_not_the_request_host(client, mixed_articles):
    locs = sitemap_locs(client.get("/sitemap.xml", HTTP_HOST="backend.up.railway.app"))
    assert locs
    assert all(loc.startswith(f"{BASE}/") for loc in locs)
    assert not any("railway" in loc or "testserver" in loc for loc in locs)


def test_sitemap_protocol_follows_public_base_url(client, settings, mixed_articles):
    settings.PUBLIC_BASE_URL = "http://localhost:5173"
    settings.PUBLIC_SITE_DOMAIN = "localhost:5173"
    locs = sitemap_locs(client.get("/sitemap.xml"))
    assert all(loc.startswith("http://localhost:5173/") for loc in locs)


def test_sitemap_static_and_category_routes(client, mixed_articles):
    locs = set(sitemap_locs(client.get("/sitemap.xml")))
    assert {f"{BASE}/", f"{BASE}/browse", f"{BASE}/categories", f"{BASE}/changes"} <= locs
    assert f"{BASE}/category/programming" in locs
    assert not any(loc.startswith(f"{BASE}/search") for loc in locs)


def test_sitemap_on_the_api_host_matches(client, mixed_articles):
    assert sitemap_locs(client.get("/api/sitemap.xml")) == sitemap_locs(client.get("/sitemap.xml"))


# --------------------------------------------------------------------------- #
# robots.txt
# --------------------------------------------------------------------------- #
def test_robots_txt(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/plain")
    lines = response.content.decode().splitlines()
    assert "User-agent: *" in lines
    for path in ("/api/", "/admin/", "/og/", "/search"):
        assert f"Disallow: {path}" in lines
    assert f"Sitemap: {BASE}/sitemap.xml" in lines


# --------------------------------------------------------------------------- #
# Open Graph crawler shell
# --------------------------------------------------------------------------- #
@pytest.fixture
def og_article(user, category):
    return Article.objects.create(
        title="Marie Curie",
        summary="Physicist and chemist who pioneered research on radioactivity.",
        content="**Marie Curie** was a physicist.",
        author=user,
        category=category,
        lead_image_url=IMAGE,
        lead_image_alt="Portrait of Marie Curie",
    )


def test_og_shell_tags(client, og_article):
    response = client.get("/og/wiki/marie-curie/")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")
    assert response["Cache-Control"] == "public, max-age=600"
    content = response.content.decode()
    canonical = f"{BASE}/wiki/marie-curie"

    assert meta(content, "property", "og:type") == "article"
    assert meta(content, "property", "og:title") == "Marie Curie"
    assert meta(content, "property", "og:description") == og_article.summary
    assert meta(content, "property", "og:url") == canonical
    assert meta(content, "property", "og:image") == IMAGE
    assert meta(content, "property", "og:image:alt") == "Portrait of Marie Curie"
    assert meta(content, "property", "article:section") == "Programming"
    assert meta(content, "name", "twitter:card") == "summary_large_image"
    assert meta(content, "name", "twitter:title") == "Marie Curie"
    assert f'<link rel="canonical" href="{canonical}">' in content
    assert f'<meta http-equiv="refresh" content="0; url={canonical}">' in content
    assert "<title>Marie Curie — Wikiverse</title>" in content


def test_og_shell_json_ld(client, og_article):
    content = client.get("/og/wiki/marie-curie/").content.decode()
    article_ld, breadcrumb_ld = json_ld(content)
    assert article_ld["@type"] == "Article"
    assert article_ld["headline"] == "Marie Curie"
    assert article_ld["url"] == f"{BASE}/wiki/marie-curie"
    assert article_ld["image"] == [IMAGE]
    assert article_ld["author"] == {"@type": "Person", "name": "tester"}
    assert article_ld["articleSection"] == "Programming"
    assert breadcrumb_ld["@type"] == "BreadcrumbList"
    assert [item["item"] for item in breadcrumb_ld["itemListElement"]] == [
        BASE,
        f"{BASE}/category/programming",
        f"{BASE}/wiki/marie-curie",
    ]


def test_og_shell_without_an_image_uses_a_small_card(client, user):
    Article.objects.create(title="Imageless", summary="No picture.", content="x", author=user)
    content = client.get("/og/wiki/imageless/").content.decode()
    assert meta(content, "name", "twitter:card") == "summary"
    assert meta(content, "property", "og:image") is None
    assert "image" not in json_ld(content)[0]


def test_og_description_falls_back_to_the_body(client, user):
    Article.objects.create(title="Bare", content="**Bare** has only a *body*.", author=user)
    content = client.get("/og/wiki/bare/").content.decode()
    assert meta(content, "property", "og:description") == "Bare has only a body."


@pytest.mark.parametrize("state", ["unknown", "draft", "deleted"])
def test_og_shell_404s_for_anything_not_crawlable(client, og_article, user, state):
    if state == "draft":
        Article.objects.filter(pk=og_article.pk).update(is_published=False)
    elif state == "deleted":
        og_article.soft_delete(by=user)
    slug = "no-such-article" if state == "unknown" else og_article.slug
    assert client.get(f"/og/wiki/{slug}/").status_code == 404


def test_og_shell_follows_redirects_to_the_canonical_url(client, og_article):
    Redirect.objects.create(from_slug="madame-curie", from_title="Madame Curie", target=og_article)
    response = client.get("/og/wiki/madame-curie/")
    assert response.status_code == 200
    content = response.content.decode()
    assert meta(content, "property", "og:url") == f"{BASE}/wiki/marie-curie"
    assert "Redirected from &ldquo;Madame Curie&rdquo;" in content


def test_og_shell_handles_unicode_slugs(client, user):
    Article.objects.create(title="Möbius strip", summary="A surface.", content="x", author=user)
    response = client.get("/og/wiki/m%C3%B6bius-strip/")
    assert response.status_code == 200
    assert meta(response.content.decode(), "property", "og:url") == f"{BASE}/wiki/m%C3%B6bius-strip"


def test_og_shell_escapes_hostile_article_text(client, user):
    title = '</script><script>alert("t")</script>'
    summary = '"><img src=x onerror=alert(1)> & more'
    category = Category.objects.create(name="<b>Cat</b>")
    Article.objects.create(
        title=title, slug="hostile", summary=summary, content="x", author=user, category=category
    )
    content = client.get("/og/wiki/hostile/").content.decode()
    # Only the two JSON-LD <script> elements exist, and nothing closes them early.
    assert content.count("<script") == 2
    assert content.count("</script>") == 2
    assert "<img" not in content
    assert "<b>Cat</b>" not in content
    assert meta(content, "property", "og:title") == title
    assert meta(content, "property", "og:description") == summary
    article_ld, _breadcrumbs = json_ld(content)
    assert article_ld["name"] == title
    assert article_ld["description"] == summary
