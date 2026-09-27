"""The Wikiverse seed corpus.

=============================================================================
CONTENT LICENCE — this package only
=============================================================================
The article text in this package (``apps/articles/management/commands/_seed_data/**``)
is licensed under the **Creative Commons Attribution 4.0 International
licence** (CC BY 4.0), <https://creativecommons.org/licenses/by/4.0/>.

Attribution: "Wikiverse seed corpus". Each article carries its own
``references`` list naming the sources the text was written from; those sources
keep their own licences and are cited, not copied.

The licence applies to the *content* modules in this package and to nothing
else in the repository: the surrounding application code is covered by the
project licence (DECISIONS §18).
=============================================================================

Layout (DECISIONS §19): every sibling module in this package exports
``ARTICLES: list[SeedArticle]``. This module discovers them with :mod:`pkgutil`
and concatenates them in module-name order, so the corpus grows by *adding a
file* — nothing here counts modules and nothing here counts articles.

The corpus currently holds 63 of the 120 titles planned in
``docs/content-plan.json``. That is deliberate: authoring of the remainder was
stopped by the owner and will resume. A ``[[wikilink]]`` to a planned but
unwritten title is a **red link**, not an error (DECISIONS §19, RED LINKS), so
every count anything reports must come from the data rather than from a
constant.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any

__all__ = ["ARTICLES", "iter_modules", "load_articles"]

#: Modules in this package that are machinery rather than content.
_NOT_CONTENT = frozenset({"meta"})


def iter_modules() -> list[str]:
    """Return the names of the content modules, in a stable order.

    Private modules (``_foo``), this ``__init__`` and :data:`_NOT_CONTENT` are
    skipped; everything else is imported and kept only if it exposes
    ``ARTICLES``. Sorting by name is what makes the concatenated corpus — and
    therefore every id the seed assigns — reproducible.
    """
    found: list[str] = []
    for info in pkgutil.iter_modules(__path__):
        if info.ispkg or info.name.startswith("_") or info.name in _NOT_CONTENT:
            continue
        module = importlib.import_module(f"{__name__}.{info.name}")
        if isinstance(getattr(module, "ARTICLES", None), list):
            found.append(info.name)
    return sorted(found)


def load_articles() -> list[dict[str, Any]]:
    """Concatenate ``ARTICLES`` from every content module.

    The dicts are the modules' own objects, not copies: the seed treats them as
    read-only, and sharing them keeps a 63-article import cheap.
    """
    articles: list[dict[str, Any]] = []
    for name in iter_modules():
        module = importlib.import_module(f"{__name__}.{name}")
        articles.extend(module.ARTICLES)
    return articles


#: The whole corpus, in module-name order. Import this, not the modules.
ARTICLES: list[dict[str, Any]] = load_articles()
