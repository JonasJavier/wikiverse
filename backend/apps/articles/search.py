"""The search layer the API calls: full text, snippets, typeahead, spelling hints.

Everything here has two implementations and picks between them at **call time**
with :func:`apps.articles.querysets.is_postgres` (``connection.vendor ==
"postgresql"``). Never at import time: the test suite and local development run
on SQLite, production runs on PostgreSQL, and the same file has to serve both.
Never with ``try/except DatabaseError`` either --
:class:`~django.contrib.postgres.search.SearchHeadline` raises ``AttributeError``
on SQLite (``DatabaseOperations`` has no ``compose_sql``), which such a guard
would not catch.

The wire shape is identical on both backends; only result quality differs.

* :func:`search_articles` -- PostgreSQL: ``websearch_to_tsquery`` against the
  stored ``search_vector``, scored with ``ts_rank(..., 32)``, plus a ``pg_trgm``
  retry when the strict query finds nothing. SQLite: ``icontains`` over title,
  short_description, summary and content, scored by which column matched.
* :func:`headline` -- PostgreSQL: ``ts_headline`` with control-character
  selectors. SQLite: raises :class:`~django.db.utils.NotSupportedError`.
* :func:`suggest` -- PostgreSQL: prefix match ``OR`` trigram match, ordered
  prefix-first then by word similarity. SQLite: ``istartswith`` then
  ``icontains``, ordered prefix-first.
* :func:`did_you_mean` -- PostgreSQL: best ``similarity()`` over titles. SQLite:
  a bounded :mod:`difflib` scan over the most-viewed titles.
* :func:`safe_headline_to_marked` -- pure Python; identical everywhere.
"""

from __future__ import annotations

import difflib
import html
from typing import Any

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
    TrigramWordSimilarity,
)
from django.db import models
from django.db.models import Case, F, Q, Value, When
from django.db.models.functions import Greatest
from django.db.utils import NotSupportedError

from .querysets import TRIGRAM_FLOOR, is_postgres, search_config

__all__ = [
    "DEFAULT_ORDERING",
    "MARK_CLOSE",
    "MARK_OPEN",
    "ORDERINGS",
    "SENTINEL_START",
    "SENTINEL_STOP",
    "SUGGEST_LIMIT",
    "SUGGEST_MIN_CHARS",
    "did_you_mean",
    "headline",
    "normalize_ordering",
    "safe_headline_to_marked",
    "safe_term",
    "search_articles",
    "suggest",
]

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

#: Highlight delimiters handed to ``ts_headline``. STX and ETX are control
#: characters: they cannot occur in a Markdown body written through the API and
#: they carry no meaning in HTML, so escaping the headline and *then* swapping
#: them for tags is safe by construction. See :func:`safe_headline_to_marked`.
#: These two values must stay identical to the ones in
#: ``ArticleQuerySet.with_snippet``.
SENTINEL_START = chr(2)
SENTINEL_STOP = chr(3)

#: What the sentinels become, after escaping.
MARK_OPEN = "<mark>"
MARK_CLOSE = "</mark>"

#: Sort controls offered by ``/api/search/``. "most edited" is deliberately
#: absent.
ORDERING_RELEVANCE = "relevance"
ORDERING_NEWEST = "newest"
ORDERING_OLDEST = "oldest"
ORDERINGS = (ORDERING_RELEVANCE, ORDERING_NEWEST, ORDERING_OLDEST)
DEFAULT_ORDERING = ORDERING_RELEVANCE

#: Longest query string considered. Anything past this is noise or an attack;
#: ``websearch_to_tsquery`` would happily parse a megabyte.
MAX_TERM_LENGTH = 128

#: Typeahead: fewer than two characters matches most of the corpus, and 10 is a
#: hard cap, not a default -- the endpoint must not let a caller widen it.
SUGGEST_MIN_CHARS = 2
SUGGEST_LIMIT = 10
SUGGEST_MAX_TERM_LENGTH = 64

#: Columns a suggestion row carries: the gloss, never a body snippet.
SUGGEST_FIELDS = ("slug", "title", "short_description")

#: Rows the SQLite spelling-hint path may pull into memory. Bounded because
#: :mod:`difflib` is linear in the number of candidates; it only ever runs on
#: the zero-result path.
DID_YOU_MEAN_SCAN = 500

#: ``ts_headline`` options for a body snippet. Two fragments of ~28 words is the
#: shape the results list is laid out for.
BODY_HEADLINE_OPTIONS: dict[str, Any] = {
    "max_words": 28,
    "min_words": 12,
    "max_fragments": 2,
    "fragment_delimiter": " … ",
    "short_word": 3,
}

#: ``rank`` for a SQLite match, by the strongest column that matched. The
#: numbers only have to order sensibly among themselves -- they are not
#: comparable with ``ts_rank`` output, and no UI promises they are.
_SQLITE_SCORES: tuple[tuple[str, float], ...] = (
    ("title__iexact", 1.0),
    ("title__istartswith", 0.8),
    ("title__icontains", 0.6),
    ("short_description__icontains", 0.4),
    ("summary__icontains", 0.3),
)

#: Ordering applied once ``rank`` exists. A term is always present for
#: ``relevance``; ``_BLANK_ORDER`` covers the empty-``q`` case, which has to look
#: like an unfiltered article list.
_ORDER_BY: dict[str, tuple[str, ...]] = {
    ORDERING_RELEVANCE: ("-rank", "-view_count", "-updated_at"),
    ORDERING_NEWEST: ("-created_at", "-id"),
    ORDERING_OLDEST: ("created_at", "id"),
}
_BLANK_ORDER: dict[str, tuple[str, ...]] = {
    ORDERING_RELEVANCE: ("-updated_at",),
    ORDERING_NEWEST: ("-created_at", "-id"),
    ORDERING_OLDEST: ("created_at", "id"),
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def safe_term(term: str | None, *, max_length: int = MAX_TERM_LENGTH) -> str:
    """Normalise a user-supplied query: strip, then bound the length."""
    return (term or "").strip()[:max_length]


def normalize_ordering(value: str | None) -> str:
    """Map a client sort value onto :data:`ORDERINGS`, defaulting to relevance.

    An unknown value is not an error: the sort control is a convenience and a
    stale bookmark should still return results.
    """
    candidate = (value or "").strip().casefold()
    return candidate if candidate in ORDERINGS else DEFAULT_ORDERING


def _query(term: str) -> SearchQuery:
    """``websearch_to_tsquery(<config>, term)``. PostgreSQL only.

    ``websearch`` is the forgiving parser: it accepts quoted phrases, ``or``,
    and a leading ``-`` for exclusion, and it never raises on syntax a human
    typed -- which ``to_tsquery`` does.
    """
    return SearchQuery(term, search_type="websearch", config=search_config())


def _zero_rank() -> Value:
    """A constant ``rank`` so the serializer field always resolves."""
    return Value(0.0, output_field=models.FloatField())


def _sqlite_rank(term: str) -> Case:
    """Score a substring match by which column it hit."""
    whens = [When(**{lookup: term}, then=Value(score)) for lookup, score in _SQLITE_SCORES]
    return Case(*whens, default=Value(0.1), output_field=models.FloatField())


def _sqlite_search(queryset: models.QuerySet, term: str) -> models.QuerySet:
    """Substring search with a usable relevance score. Same shape as FTS."""
    return queryset.annotate(rank=_sqlite_rank(term)).filter(
        Q(title__icontains=term)
        | Q(short_description__icontains=term)
        | Q(summary__icontains=term)
        | Q(content__icontains=term)
    )


def _postgres_search(queryset: models.QuerySet, term: str) -> models.QuerySet:
    """Weighted ``tsvector`` match, scored with ``ts_rank``.

    The weights (title A, short_description and summary B, content C) are baked
    into the stored vector by the database trigger, so ``ts_rank``'s default
    weight array already gives a title hit five times the pull of a body hit.
    ``normalization=32`` is ``rank / (rank + 1)``, which squashes the score into
    ``(0, 1)`` and stops long articles from monopolising the top.
    """
    return queryset.annotate(
        rank=SearchRank(F("search_vector"), _query(term), normalization=Value(32))
    ).filter(search_vector=_query(term))


def _postgres_fuzzy(queryset: models.QuerySet, term: str) -> models.QuerySet:
    """``pg_trgm`` retry for misspellings.

    The ``%`` operator (``__trigram_similar``) does the filtering because it is
    index-backed by the ``gin_trgm_ops`` indexes; ``WORD_SIMILARITY`` in a
    ``WHERE`` clause is a sequential scan, so the function only scores the
    survivors of the indexed filter.
    """
    return (
        queryset.filter(Q(title__trigram_similar=term) | Q(short_description__trigram_similar=term))
        .annotate(
            rank=Greatest(
                TrigramWordSimilarity(term, "title"),
                TrigramWordSimilarity(term, "short_description"),
            )
        )
        .filter(rank__gte=TRIGRAM_FLOOR)
    )


def _articles() -> models.QuerySet:
    """Published articles. Imported lazily to keep this module import-safe."""
    from .models import Article

    return Article.objects.published()


# --------------------------------------------------------------------------- #
# Full-text search
# --------------------------------------------------------------------------- #
def search_articles(
    queryset: models.QuerySet,
    term: str | None,
    ordering: str | None = DEFAULT_ORDERING,
) -> models.QuerySet:
    """Return ``queryset`` filtered, annotated with ``rank``, and ordered.

    ``queryset`` must already be visibility-filtered by the caller
    (``Article.objects.visible(user)``); this function never widens it.

    ``rank`` is annotated on **every** path, including a blank ``term`` and the
    SQLite path, because ``SearchResultSerializer.rank`` is a required field --
    an unannotated queryset would raise at serialization time rather than at the
    query. A blank ``term`` filters nothing and behaves like an unfiltered
    article list.

    PostgreSQL: the strict ``tsvector`` query runs first; if it matches nothing,
    a trigram retry runs, so ``photosynthasis`` still finds *Photosynthesis*.
    That costs one extra ``EXISTS`` query, and only on the zero-result path.
    SQLite: a single substring pass, scored by which column matched.

    ``ordering`` is one of :data:`ORDERINGS`; anything else is treated as
    ``relevance``. ``newest`` and ``oldest`` order by ``created_at`` and still
    carry ``rank``, so switching sort does not change the response shape.
    """
    term = safe_term(term)
    order = normalize_ordering(ordering)

    if not term:
        return queryset.annotate(rank=_zero_rank()).order_by(*_BLANK_ORDER[order])

    if not is_postgres():
        return _sqlite_search(queryset, term).order_by(*_ORDER_BY[order])

    strict = _postgres_search(queryset, term)
    if strict.exists():
        return strict.order_by(*_ORDER_BY[order])
    return _postgres_fuzzy(queryset, term).order_by(*_ORDER_BY[order])


# --------------------------------------------------------------------------- #
# Snippets
# --------------------------------------------------------------------------- #
def headline(
    field_expression: str | models.Expression,
    term: str | None,
    *,
    highlight_all: bool = False,
    **options: Any,
) -> SearchHeadline:
    """Build a ``ts_headline`` annotation over ``field_expression``.

    The match delimiters are :data:`SENTINEL_START` and :data:`SENTINEL_STOP`,
    never HTML. Pass the annotated value through
    :func:`safe_headline_to_marked` before it reaches a serializer.

    ``highlight_all=True`` marks every match in the whole value instead of
    cutting fragments -- the right shape for a title, where the fragment options
    are meaningless and PostgreSQL ignores them anyway.

    PostgreSQL only, and it must be the **last** thing added to a queryset:
    ``SearchHeadline.as_sql()`` calls ``connection.ops.compose_sql()``, so
    compiling it needs a live PostgreSQL connection. On SQLite this raises
    :class:`~django.db.utils.NotSupportedError` at the call site rather than the
    bare ``AttributeError`` the expression itself would produce later, at SQL
    compile time, far from the code that caused it.
    """
    if not is_postgres():
        raise NotSupportedError(
            "ts_headline is PostgreSQL-only; gate the call on "
            "apps.articles.querysets.is_postgres() and fall back to the plain field."
        )
    term = safe_term(term)
    if not term:
        raise ValueError("headline() needs a non-blank term; there is nothing to highlight.")

    resolved: dict[str, Any] = {} if highlight_all else dict(BODY_HEADLINE_OPTIONS)
    if highlight_all:
        resolved["highlight_all"] = True
    resolved.update(options)
    return SearchHeadline(
        field_expression,
        _query(term),
        config=search_config(),
        start_sel=SENTINEL_START,
        stop_sel=SENTINEL_STOP,
        **resolved,
    )


def safe_headline_to_marked(raw: str | None) -> str:
    """Turn a sentinel-delimited headline into escaped, ``<mark>``-marked text.

    Escape first, substitute second. That order is the whole point of the
    sentinels, and getting it backwards is a stored cross-site-scripting hole:

    * ``ts_headline`` re-tokenises the **raw article body**, which any signed-in
      editor can write. Given ``StartSel='<mark>'`` directly, its output would be
      a mixture of trusted tags and untrusted body text -- including whatever
      ``<script>`` or ``<img onerror=...>`` an editor put in the article -- in a
      field the results list renders as markup. Escaping afterwards would
      destroy the real tags along with the injected ones, so there would be no
      way left to tell them apart.
    * With control characters as delimiters there is nothing to tell apart.
      ``html.escape()`` neutralises every ``<``, ``>``, ``&``, ``"`` and ``'``
      that came from the article, and only then are the two sentinels -- which no
      author can type through a JSON API, and which mean nothing in HTML --
      replaced by the only two tags this function is allowed to emit.

    So the strongest thing an attacker controls in the output is a bare
    ``<mark>`` or ``</mark>``: no attributes, no other tag, no entity, and
    therefore no script. Unbalanced sentinels are harmless for the same reason --
    the front end splits the string on those two literal tokens and builds React
    elements from the pieces, so a stray one renders as an empty highlight
    instead of leaking into the surrounding markup.

    ``None`` and ``""`` return ``""``, so a caller can pass a missing annotation
    straight through -- SQLite never produces one -- and fall back to ``summary``
    or ``title`` itself.
    """
    if not raw:
        return ""
    escaped = html.escape(str(raw))
    return escaped.replace(SENTINEL_START, MARK_OPEN).replace(SENTINEL_STOP, MARK_CLOSE)


# --------------------------------------------------------------------------- #
# Typeahead
# --------------------------------------------------------------------------- #
def suggest(
    term: str | None,
    limit: int = SUGGEST_LIMIT,
    *,
    queryset: models.QuerySet | None = None,
) -> list[dict[str, str]]:
    """At most ``limit`` typeahead rows of ``slug``, ``title``, ``short_description``.

    Built for keystroke-rate traffic: three short columns, no ``content``, no
    ``Revision``, no view-count write, one index-backed query, and a list of
    plain dicts that is cheap to cache in Redis as it stands. ``limit`` is
    clamped into ``1..10``: the cap is part of the endpoint contract, so a caller
    passing a client-supplied number cannot widen it.

    Fewer than :data:`SUGGEST_MIN_CHARS` characters returns ``[]`` without
    touching the database -- one letter matches most of the corpus.

    Results are prefix-biased on both backends: titles starting with the term
    come first, always. PostgreSQL then adds a trigram arm so a typo still
    suggests something (``photosynthasis`` finds *Photosynthesis*) and orders the
    remainder by word similarity; SQLite widens to ``icontains`` instead, which
    catches mid-title matches but no misspellings. Both fall back to
    ``-view_count`` then title, so the order is stable.

    ``queryset`` defaults to published, non-deleted articles; pass one to narrow
    it further.
    """
    term = safe_term(term, max_length=SUGGEST_MAX_TERM_LENGTH)
    if len(term) < SUGGEST_MIN_CHARS:
        return []
    limit = max(1, min(int(limit or SUGGEST_LIMIT), SUGGEST_LIMIT))

    base = _articles() if queryset is None else queryset
    starts = Case(
        When(title__istartswith=term, then=Value(1)),
        default=Value(0),
        output_field=models.IntegerField(),
    )

    if not is_postgres():
        rows = (
            base.filter(Q(title__istartswith=term) | Q(title__icontains=term))
            .annotate(starts=starts)
            .order_by("-starts", "-view_count", "title")
        )
    else:
        rows = (
            base.filter(Q(title__istartswith=term) | Q(title__trigram_similar=term))
            .annotate(starts=starts, similarity=TrigramWordSimilarity(term, "title"))
            .order_by("-starts", "-similarity", "-view_count", "title")
        )
    return list(rows.values(*SUGGEST_FIELDS)[:limit])


# --------------------------------------------------------------------------- #
# Spelling hints
# --------------------------------------------------------------------------- #
def did_you_mean(term: str | None, *, queryset: models.QuerySet | None = None) -> str | None:
    """The single best title correction for ``term``, or ``None``.

    Call this only when a search returned nothing: it is a second query, and a
    correction shown next to results reads as a bug.

    PostgreSQL: the ``%`` operator narrows to trigram-similar titles using the
    index, ``similarity()`` scores them, and the floor is
    :data:`~apps.articles.querysets.TRIGRAM_FLOOR` -- 0.30, calibrated so that
    ``postgersql`` finds *PostgreSQL* (0.467) while noise does not survive.
    SQLite has no ``pg_trgm``, so it scans the titles of the
    :data:`DID_YOU_MEAN_SCAN` most-viewed articles through :mod:`difflib` at the
    same cutoff -- bounded, and only ever on the zero-result path.

    A title equal to the term is never suggested, on either backend.
    """
    term = safe_term(term)
    if len(term) < SUGGEST_MIN_CHARS:
        return None

    base = (_articles() if queryset is None else queryset).exclude(title__iexact=term)

    if not is_postgres():
        titles = list(
            base.order_by("-view_count").values_list("title", flat=True)[:DID_YOU_MEAN_SCAN]
        )
        matches = difflib.get_close_matches(term, titles, n=1, cutoff=TRIGRAM_FLOOR)
        return matches[0] if matches else None

    return (
        base.filter(title__trigram_similar=term)
        .annotate(similarity=TrigramSimilarity("title", term))
        .filter(similarity__gte=TRIGRAM_FLOOR)
        .order_by("-similarity", "-view_count", "title")
        .values_list("title", flat=True)
        .first()
    )
