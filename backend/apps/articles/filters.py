"""Query-parameter filters for the article and feed endpoints.

``rest_framework.filters.SearchFilter`` is deliberately **not** used anywhere:
with no ``search_fields`` it is a no-op that still advertises a ``search``
parameter in the schema. The ``search`` parameter is implemented here instead, so
it goes through :func:`apps.articles.search.search_articles` and gets the same
ranking, the same PostgreSQL/SQLite split and the same ``rank`` annotation as
``/api/search/``.
"""

from __future__ import annotations

import django_filters
from django.db.models import Q, QuerySet

from apps.articles.search import search_articles

from .models import Article

__all__ = ["ArticleFilter", "SearchFilter"]


class ArticleFilter(django_filters.FilterSet):
    """``GET /api/articles/``."""

    search = django_filters.CharFilter(
        method="filter_search",
        label="Full-text search (ranked; same engine as /api/search/)",
    )
    category = django_filters.CharFilter(field_name="category__slug", label="Primary category slug")
    any_category = django_filters.CharFilter(
        method="filter_any_category",
        label="Category slug, primary or additional",
    )
    author = django_filters.CharFilter(field_name="author__username", label="Author username")
    page_type = django_filters.ChoiceFilter(
        choices=Article.PageType.choices, label="article | disambiguation | list"
    )
    protection = django_filters.ChoiceFilter(choices=Article.Protection.choices)
    is_stub = django_filters.BooleanFilter()
    is_deleted = django_filters.BooleanFilter(label="Staff only; other callers never see these")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_after = django_filters.IsoDateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_before = django_filters.IsoDateTimeFilter(field_name="updated_at", lookup_expr="lte")

    class Meta:
        model = Article
        fields = [
            "search",
            "category",
            "any_category",
            "author",
            "page_type",
            "protection",
            "is_stub",
            "is_deleted",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
        ]

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """Rank-ordered search, so ``?search=`` and ``/api/search/`` agree."""
        return search_articles(queryset, value)

    def filter_any_category(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """Primary *or* additional category (DECISIONS §13).

        ``distinct()`` is required: the ``extra_categories`` join fans out one row
        per matching category.
        """
        if not value:
            return queryset
        return queryset.filter(Q(category__slug=value) | Q(extra_categories__slug=value)).distinct()


class SearchFilter(django_filters.FilterSet):
    """``GET /api/search/`` — the facets beside the query box.

    ``q`` and ``ordering`` are handled by the view, not here: they change the
    queryset's *shape* (annotation and ordering) rather than narrowing it, and
    ``ts_headline`` must be the last thing annotated.
    """

    category = django_filters.CharFilter(field_name="category__slug")
    author = django_filters.CharFilter(field_name="author__username")
    page_type = django_filters.ChoiceFilter(choices=Article.PageType.choices)
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Article
        fields = ["category", "author", "page_type", "created_after", "created_before"]
