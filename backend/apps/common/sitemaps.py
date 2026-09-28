"""Sitemaps that always advertise the public SPA, never the API host.

The trap this module exists to avoid: ``django.contrib.sitemaps.views.sitemap``
resolves the host with ``get_current_site(request)``, which -- with
``django.contrib.sites`` uninstalled -- returns ``RequestSite(request)``. nginx
proxies ``/sitemap.xml`` to the backend with
``proxy_set_header Host <backend>.up.railway.app``, so the generated sitemap
would be full of URLs on a host that serves JSON instead of the encyclopedia.

:class:`PublicSitemap` therefore overrides :meth:`get_domain` and
:attr:`protocol` and ignores the request entirely: the host comes from
``settings.PUBLIC_SITE_DOMAIN`` and the scheme from ``settings.PUBLIC_BASE_URL``,
both read at request time (see :mod:`apps.common.seo`) so an E2E run can
override them.
"""

from __future__ import annotations

from typing import Any

from django.contrib.sitemaps import Sitemap

from apps.common.seo import encode_path, site_domain, site_protocol

__all__ = [
    "SITEMAPS",
    "ArticleSitemap",
    "CategorySitemap",
    "PublicSitemap",
    "StaticSitemap",
]

#: Real SPA routes worth listing. ``/search`` is deliberately absent: infinite
#: ``?q=`` permutations are a genuine duplicate-content problem for a wiki, and
#: ``robots.txt`` disallows it. Authenticated and editor routes are absent too.
STATIC_ROUTES: tuple[str, ...] = ("/", "/browse", "/categories", "/changes")

STATIC_ROUTE_META: dict[str, tuple[str, float]] = {
    "/": ("daily", 1.0),
    "/browse": ("daily", 0.7),
    "/categories": ("weekly", 0.6),
    "/changes": ("hourly", 0.4),
}


class PublicSitemap(Sitemap):
    """Base class emitting the public SPA origin rather than the request host."""

    @property
    def protocol(self) -> str:  # type: ignore[override]
        """Derived from ``settings.PUBLIC_BASE_URL``, never hardcoded."""
        return site_protocol()

    def get_protocol(self, protocol: str | None = None) -> str:
        return site_protocol()

    def get_domain(self, site: Any = None) -> str:
        """Ignore the request's ``Host`` -- see the module docstring."""
        return site_domain()


class ArticleSitemap(PublicSitemap):
    """Every crawlable article.

    ``items()`` is exactly ``is_published=True, is_deleted=False`` and excludes
    nothing else (DECISIONS section 16): stubs, disambiguation pages and list
    pages are all real encyclopedia pages and all belong in the index.
    """

    changefreq = "weekly"
    priority = 0.8
    limit = 5000

    def items(self):
        from apps.articles.models import Article

        return (
            Article.objects.filter(is_published=True, is_deleted=False)
            .order_by("slug")
            .only("slug", "updated_at")
        )

    def location(self, item) -> str:
        return encode_path(f"/wiki/{item.slug}")

    def lastmod(self, item):
        return item.updated_at


class CategorySitemap(PublicSitemap):
    """Category index pages.

    ``Category`` has no ``updated_at`` column, so ``lastmod`` is the newest
    ``updated_at`` among the category's crawlable articles, annotated in a
    single query. It is ``None`` for an empty category, which simply omits the
    element for that URL.
    """

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        from django.db.models import Max, Q

        from apps.articles.models import Category

        return (
            Category.objects.annotate(
                latest_article_updated=Max(
                    "articles__updated_at",
                    filter=Q(articles__is_published=True, articles__is_deleted=False),
                )
            )
            .order_by("slug")
            .only("slug")
        )

    def location(self, item) -> str:
        return encode_path(f"/category/{item.slug}")

    def lastmod(self, item):
        return getattr(item, "latest_article_updated", None)


class StaticSitemap(PublicSitemap):
    """The handful of real static SPA routes."""

    def items(self) -> list[str]:
        return list(STATIC_ROUTES)

    def location(self, item: str) -> str:
        return item

    def changefreq(self, item: str) -> str:
        return STATIC_ROUTE_META.get(item, ("weekly", 0.5))[0]

    def priority(self, item: str) -> float:
        return STATIC_ROUTE_META.get(item, ("weekly", 0.5))[1]


#: Mount with
#: ``path("sitemap.xml", cache_page(3600)(sitemap), {"sitemaps": SITEMAPS},
#: name="django.contrib.sitemaps.views.sitemap")``.
#: Classes, not instances, so each request builds fresh querysets.
SITEMAPS: dict[str, type[PublicSitemap]] = {
    "static": StaticSitemap,
    "articles": ArticleSitemap,
    "categories": CategorySitemap,
}
