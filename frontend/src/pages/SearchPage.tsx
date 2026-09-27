import type { FormEvent } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import { useCategories } from "@/api/categories";
import {
  DEFAULT_SEARCH_SORT,
  SEARCH_PAGE_SIZE,
  type SearchFacets,
  type SearchQuery,
  toSearchSort,
  useSearch,
} from "@/api/search";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { ResultRow, ResultRowSkeleton } from "@/components/search/ResultRow";
import {
  SearchFilters,
  type SearchFilterPatch,
} from "@/components/search/SearchFilters";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Input } from "@/components/ui/Field";
import { Pagination } from "@/components/ui/Pagination";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { cn, formatNumber } from "@/lib/utils";

/**
 * A result list is SCANNED, not read, so this column is deliberately narrower
 * than the article measure (Wikipedia measures 561px against its own 960px
 * article body; ours is 608px against 640px of prose).
 */
const COLUMN = "max-w-[38rem]";

/** U+2013 EN DASH. DECISIONS §10: `Results {start}–{end} of {count}`. */
const EN_DASH = "–";

/**
 * `/search?q=&ordering=&category=&author=&created_after=&created_before=&page=`
 *
 * The facet names are the API's own (DECISIONS §2), so the URL, the query key
 * and the request never need translating between three vocabularies. `from` /
 * `to` and `sort` are accepted as read-only aliases, because earlier drafts of
 * the spec used those names and a deep link written against them should still
 * land on the right results; everything this page writes is canonical.
 */
function readQuery(params: URLSearchParams): SearchQuery {
  const page = Number.parseInt(params.get("page") ?? "1", 10);

  return {
    q: params.get("q") ?? "",
    ordering: toSearchSort(params.get("ordering") ?? params.get("sort")),
    category: params.get("category") ?? "",
    author: params.get("author") ?? "",
    created_after: params.get("created_after") ?? params.get("from") ?? "",
    created_before: params.get("created_before") ?? params.get("to") ?? "",
    page: Number.isFinite(page) && page > 0 ? page : 1,
  };
}

/** Defaults are omitted, so a plain search stays a clean, shareable URL. */
function searchHref(query: SearchQuery): string {
  const params = new URLSearchParams();
  if (query.q) params.set("q", query.q);
  if (query.ordering !== DEFAULT_SEARCH_SORT) {
    params.set("ordering", query.ordering);
  }
  if (query.category) params.set("category", query.category);
  if (query.author) params.set("author", query.author);
  if (query.created_after) params.set("created_after", query.created_after);
  if (query.created_before) params.set("created_before", query.created_before);
  if (query.page > 1) params.set("page", String(query.page));
  const qs = params.toString();
  return qs ? `/search?${qs}` : "/search";
}

export function SearchPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const query = readQuery(params);
  const term = query.q.trim();

  const { data: categories } = useCategories();
  const { data, isLoading, isPlaceholderData, isError, error, refetch } =
    useSearch(query);

  useDocumentMeta({
    title: term ? `Search results for “${term}”` : "Search results",
    description:
      "Search the full text of every article in Wikiverse by title, body, contributor and category.",
    canonical: "/search",
    // One indexable page per ?q= would be duplicate-content sprawl. `follow`
    // still lets a crawler walk through to the articles themselves.
    robots: "noindex,follow",
  });

  /** Any facet change resets the page: page 7 of a different query is not a page. */
  function patch(next: SearchFilterPatch) {
    navigate(searchHref({ ...query, ...next, page: 1 }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const submitted = String(
      new FormData(event.currentTarget).get("q") ?? "",
    ).trim();
    navigate(searchHref({ ...query, q: submitted, page: 1 }));
  }

  const facets: SearchFacets = {
    category: query.category,
    author: query.author,
    created_after: query.created_after,
    created_before: query.created_before,
  };

  const count = data?.count ?? 0;
  const start = (query.page - 1) * SEARCH_PAGE_SIZE + 1;
  const end = Math.min(query.page * SEARCH_PAGE_SIZE, count);
  // While `keepPreviousData` is still serving the previous query's rows, the
  // count belongs to that query. Rendering it under the new heading is the bug
  // the old page shipped, so it is withheld rather than corrected afterwards.
  const showCount = Boolean(data) && !isPlaceholderData && count > 0;

  return (
    <WikiFrame>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          Search results
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          Search the full text of every article in Wikiverse.
        </p>
      </div>

      <div className={cn("mt-3", COLUMN)}>
        <form role="search" onSubmit={handleSubmit} className="flex gap-2">
          <label htmlFor="search-q" className="sr-only">
            Search Wikiverse
          </label>
          <Input
            id="search-q"
            name="q"
            type="search"
            key={term}
            defaultValue={term}
            placeholder="Search Wikiverse…"
            autoComplete="off"
            className="h-9"
          />
          <Button
            type="submit"
            variant="secondary"
            size="lg"
            className="h-9 shrink-0"
          >
            Search
          </Button>
        </form>

        <SearchFilters
          className="mt-3"
          values={facets}
          ordering={query.ordering}
          categories={categories}
          onChange={patch}
        />

        {showCount && (
          <p
            role="status"
            aria-live="polite"
            className="mt-3 text-xs tabular-nums text-ink-2"
          >
            Results {formatNumber(start)}
            {EN_DASH}
            {formatNumber(end)} of {formatNumber(count)} for{" "}
            <b className="font-semibold text-ink">{term}</b>
          </p>
        )}

        {data?.did_you_mean && (
          <p className="mt-2 text-ui">
            Did you mean:{" "}
            <Link
              to={searchHref({ ...query, q: data.did_you_mean, page: 1 })}
              className="text-link hover:underline"
            >
              {data.did_you_mean}
            </Link>
            ?
          </p>
        )}

        <div
          aria-busy={isLoading || isPlaceholderData}
          className={cn(
            "mt-3",
            isPlaceholderData && "opacity-60 transition-opacity duration-100",
          )}
        >
          {!term ? (
            <EmptyState
              title="Enter a search term."
              hint={
                <>
                  Search matches article titles and their full text. You can
                  also{" "}
                  <Link to="/browse" className="text-link hover:underline">
                    browse every article
                  </Link>
                  .
                </>
              }
            />
          ) : isError ? (
            <SearchError
              message={errorMessage(error)}
              onRetry={() => void refetch()}
            />
          ) : isLoading ? (
            <ol>
              {Array.from({ length: 5 }, (_, index) => (
                <ResultRowSkeleton key={index} />
              ))}
            </ol>
          ) : count === 0 ? (
            <NoResults
              term={term}
              filtered={hasFacets(facets)}
              onClearFacets={patch}
            />
          ) : (
            <ol>
              {data?.results.map((result) => (
                <ResultRow key={result.slug} result={result} />
              ))}
            </ol>
          )}
        </div>

        {term && !isError && count > 0 && (
          <Pagination
            page={query.page}
            count={count}
            pageSize={SEARCH_PAGE_SIZE}
            hrefFor={(page) => searchHref({ ...query, page })}
          />
        )}
      </div>
    </WikiFrame>
  );
}

function hasFacets(facets: SearchFacets): boolean {
  return Object.values(facets).some(Boolean);
}

/**
 * The wiki idiom rather than an apology: a query that matched nothing is an
 * invitation to write the article. The create link is styled as a RED LINK,
 * because that is precisely what it is — a page that does not exist yet
 * (DECISIONS §19).
 */
function NoResults({
  term,
  filtered,
  onClearFacets,
}: {
  term: string;
  filtered: boolean;
  onClearFacets: (patch: SearchFilterPatch) => void;
}) {
  return (
    <div className="rounded-chrome border border-rule-hair bg-panel px-4 py-6 text-ui">
      <p className="font-medium text-ink">No pages matched.</p>
      <p className="mt-1 text-ink-2">
        You can create the page{" "}
        <Link
          to={`/new?title=${encodeURIComponent(term)}`}
          title={`${term} (page does not exist)`}
          className="font-semibold text-link-red hover:underline"
        >
          “{term}”
        </Link>
        .
      </p>
      {filtered && (
        <p className="mt-3">
          <button
            type="button"
            onClick={() =>
              onClearFacets({
                category: "",
                author: "",
                created_after: "",
                created_before: "",
              })
            }
            className="cursor-pointer text-link hover:underline"
          >
            Clear all filters
          </button>{" "}
          <span className="text-ink-2">
            and search the whole encyclopedia again.
          </span>
        </p>
      )}
    </div>
  );
}

/**
 * A search that failed is a different thing from a search that found nothing,
 * and conflating the two sends a reader off to rewrite a perfectly good query.
 * `role="alert"`, because it appears after the fact.
 */
function SearchError({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  return (
    <div
      role="alert"
      className="rounded-chrome border border-rule-hair bg-panel px-4 py-6 text-ui"
    >
      <p className="font-medium text-ink">The search could not be completed.</p>
      <p className="mt-1 text-ink-2">{message}</p>
      <div className="mt-3">
        <Button variant="secondary" onClick={onRetry}>
          Try again
        </Button>
      </div>
    </div>
  );
}

/**
 * 429 is the one status worth naming: `/api/search/` has its own throttle
 * scope, and "you are searching faster than the limit allows" is actionable
 * where "Request failed with status code 429" is not.
 */
function errorMessage(error: unknown): string {
  const status =
    typeof error === "object" && error !== null && "response" in error
      ? (error as { response?: { status?: number } }).response?.status
      : undefined;

  if (status === 429) {
    return "Too many searches in a short time. Wait a moment and try again.";
  }
  if (status !== undefined && status >= 500) {
    return "The server could not answer the query. This is usually temporary.";
  }
  return "The connection to the server failed. Check that you are online, then try again.";
}
