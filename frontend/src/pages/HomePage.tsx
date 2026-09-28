import { Link } from "react-router-dom";

import { buildCategoryTree, useCategories } from "@/api/categories";
import { useLatestChanges, useMainPage } from "@/api/mainpage";
import { useArticleLinkResolver } from "@/components/article/markdownUtils";
import { CategoryTree } from "@/components/mainpage/CategoryTree";
import { DidYouKnow } from "@/components/mainpage/DidYouKnow";
import { FeaturedArticle } from "@/components/mainpage/FeaturedArticle";
import { OnThisDay } from "@/components/mainpage/OnThisDay";
import { Panel } from "@/components/mainpage/Panel";
import { SiteStatistics } from "@/components/mainpage/SiteStatistics";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import type { ChangeRow } from "@/lib/types";
import {
  byteDeltaTone,
  changeRowKey,
  formatByteDelta,
  formatRelativeTime,
  formatDateTime,
  formatNumber,
} from "@/lib/utils";

/**
 * The main page — an encyclopedia front page, not a landing page.
 *
 * What used to be here: a full-viewport hero with a radial dotted background,
 * a blurred indigo blob, the headline "The encyclopedia anyone can read &
 * write", a four-tile KPI strip, two 3-up card grids and a solid-indigo
 * call-to-action block. The first fact on the page sat below the fold. All of
 * it is deleted.
 *
 * What replaces it: the masthead, then bordered panels of real content —
 * Featured article, Did you know…, On this day, Recent changes, Browse by
 * category — and the statistics as one sentence. Target: a fact within 200px.
 *
 * There is NO "In the news" panel. DECISIONS §5 cut it: a fabricated news feed
 * on a demo encyclopedia reads as fake and is stale the day after it ships.
 *
 * Nothing on this page animates, nothing has a shadow, and nothing lifts on
 * hover.
 */
export function HomePage() {
  const { data, isPending, isError } = useMainPage();
  const { data: categories } = useCategories();
  const { data: changes } = useLatestChanges(8);
  // The article surface's own resolver, fed by `GET /api/wanted/` when no
  // article's link rows are in hand: one cached request, and the front page's
  // red links agree with an article body's by construction.
  const resolve = useArticleLinkResolver(undefined);

  useDocumentMeta({
    // `undefined` yields the site default, `Wikiverse — the open encyclopedia`.
    title: null,
    description:
      "Wikiverse is an open encyclopedia. Read the featured article, browse every category, and follow the latest changes.",
    canonical: "/",
    image: data?.featured?.lead_image_url ?? null,
    imageAlt: data?.featured?.lead_image_alt ?? null,
  });

  const branches = buildCategoryTree(categories);
  const articleCount = data?.stats.articles;

  return (
    <WikiFrame rail={<Sidebar />} paper={false}>
      <div className="pt-4 pb-16">
        <div>
          <h1 className="font-serif text-display font-normal text-ink">
            Welcome to Wikiverse
          </h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <p className="mt-1.5 text-ui text-ink-2 tabular-nums">
            the open encyclopedia —{" "}
            {articleCount === undefined
              ? "loading the corpus"
              : `${formatNumber(articleCount)} article${articleCount === 1 ? "" : "s"} in English`}
          </p>
        </div>

        {isError ? (
          <EmptyState
            className="mt-5"
            title="The main page could not be loaded."
            hint={
              <>
                The API did not answer.{" "}
                <Link to="/browse" className="text-link hover:underline">
                  Browse all articles
                </Link>{" "}
                or{" "}
                <Link to="/search" className="text-link hover:underline">
                  search
                </Link>{" "}
                instead.
              </>
            }
          />
        ) : (
          <>
            {/* The masthead grid: Featured spans both columns, because a
                floated lead image inside a half-width panel leaves ~230px of
                measure and the extract stops being readable. Below it the
                panels pair off, which is the two-column reading the front
                page is meant to have. */}
            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <Panel
                title="Featured article"
                busy={isPending}
                className="md:col-span-2"
              >
                {isPending ? (
                  <FeaturedSkeleton />
                ) : (
                  <FeaturedArticle
                    featured={data?.featured}
                    recentlyFeatured={data?.recently_featured ?? []}
                  />
                )}
              </Panel>

              <Panel title="Did you know…" busy={isPending}>
                {isPending ? (
                  <LineSkeleton lines={5} />
                ) : (
                  <DidYouKnow hooks={data?.dyk ?? []} resolve={resolve} />
                )}
              </Panel>

              <Panel title="On this day" busy={isPending}>
                {isPending ? (
                  <LineSkeleton lines={4} />
                ) : (
                  <OnThisDay entries={data?.otd ?? []} resolve={resolve} />
                )}
              </Panel>

              <Panel
                title="Recent changes"
                busy={!changes}
                action={
                  <Link to="/changes" className="text-link hover:underline">
                    All recent changes →
                  </Link>
                }
              >
                {changes ? (
                  <RecentChangesList rows={changes.results.slice(0, 8)} />
                ) : (
                  <LineSkeleton lines={6} />
                )}
              </Panel>

              <Panel
                title="Browse by category"
                busy={!categories}
                action={
                  <Link to="/categories" className="text-link hover:underline">
                    All categories →
                  </Link>
                }
              >
                {categories ? (
                  <CategoryTree branches={branches} variant="columns" />
                ) : (
                  <LineSkeleton lines={4} />
                )}
              </Panel>
            </div>

            <SiteStatistics
              stats={data?.stats}
              className="mt-4 text-ui text-ink-2"
            />
          </>
        )}
      </div>
    </WikiFrame>
  );
}

/**
 * The eight newest rows of the change feed, in the wiki's own order: time,
 * article, byte delta, editor, summary.
 *
 * Rendered here rather than through `components/wiki/ChangeRow.tsx`, which is
 * the shared row for Recent changes, the watchlist and contributions and does
 * not exist yet. When it lands this list should be replaced by it — the field
 * names already match `ChangeRow` (DECISIONS §4), including the em dash for a
 * talk row's null `byte_delta`.
 */
function RecentChangesList({ rows }: { rows: ChangeRow[] }) {
  if (rows.length === 0) {
    return <p className="text-ui text-ink-2">No changes recorded yet.</p>;
  }

  return (
    <ul className="text-ui">
      {rows.map((row) => {
        const tone = byteDeltaTone(row.byte_delta);
        return (
          <li
            key={changeRowKey(row)}
            className="border-b border-rule-hair py-1 last:border-0"
          >
            <span className="flex flex-wrap items-baseline gap-x-1.5">
              <time
                dateTime={row.timestamp}
                title={formatDateTime(row.timestamp)}
                className="tabular-nums text-ink-2"
              >
                {formatRelativeTime(row.timestamp)}
              </time>
              <Link
                to={`/wiki/${row.article.slug}`}
                className="font-serif text-[1.0625rem] text-link visited:text-link-visited hover:underline"
              >
                {row.article.title}
              </Link>
              <span
                className={
                  tone === "positive"
                    ? "tabular-nums text-delta-pos"
                    : tone === "negative"
                      ? "tabular-nums text-delta-neg"
                      : "tabular-nums text-delta-null"
                }
              >
                {formatByteDelta(row.byte_delta)}
              </span>
              {row.is_minor && (
                <abbr title="Minor edit" className="text-flag text-ink-2 no-underline">
                  m
                </abbr>
              )}
              {row.kind === "talk" && (
                <span className="text-2xs text-ink-2">talk</span>
              )}
            </span>
            {(row.comment || row.user) && (
              <span className="block truncate text-2xs text-ink-2">
                {row.user ? (
                  <Link
                    to={`/u/${row.user.username}`}
                    className="text-link hover:underline"
                  >
                    {row.user.username}
                  </Link>
                ) : (
                  "anonymous"
                )}
                {row.comment && <>: {row.comment}</>}
              </span>
            )}
          </li>
        );
      })}
    </ul>
  );
}

/** Static skeletons that match the panel geometry — no shimmer (§6.2). */
function FeaturedSkeleton() {
  return (
    <div>
      <Skeleton className="float-right mb-2 ml-3 h-[13.75rem] w-[7.5rem] sm:w-[9rem] md:w-[11rem]" />
      <Skeleton className="h-5 w-2/3" />
      <div className="mt-2 space-y-1.5">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-11/12" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-4/5" />
      </div>
      <div className="clear-both" />
    </div>
  );
}

function LineSkeleton({ lines }: { lines: number }) {
  return (
    <div className="space-y-1.5">
      {Array.from({ length: lines }).map((_, index) => (
        <Skeleton
          key={index}
          className={index % 3 === 2 ? "h-4 w-4/5" : "h-4 w-full"}
        />
      ))}
    </div>
  );
}
