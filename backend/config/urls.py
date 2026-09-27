"""Root URL configuration for Wikiverse.

Three routes here are not part of the JSON API and are easy to mis-wire:

* ``sitemap.xml`` **must** keep the URL name
  ``django.contrib.sitemaps.views.sitemap`` — ``sitemaps.views.index`` reverses
  that exact name.
* ``og/wiki/<slug>/`` uses ``<str:slug>``, not ``<slug:slug>``. Slugs come from
  ``wiki_slug()``, which runs ``slugify(allow_unicode=True)``, so real slugs
  contain characters such as ``ł`` and ``ö``; Django's ``slug`` converter is
  ASCII-only and would 404 them.
* ``/api/ready/`` is the deep readiness probe and is deliberately *not* what the
  platform health check points at — that is ``/api/health/``, which touches
  nothing.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.common.seo import ArticleOpenGraphView, RobotsTxtView
from apps.common.sitemaps import SITEMAPS
from apps.common.views import health_check, readiness_check

urlpatterns = [
    path("admin/", admin.site.urls),
    # Health / ops
    path("api/health/", health_check, name="health"),
    path("api/ready/", readiness_check, name="ready"),
    # Auth
    path("api/auth/", include("apps.accounts.urls")),
    # Domain
    path("api/", include("apps.articles.urls")),
    # API schema & interactive docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Crawler surface (DECISIONS §16). nginx routes only social preview bots at
    # the Open Graph shell; humans and JS-rendering crawlers never see it.
    path("og/wiki/<str:slug>/", ArticleOpenGraphView.as_view(), name="article-og"),
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path(
        "sitemap.xml",
        cache_page(3600)(sitemap),
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Same document on the API host, so a staging backend advertises its own.
    path("api/sitemap.xml", cache_page(3600)(sitemap), {"sitemaps": SITEMAPS}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
