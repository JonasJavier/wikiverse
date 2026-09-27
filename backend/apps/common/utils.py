"""Small shared helpers: slugs, reserved names and word counting."""

from __future__ import annotations

import secrets

from django.db import IntegrityError, models, transaction
from django.utils.text import slugify

from apps.articles.markup import count_words, strip_markup

__all__ = [
    "RESERVED_SLUGS",
    "SYMBOL_MAP",
    "count_words",
    "strip_markup",
    "unique_slugify",
    "wiki_slug",
]

#: Slugs an article or a redirect may never take, because a collection route,
#: a router action or a frontend route already owns the path. Without this a
#: page called "Search" would permanently shadow ``/api/search/``.
RESERVED_SLUGS = frozenset(
    {
        # DRF router collection actions
        "random",
        "popular",
        "stats",
        "suggest",
        "search",
        "restore",
        # flat /api/ paths and frontend routes
        "admin",
        "api",
        "articles",
        "backlinks",
        "categories",
        "changes",
        "diff",
        "docs",
        "edit",
        "feeds",
        "health",
        "history",
        "info",
        "login",
        "logout",
        "main-page",
        "me",
        "new",
        "profile",
        "redoc",
        "register",
        "robots",
        "schema",
        "sitemap",
        "talk",
        "users",
        "wanted",
        "watch",
        "watchlist",
        "wiki",
    }
)

#: Symbols that :func:`slugify` would silently drop, mapped to something
#: readable. Without this, "C++", "C#" and "C" all slugify to ``c``.
SYMBOL_MAP = {
    "+": "-plus",
    "#": "-sharp",
    "&": "-and",
    "/": "-",
    "@": "-at",
    "%": "-percent",
    "°": "-degrees",
    "½": "one-half",
    "π": "pi",
    "Ω": "omega",
    "Σ": "sigma",
    "∞": "infinity",
    "√": "sqrt",
}

#: Appended when a title slugifies to nothing at all.
FALLBACK_SLUG = "untitled"


def wiki_slug(value: str, *, max_length: int = 220) -> str:
    """Slugify a wiki title, preserving non-Latin script.

    ``allow_unicode=True`` keeps "Erdős number" readable as ``erdős-number``
    instead of collapsing it to ``erd-s-number``; DRF's default
    ``lookup_value_regex`` routes it and the frontend encodes it. Symbols that
    carry meaning go through :data:`SYMBOL_MAP` first, so ``C++`` and ``C#`` do
    not both become ``c``.

    This must be the exact function that assigns article slugs, or every
    ``[[wikilink]]`` resolves to a red link.
    """
    text = (value or "").strip()
    for symbol, replacement in SYMBOL_MAP.items():
        if symbol in text:
            text = text.replace(symbol, replacement)
    slug = slugify(text, allow_unicode=True).strip("-")
    return slug[:max_length].strip("-")


def unique_slugify(
    instance: models.Model,
    value: str,
    slug_field_name: str = "slug",
    max_length: int = 220,
) -> str:
    """Set a unique, non-reserved slug on ``instance`` derived from ``value``.

    Appends ``-1``, ``-2``… until the slug is free, ignoring the instance's own
    row so re-saving keeps the slug stable. Reserved slugs are treated as taken.
    This is a check-then-insert, so it can still lose a race; the caller should
    wrap the insert in :func:`slug_collision_retry`.
    """
    base = wiki_slug(value, max_length=max_length) or FALLBACK_SLUG
    model = instance.__class__
    manager = model._default_manager
    slug = base
    counter = 1
    while (
        slug in RESERVED_SLUGS
        or manager.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists()
    ):
        suffix = f"-{counter}"
        slug = f"{base[: max_length - len(suffix)]}{suffix}"
        counter += 1
    setattr(instance, slug_field_name, slug)
    return slug


def slug_collision_retry(save, instance, slug_field_name: str = "slug", attempts: int = 3):
    """Call ``save()``, retrying with a random suffix on a slug collision.

    Two concurrent creates of the same title both pass the ``exists()`` check in
    :func:`unique_slugify` and the loser raises ``IntegrityError``. Returning a
    500 for that is wrong when a two-character suffix fixes it.
    """
    for attempt in range(attempts):
        try:
            with transaction.atomic():
                return save()
        except IntegrityError:
            if attempt == attempts - 1:
                raise
            current = getattr(instance, slug_field_name, "") or FALLBACK_SLUG
            suffix = f"-{secrets.token_hex(2)}"
            setattr(instance, slug_field_name, f"{current[: 220 - len(suffix)]}{suffix}")
    return None
