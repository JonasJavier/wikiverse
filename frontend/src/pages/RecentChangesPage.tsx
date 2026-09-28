import { Link, useSearchParams } from "react-router-dom";

import {
  CHANGE_DAY_OPTIONS,
  changesQuery,
  readChangeFilters,
  useChanges,
  writeChangeFilters,
} from "@/api/community";
import { ChangeFilters } from "@/components/community/ChangeFilters";
import {
  ChangeDayGroups,
  ChangeLegend,
} from "@/components/community/ChangeRow";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { formatNumber } from "@/lib/utils";

/**
 * `/changes` — DECISIONS §4 fixes this route, superseding design-ui §3.8's
 * `/recent-changes`; `Sidebar.tsx` already links here.
 *
 * Every filter is in the URL and nowhere else, so this view is shareable,
 * bookmarkable and survives the back button. `/api/changes/` pages by
 * TIMESTAMP CURSOR rather than by page number, because an append-at-the-head
 * feed cannot produce an honest `count` and page 2 of one shifts under the
 * reader; "Show older changes" therefore writes `?before=` into the URL,
 * which keeps even a position in the feed shareable.
 */
export function RecentChangesPage() {
  const [search] = useSearchParams();
  const state = readChangeFilters(search);
  const query = useChanges(changesQuery(state));

  useDocumentMeta({
    title: "Recent changes",
    description:
      "The most recent edits and talk-page posts across Wikiverse, newest first.",
    canonical: "/changes",
  });

  const rows = query.data?.results ?? [];
  // The next period up, offered when this one is empty.
  const wider = CHANGE_DAY_OPTIONS.find((days) => days > state.days);

  const olderSearch = new URLSearchParams(writeChangeFilters(state, {}));
  if (query.data?.next_before) {
    olderSearch.set("before", query.data.next_before);
  }

  return (
    <WikiFrame rail={<Sidebar />}>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          Recent changes
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          Track the most recent changes to Wikiverse.
        </p>
      </div>

      <ChangeFilters
        onRefresh={() => void query.refetch()}
        updatedAt={query.dataUpdatedAt || undefined}
        busy={query.isFetching}
        showFeedLink
      />

      {state.before && (
        <p className="mt-3 text-ui">
          <Link to={{ search: "" }} className="text-link hover:underline">
            {"← Back to the latest changes"}
          </Link>
        </p>
      )}

      <section aria-busy={query.isPending} className="mt-4">
        {query.isPending ? (
          <div className="space-y-2">
            {Array.from({ length: 10 }).map((_, index) => (
              <Skeleton key={index} className="h-6 w-full" />
            ))}
          </div>
        ) : query.isError ? (
          <EmptyState
            title="The changes feed could not be loaded."
            hint="The API did not answer. Use Refresh above to try again."
          />
        ) : rows.length === 0 ? (
          <EmptyState
            title="No changes in this period."
            hint={
              wider ? (
                <>
                  <Link
                    to={{ search: `?${writeChangeFilters(state, { days: wider })}` }}
                    className="text-link hover:underline"
                  >
                    Show the last {wider} days
                  </Link>
                  , or clear the contributor and category filters.
                </>
              ) : (
                "Clear the contributor and category filters."
              )
            }
          />
        ) : (
          <>
            <ChangeLegend />
            <ChangeDayGroups rows={rows} className="mt-3" />
            <p className="mt-6 flex flex-wrap items-baseline justify-between gap-2 border-t border-rule pt-3 text-ui text-ink-2">
              <span>
                Showing{" "}
                <span className="tabular-nums">{formatNumber(rows.length)}</span>{" "}
                {rows.length === 1 ? "change" : "changes"}.
              </span>
              {query.data?.has_more && query.data.next_before && (
                <Link
                  to={{ search: `?${olderSearch.toString()}` }}
                  rel="next"
                  className="text-link hover:underline"
                >
                  {"Show older changes →"}
                </Link>
              )}
            </p>
          </>
        )}
      </section>
    </WikiFrame>
  );
}
