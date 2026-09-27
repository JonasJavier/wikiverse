"""Crawler-facing SEO surfaces.

Wikiverse is a client-rendered SPA, so social crawlers -- which do not execute
JavaScript -- would only ever see the site-level Open Graph card baked into
``index.html``. DECISIONS.md section 16 resolves that with a *crawler shell*:
nginx maps a small allowlist of social user agents and proxies their requests
for ``/wiki/<slug>`` to :class:`ArticleOpenGraphView`, which renders a tiny
metadata-only document. Humans never reach it through normal browsing, and the
few who do (a shared backend URL, a curious developer) get a ``<meta
http-equiv="refresh">`` plus a real anchor back to the SPA rather than a dead
end.

Everything here is derived from ``settings.PUBLIC_BASE_URL`` and
``settings.PUBLIC_SITE_DOMAIN`` at *call* time, never at import time, so an E2E
run can point both at its own host with ``override_settings``. Nothing is
hardcoded to the production domain beyond the fallbacks below, which exist only
so the module keeps working if the settings entries are absent.

Every value rendered into the shell is user-authored (article titles,
summaries, category names), so the template relies on Django's autoescaping and
the JSON-LD payloads are escaped for a ``<script>`` context before they are
marked safe.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, urlsplit

from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.safestring import SafeString, mark_safe
from django.utils.text import Truncator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

if TYPE_CHECKING:  # pragma: no cover - typing only
    from apps.articles.models import Article

__all__ = [
    "ArticleOpenGraphView",
    "RobotsTxtView",
    "article_canonical_url",
    "encode_path",
    "public_base_url",
    "site_domain",
    "site_protocol",
    "spa_url",
]

# Fallbacks used only when the settings entries are missing entirely.
DEFAULT_PUBLIC_BASE_URL = "https://wikiverse.jonasjavier.dev"
DEFAULT_PUBLIC_SITE_DOMAIN = "wikiverse.jonasjavier.dev"

SITE_NAME = "Wikiverse"
SITE_LOCALE = "en_US"
SITE_LANGUAGE = "en"

#: Longest ``og:description`` we will emit. Matches ``Article.summary``.
MAX_DESCRIPTION = 300

#: How long a crawler (or an intermediate CDN) may reuse the shell.
OG_MAX_AGE = 600

# Exactly the substitutions ``django.utils.html.json_script`` applies: with
# ``ensure_ascii=True`` on top, the serialized payload is pure ASCII and cannot
# terminate the surrounding <script> element or open an HTML comment.
_JSON_SCRIPT_ESCAPES = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


# --------------------------------------------------------------------------- #
# Public URL helpers
# --------------------------------------------------------------------------- #
def public_base_url() -> str:
    """Return the public SPA origin, without a trailing slash.

    Read at call time so tests and E2E runs can override the setting.
    """
    raw = str(getattr(settings, "PUBLIC_BASE_URL", "") or "").strip()
    raw = raw.strip('"').strip("'").rstrip("/")
    if not raw:
        raw = DEFAULT_PUBLIC_BASE_URL
    if "://" not in raw:
        raw = f"https://{raw}"
    return raw


def site_protocol() -> str:
    """Return the scheme of :func:`public_base_url` (``http`` or ``https``)."""
    scheme = urlsplit(public_base_url()).scheme
    return scheme if scheme in {"http", "https"} else "https"


def site_domain() -> str:
    """Return the public SPA host.

    ``PUBLIC_SITE_DOMAIN`` wins; otherwise the host is taken from
    ``PUBLIC_BASE_URL``. This must never fall back to the request ``Host``:
    nginx rewrites it to the backend's Railway hostname, which would publish a
    sitemap pointing crawlers at a host that only serves JSON.
    """
    raw = str(getattr(settings, "PUBLIC_SITE_DOMAIN", "") or "").strip()
    raw = raw.strip('"').strip("'").strip("/")
    if raw:
        return raw
    return urlsplit(public_base_url()).netloc or DEFAULT_PUBLIC_SITE_DOMAIN


def encode_path(path: str) -> str:
    """Percent-encode a route path, leaving ``/`` and ASCII alone.

    ``wiki_slug`` runs ``slugify(allow_unicode=True)``, so real slugs contain
    characters like ``ł`` and ``ö``. The sitemaps protocol requires RFC 3986
    URLs, and a canonical ``href`` should match what the sitemap publishes, so
    both go through this one function. Slugs never contain ``%``, so
    double-encoding is not a risk.
    """
    return quote(path, safe="/")


def spa_url(path: str) -> str:
    """Absolute URL for an SPA route such as ``/wiki/marie-curie``."""
    return f"{public_base_url()}/{encode_path(path.lstrip('/'))}"


def article_canonical_url(slug: str) -> str:
    """Canonical SPA URL for an article slug."""
    return spa_url(f"wiki/{slug}")


def _json_ld(payload: dict[str, Any]) -> SafeString:
    """Serialize ``payload`` for embedding in a ``<script>`` element.

    ``ensure_ascii=True`` plus the ``< > &`` escapes means the result contains
    no character that HTML parses specially, so marking it safe is sound.
    """
    dumped = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    return mark_safe(dumped.translate(_JSON_SCRIPT_ESCAPES))  # noqa: S308 - escaped above


# --------------------------------------------------------------------------- #
# Article resolution
# --------------------------------------------------------------------------- #
def _crawlable_articles():
    """Only published, non-deleted articles are ever exposed to crawlers."""
    from apps.articles.models import Article

    return Article.objects.filter(is_published=True, is_deleted=False)


def resolve_article(slug: str) -> tuple[Article, str]:
    """Resolve ``slug`` to a crawlable article.

    Returns ``(article, redirected_from)`` where ``redirected_from`` is the
    title the crawler asked for when the slug was a :class:`Redirect` source,
    and ``""`` otherwise. Raises :class:`~django.http.Http404` for unknown,
    unpublished and soft-deleted slugs alike -- an unpublished draft must not
    leak its summary through the shell.
    """
    from apps.articles.models import Redirect

    slug = (slug or "").strip().strip("/")
    if not slug:
        raise Http404("No article slug given.")

    article = _crawlable_articles().select_related("category", "author").filter(slug=slug).first()
    if article is not None:
        return article, ""

    redirect = (
        Redirect.objects.select_related("target", "target__category", "target__author")
        .filter(from_slug=slug)
        .first()
    )
    if redirect is not None:
        target = redirect.target
        if target is not None and target.is_published and not target.is_deleted:
            return target, redirect.from_title
    raise Http404(f"No crawlable article for slug {slug!r}.")


def _description(article: Article) -> str:
    """Best available plain-text description, capped at 300 characters."""
    from apps.common.utils import strip_markup

    for candidate in (article.summary, article.short_description):
        text = (candidate or "").strip()
        if text:
            return Truncator(text).chars(MAX_DESCRIPTION)
    body = strip_markup(article.content or "").strip()
    if body:
        return Truncator(" ".join(body.split())).chars(MAX_DESCRIPTION)
    return f"{article.title} on {SITE_NAME}."


# --------------------------------------------------------------------------- #
# Views
# --------------------------------------------------------------------------- #
@method_decorator(cache_control(public=True, max_age=OG_MAX_AGE), name="dispatch")
class ArticleOpenGraphView(TemplateView):
    """The crawler shell for a single article.

    Mounted at ``/og/wiki/<slug>/``. nginx proxies social-crawler requests for
    ``/wiki/<slug>`` here; see the ``map $http_user_agent`` block in
    ``frontend/nginx.conf.template``.
    """

    template_name = "seo/article_og.html"
    content_type = "text/html; charset=utf-8"
    http_method_names = ["get", "head", "options"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        article, redirected_from = resolve_article(kwargs.get("slug", ""))

        base_url = public_base_url()
        canonical = article_canonical_url(article.slug)
        description = _description(article)
        image_url = (article.lead_image_url or "").strip()
        image_alt = (article.lead_image_alt or "").strip() or article.title
        category = article.category
        # A deleted account leaves author NULL; crediting the site as a Person
        # would be wrong, so fall back to the Organization node.
        author_ld: dict[str, str] = (
            {"@type": "Person", "name": article.author.username}
            if article.author is not None
            else {"@type": "Organization", "name": SITE_NAME}
        )

        article_ld: dict[str, Any] = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": Truncator(article.title).chars(110),
            "name": article.title,
            "description": description,
            "url": canonical,
            "datePublished": article.created_at.isoformat(),
            "dateModified": article.updated_at.isoformat(),
            "inLanguage": SITE_LANGUAGE,
            "wordCount": article.word_count,
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": base_url},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": base_url},
            "author": author_ld,
        }
        if image_url:
            article_ld["image"] = [image_url]
        if category is not None:
            article_ld["articleSection"] = category.name

        crumbs: list[tuple[str, str]] = [(SITE_NAME, base_url)]
        if category is not None:
            crumbs.append((category.name, spa_url(f"category/{category.slug}")))
        crumbs.append((article.title, canonical))
        breadcrumb_ld = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": index, "name": name, "item": url}
                for index, (name, url) in enumerate(crumbs, start=1)
            ],
        }

        context.update(
            {
                "article": article,
                "redirected_from": redirected_from,
                "site_name": SITE_NAME,
                "site_locale": SITE_LOCALE,
                "site_language": SITE_LANGUAGE,
                "page_title": f"{article.title} — {SITE_NAME}",
                "og_title": article.title,
                "og_description": description,
                "og_url": canonical,
                "og_image": image_url,
                "og_image_alt": image_alt if image_url else "",
                "twitter_card": "summary_large_image" if image_url else "summary",
                "published_time": article.created_at.isoformat(),
                "modified_time": article.updated_at.isoformat(),
                "category_name": category.name if category is not None else "",
                "category_url": (
                    spa_url(f"category/{category.slug}") if category is not None else ""
                ),
                "article_jsonld": _json_ld(article_ld),
                "breadcrumb_jsonld": _json_ld(breadcrumb_ld),
            }
        )
        return context


@method_decorator(cache_control(public=True, max_age=3600), name="dispatch")
class RobotsTxtView(TemplateView):
    """``/robots.txt``, pointing at the public sitemap.

    Driven by ``settings.PUBLIC_BASE_URL`` so a staging or E2E host advertises
    its own sitemap instead of production's.
    """

    template_name = "seo/robots.txt"
    content_type = "text/plain; charset=utf-8"
    http_method_names = ["get", "head", "options"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "base_url": public_base_url(),
                "sitemap_url": spa_url("sitemap.xml"),
            }
        )
        return context
