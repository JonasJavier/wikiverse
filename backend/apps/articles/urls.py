"""Routes under ``/api/``.

Every collection endpoint is a **flat** path, never a DRF collection action on
``/api/articles/``: ``/api/articles/search/`` and ``/api/articles/<slug>/`` are
the same URL shape, so an article whose slug is ``search`` would shadow the
endpoint. The names that could collide live in
:data:`apps.common.utils.RESERVED_SLUGS`, and the flat layout means a new
endpoint cannot be shadowed at all (DECISIONS §2).
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet,
    CategoryViewSet,
    ChangesView,
    ContributionsView,
    MainPageView,
    RecentChangesFeed,
    SearchView,
    SiteStatsView,
    SuggestView,
    TalkMessageViewSet,
    TalkThreadViewSet,
    WantedPagesView,
    WatchlistView,
)

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="article")
router.register("categories", CategoryViewSet, basename="category")
router.register("talk/threads", TalkThreadViewSet, basename="talk-thread")
router.register("talk/messages", TalkMessageViewSet, basename="talk-message")

urlpatterns = [
    # Search (DECISIONS §2: these two paths, and no others)
    path("search/", SearchView.as_view(), name="search"),
    path("search/suggest/", SuggestView.as_view(), name="search-suggest"),
    # Change feeds
    path("changes/", ChangesView.as_view(), name="changes"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path(
        "users/<str:username>/contributions/",
        ContributionsView.as_view(),
        name="user-contributions",
    ),
    path("feeds/changes.rss", RecentChangesFeed(), name="changes-feed"),
    # Site
    path("main-page/", MainPageView.as_view(), name="main-page"),
    path("stats/", SiteStatsView.as_view(), name="site-stats"),
    path("wanted/", WantedPagesView.as_view(), name="wanted-pages"),
    *router.urls,
]
