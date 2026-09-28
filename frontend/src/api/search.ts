import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { SearchResponse, SearchSort, Suggestion } from "@/lib/types";

/* =====================================================================
   THE SEARCH ENDPOINTS — the only two that exist (DECISIONS §2)
   =====================================================================
     GET /api/search/?q=           full results page, 20 per page
     GET /api/search/suggest/?q=   typeahead, hard-capped at 10 rows, and
                                   ALSO the 404 page's "similar titles"

   There is no /api/articles/search/, no /api/articles/suggest/ and no
   /api/search/similar/. This module is deliberately separate from
   `api/articles.ts`: `/api/articles/` is a different endpoint with
   different parameters (`search`, `ordering=-updated_at`, …) and no
   `snippet`, `rank` or `did_you_mean`. Reusing `useArticles` for the
   results page is the specific mistake this file exists to prevent.
   ===================================================================== */

/** DECISIONS §10. The UI labels read "Previous 20" / "Next 20". */
export const SEARCH_PAGE_SIZE = 20;

/** DECISIONS §10 — a hard cap on the server; no `limit` parameter exists. */
export const SUGGEST_LIMIT = 10;

/** The server returns `[]` below this, so there is no point asking. */
export const MIN_SUGGEST_LENGTH = 2;

/** The sort control offers exactly these three. "most edited" was cut. */
export const SEARCH_SORTS: readonly { value: SearchSort; label: string }[] = [
  { value: "relevance", label: "Relevance" },
  { value: "newest", label: "Newest first" },
  { value: "oldest", label: "Oldest first" },
];

export const DEFAULT_SEARCH_SORT: SearchSort = "relevance";

/** Narrow an untrusted URL value onto the three legal sorts. */
export function toSearchSort(value: string | null | undefined): SearchSort {
  return SEARCH_SORTS.some((s) => s.value === value)
    ? (value as SearchSort)
    : DEFAULT_SEARCH_SORT;
}

/**
 * The four facets beside the query box, named exactly as the API names them
 * (`SearchFilter` in `apps/articles/filters.py`), so the URL, the query key
 * and the request agree and nothing has to be translated twice.
 *
 * The two dates are held as the reader typed them — `"YYYY-MM-DD"` from an
 * `<input type="date">` — and widened to instants only at the request
 * boundary (see `searchRequestParams`).
 */
export interface SearchFacets {
  category: string;
  author: string;
  created_after: string;
  created_before: string;
}

export const EMPTY_FACETS: SearchFacets = {
  category: "",
  author: "",
  created_after: "",
  created_before: "",
};

export interface SearchQuery extends SearchFacets {
  q: string;
  ordering: SearchSort;
  /** 1-based, as it appears in the URL. */
  page: number;
}

export const searchKeys = {
  all: ["search"] as const,
  results: (query: SearchQuery) => ["search", "results", query] as const,
  suggest: (q: string) => ["search", "suggest", q] as const,
};

/**
 * `created_after` / `created_before` are `IsoDateTimeFilter`s, so a date is
 * widened to an instant here rather than in the URL — the URL keeps what the
 * reader picked, which is what makes it shareable and re-editable.
 *
 * Widening at the request boundary is not cosmetic. A bare `"2026-01-01"` does
 * parse (Django 5 accepts a date through `fromisoformat` — verified against the
 * installed 5.2), but it parses to *midnight*, which silently excludes the
 * whole of the named day from `created_before` — an off-by-one-day the reader
 * would have no way to see. And a naive value is interpreted in the server's
 * timezone, so the same URL would select a different window depending on where
 * it was answered. `T00:00:00Z` / `T23:59:59Z` makes the window inclusive at
 * both ends and identical for every reader.
 */
function startOfDay(date: string): string {
  return `${date}T00:00:00Z`;
}

function endOfDay(date: string): string {
  return `${date}T23:59:59Z`;
}

/** The exact query string sent to `GET /api/search/`. Empty facets are omitted. */
export function searchRequestParams(query: SearchQuery): Record<string, string> {
  const params: Record<string, string> = {
    q: query.q.trim(),
    ordering: query.ordering,
    page: String(Math.max(1, query.page)),
    page_size: String(SEARCH_PAGE_SIZE),
  };
  if (query.category) params.category = query.category;
  if (query.author) params.author = query.author.trim();
  if (query.created_after) params.created_after = startOfDay(query.created_after);
  if (query.created_before) params.created_before = endOfDay(query.created_before);
  return params;
}

/**
 * The results page. `enabled` is false on a bare `/search`, because the
 * endpoint answers a blank `q` with "the newest articles" — which is a
 * different page, and firing it means the reader's first paint is a list they
 * did not ask for.
 *
 * `keepPreviousData` is what stops the list flashing empty between pages; the
 * page compensates for it by dimming the list and hiding the stale count
 * while `isPlaceholderData` is true (see `SearchPage`).
 */
export function useSearch(query: SearchQuery) {
  const term = query.q.trim();
  const normalised: SearchQuery = { ...query, q: term };

  return useQuery({
    queryKey: searchKeys.results(normalised),
    queryFn: async ({ signal }) => {
      const { data } = await api.get<SearchResponse>("/search/", {
        params: searchRequestParams(normalised),
        signal,
      });
      return data;
    },
    enabled: term.length > 0,
    placeholderData: keepPreviousData,
    staleTime: 60_000,
  });
}

/**
 * `GET /api/search/suggest/?q=` — the typeahead, and the 404 page's "Similar
 * titles". One endpoint, one hook: DECISIONS §2 is explicit that there is no
 * separate similar-titles endpoint.
 *
 * On PostgreSQL this is a prefix match OR a trigram match, so it answers a
 * misspelling; on SQLite it degrades to `icontains`. Either way the row
 * carries the article's gloss rather than a body snippet, which is what makes
 * a list of ten titles scannable.
 */
export function useSuggest(term: string, options?: { enabled?: boolean }) {
  const q = term.trim();

  return useQuery({
    queryKey: searchKeys.suggest(q),
    queryFn: async ({ signal }) => {
      const { data } = await api.get<Suggestion[]>("/search/suggest/", {
        params: { q },
        signal,
      });
      return data;
    },
    enabled: (options?.enabled ?? true) && q.length >= MIN_SUGGEST_LENGTH,
    staleTime: 5 * 60_000,
  });
}
