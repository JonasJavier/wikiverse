import { Link, useSearchParams } from "react-router-dom";

import {
  changeFiltersWithPage,
  FEED_PAGE_SIZE,
  feedQuery,
  readChangeFilters,
  useWatchlist,
} from "@/api/community";
import { ChangeFilters } from "@/components/community/ChangeFilters";
import {
  ChangeDayGroups,
  ChangeLegend,
} from "@/components/community/ChangeRow";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { formatNumber } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";

/**
 * `/watchlist` — the same rows as Recent changes, filtered to the articles
 * this reader watches.
 *
 * THREE CONTROLS FROM design-ui §5.11 ARE DELIBERATELY ABSENT, because no
 * backend exists behind any of them and a dead button is worse than no button
 * (the reasoning DECISIONS §12 applies to Subscribe):
 *
 *   - *"Your watchlist contains 18 pages"* — `/api/watchlist/` returns
 *     CHANGES, not watched pages, so `count` is a number of edits. Printing it
 *     as a page count would be a lie; this page prints what the number is.
 *   - *"Rows changed since your last visit"* — there is no `last_visit`
 *     column on `Watch`, so there is nothing to compare against.
 *   - *"Edit raw watchlist"* and *"Mark all as visited"* — neither endpoint
 *     exists. The star beside an article title is the whole write path.
 *
 * The page is rendered signed-out too, as an invitation rather than a
 * redirect: a reader who lands on a shared `/watchlist` link should be told
 * what it is, not bounced to a login form with no explanation.
 */
export function WatchlistPage() {
  const [search] = useSearchParams();
  const state = readChangeFilters(search);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const query = useWatchlist(feedQuery(state), isAuthenticated);

  useDocumentMeta({
    title: "Watchlist",
    description: "Changes to the pages you are watching.",
    canonical: "/watchlist",
    robots: "noindex",
  });

  const rows = query.data?.results ?? [];
  const count = query.data?.count ?? 0;

  return (
    <WikiFrame rail={<Sidebar />}>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          Watchlist
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          Changes to the pages you are watching, newest first.
        </p>
      </div>

      {!isAuthenticated ? (
        <EmptyState
          title="Sign in to keep a watchlist."
          hint="The star beside an article title adds that article here, and this page then shows every change to it."
          action={
            <Link to="/login" className={buttonVariants()}>
              Sign in
            </Link>
          }
        />
      ) : (
        <>
          <ChangeFilters
            variant="watchlist"
            onRefresh={() => void query.refetch()}
            updatedAt={query.dataUpdatedAt || undefined}
            busy={query.isFetching}
          />

          <section aria-busy={query.isPending} className="mt-4">
            {query.isPending ? (
              <div className="space-y-2">
                {Array.from({ length: 8 }).map((_, index) => (
                  <Skeleton key={index} className="h-6 w-full" />
                ))}
              </div>
            ) : query.isError ? (
              <EmptyState
                title="Your watchlist could not be loaded."
                hint="The API did not answer. Use Refresh above to try again."
              />
            ) : rows.length === 0 ? (
              <EmptyState
                title="You are not watching any pages."
                hint="The star beside an article title adds it here. If you are already watching pages, none of them changed in this period — widen it above."
              />
            ) : (
              <>
                <p className="text-ui text-ink-2">
                  <span className="tabular-nums">{formatNumber(count)}</span>{" "}
                  {count === 1 ? "change" : "changes"} to the pages you watch in
                  the last{" "}
                  <span className="tabular-nums">{state.days}</span>{" "}
                  {state.days === 1 ? "day" : "days"}.
                </p>
                <ChangeLegend className="mt-1" />
                <ChangeDayGroups rows={rows} className="mt-3" />
                <Pagination
                  page={state.page}
                  count={count}
                  pageSize={FEED_PAGE_SIZE}
                  hrefFor={(page) =>
                    `?${changeFiltersWithPage(state, page).toString()}`
                  }
                />
              </>
            )}
          </section>
        </>
      )}
    </WikiFrame>
  );
}
