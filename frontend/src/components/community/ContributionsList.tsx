import {
  contributionsQuery,
  FEED_PAGE_SIZE,
  useContributions,
} from "@/api/community";
import {
  ChangeDayGroups,
  ChangeLegend,
} from "@/components/community/ChangeRow";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { formatNumber } from "@/lib/utils";

/**
 * One contributor's edits: Recent-Changes rows with a different query
 * (`GET /api/users/{username}/contributions/`), day-grouped, newest first,
 * 50 per page.
 *
 * design-ui §4.15 puts a stats block — username, join date, edit count,
 * article count — at the head of this component. It is NOT here, because
 * `ProfilePage` already carries all four in its title-block tagline and
 * printing them twice, 40px apart, is the kind of duplication the density
 * rules exist to prevent. The `current` marker §4.15 asks for is on the rows,
 * where it belongs: it answers "is this edit still standing?" per edit.
 *
 * Pagination is `<Link>`-based prev/next carrying `?page=` — which is what
 * makes the back button, scroll restoration and page 2 of a crawl work.
 */

export interface ContributionsListProps {
  username: string;
  /** 1-based, read from the URL by the page. */
  page: number;
  /** Builds the URL for a page, preserving whatever else the page keeps there. */
  hrefForPage: (page: number) => string;
  /** `3` when an `h2` already names the section. Heading order is a gate. */
  headingLevel?: 2 | 3;
}

export function ContributionsList({
  username,
  page,
  hrefForPage,
  headingLevel = 3,
}: ContributionsListProps) {
  const query = useContributions(username, contributionsQuery(page));
  const rows = query.data?.results ?? [];

  if (query.isPending) {
    return (
      <div className="space-y-2" aria-busy="true">
        {Array.from({ length: 6 }).map((_, index) => (
          <Skeleton key={index} className="h-6 w-full" />
        ))}
      </div>
    );
  }

  if (query.isError) {
    return (
      <EmptyState
        title="Those contributions could not be loaded."
        hint="The account may have been removed. Try again in a moment."
      />
    );
  }

  if (rows.length === 0) {
    return (
      <EmptyState
        title="No edits yet."
        hint={`${username} has not saved a revision to any article.`}
      />
    );
  }

  return (
    <div>
      <p className="text-ui text-ink-2">
        <span className="tabular-nums">{formatNumber(query.data?.count ?? 0)}</span>{" "}
        {query.data?.count === 1 ? "edit" : "edits"}, newest first.
      </p>
      <ChangeLegend className="mt-1" />
      <ChangeDayGroups
        rows={rows}
        headingLevel={headingLevel}
        className="mt-3"
      />
      <Pagination
        page={page}
        count={query.data?.count ?? 0}
        pageSize={FEED_PAGE_SIZE}
        hrefFor={hrefForPage}
      />
    </div>
  );
}
