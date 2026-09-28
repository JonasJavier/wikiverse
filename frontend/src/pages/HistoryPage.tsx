import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";

import { useArticle } from "@/api/articles";
import { REVISIONS_PAGE_SIZE, useRevisions } from "@/api/revisions";
import { RevisionHistoryTable } from "@/components/history/RevisionHistoryTable";
import { RailGroup, Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import type { Revision } from "@/lib/types";
import { formatNumber } from "@/lib/utils";

/**
 * `/wiki/:slug/history?oldid=&diff=&page=`
 *
 * Everything that is state here is in the URL, which is what makes a pending
 * comparison shareable, the back button correct, `ScrollRestoration` work and
 * page 2 crawlable — and it is also what fixes, structurally, the old page's
 * bug where the selected revision survived a navigation to a different
 * article: the selection cannot outlive the URL that carries the slug.
 *
 * `?oldid=` / `?diff=` are MediaWiki's own parameter names for the two sides of
 * a pending comparison, kept because a reader who knows one wiki knows this
 * one. Submitting the form navigates to the route DECISIONS §14 fixes,
 * `/wiki/:slug/diff?from=&to=`.
 */
export function HistoryPage() {
  const { slug = "" } = useParams();
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();

  const page = pageParam(params.get("page"));
  const { data: article } = useArticle(slug);
  const { data, isLoading, isError } = useRevisions(slug, page);

  const revisions = data?.results ?? [];
  const count = data?.count ?? article?.revision_count ?? 0;
  const title = article?.title ?? slug;
  const heading = `${title}: revision history`;

  useDocumentMeta({
    title: heading,
    description: `The full edit history of the Wikiverse article ${title}: every revision, its editor, its size and its edit summary.`,
    canonical: `/wiki/${slug}/history`,
  });

  /**
   * `cur` is a diff against the article's current revision, so it needs that
   * id — which the history page itself only knows on page 1. The article detail
   * carries it for every page; until it resolves, `RevisionHistoryTable`
   * renders `cur` as plain text rather than pointing it somewhere wrong.
   */
  const latestId =
    article?.latest_revision?.id ??
    (page === 1 ? (revisions[0]?.id ?? null) : null);

  const { older, newer } = selection(
    revisions,
    intParam(params.get("oldid")),
    intParam(params.get("diff")),
  );

  function select(side: "old" | "new", id: number) {
    const next = new URLSearchParams(params);
    next.set(side === "old" ? "oldid" : "diff", String(id));
    // `replace`: choosing a radio is not a destination, and a history entry per
    // click would make the back button useless on this page.
    setParams(next, { replace: true });
  }

  function compare() {
    if (older === null || newer === null) return;
    navigate(`/wiki/${slug}/diff?from=${older}&to=${newer}`);
  }

  function hrefForPage(target: number): string {
    const next = new URLSearchParams(params);
    if (target <= 1) next.delete("page");
    else next.set("page", String(target));
    const query = next.toString();
    return `/wiki/${slug}/history${query ? `?${query}` : ""}`;
  }

  const lastPage = Math.max(1, Math.ceil(count / REVISIONS_PAGE_SIZE));

  return (
    <WikiFrame
      rail={<Sidebar />}
      tools={<Tools slug={slug} lastPage={lastPage} hrefForPage={hrefForPage} />}
    >
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-ink text-balance">
          {heading}
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          {count > 0
            ? `All ${formatNumber(count)} ${count === 1 ? "revision" : "revisions"} to this article, newest first.`
            : "Every revision to this article, newest first."}{" "}
          <Link to={`/wiki/${slug}`} className="text-link hover:underline">
            Read the article
          </Link>
          .
        </p>
      </div>

      {isError ? (
        <EmptyState
          title="This history could not be loaded."
          hint={
            <>
              The article may have been deleted or renamed.{" "}
              <Link to="/browse" className="text-link hover:underline">
                Browse the encyclopedia
              </Link>{" "}
              instead.
            </>
          }
        />
      ) : isLoading && revisions.length === 0 ? (
        <HistorySkeleton />
      ) : revisions.length === 0 ? (
        <EmptyState
          title="No revisions on this page."
          hint={
            page > 1 ? (
              <Link to={hrefForPage(1)} className="text-link hover:underline">
                Back to the newest revisions
              </Link>
            ) : (
              "This article has no recorded history yet."
            )
          }
        />
      ) : (
        <>
          <RevisionHistoryTable
            slug={slug}
            title={title}
            revisions={revisions}
            count={count}
            latestId={latestId}
            oldid={older}
            newid={newer}
            onSelect={select}
            onCompare={compare}
          />
          <Pagination
            page={page}
            count={count}
            pageSize={REVISIONS_PAGE_SIZE}
            hrefFor={hrefForPage}
          />
        </>
      )}
    </WikiFrame>
  );
}

/* ---------------------------------------------------------------------------
   Selection
   ------------------------------------------------------------------------- */

/**
 * The effective comparison pair.
 *
 * Defaults to the top two rows, which is what MediaWiki pre-selects and what
 * makes the commonest action — "what was the last edit?" — one click. The
 * defaults are computed rather than written into the URL, so a shared link
 * still means exactly what its author selected.
 *
 * A pair that is backwards (a hand-edited URL, or a link that outlived its
 * revisions) drops the OLDER side rather than silently swapping the two: a
 * reader who asked for a specific newer revision should keep it.
 */
function selection(
  revisions: Revision[],
  urlOld: number | null,
  urlNew: number | null,
): { older: number | null; newer: number | null } {
  const newer = urlNew ?? revisions[0]?.id ?? null;
  const older = urlOld ?? revisions[1]?.id ?? null;

  if (older !== null && newer !== null && older >= newer) {
    return { older: null, newer };
  }
  return { older, newer };
}

function intParam(raw: string | null): number | null {
  if (raw === null || raw.trim() === "") return null;
  const value = Number(raw);
  return Number.isSafeInteger(value) && value > 0 ? value : null;
}

function pageParam(raw: string | null): number {
  return intParam(raw) ?? 1;
}

/* ---------------------------------------------------------------------------
   Rails and loading
   ------------------------------------------------------------------------- */

function Tools({
  slug,
  lastPage,
  hrefForPage,
}: {
  slug: string;
  lastPage: number;
  hrefForPage: (page: number) => string;
}) {
  return (
    <nav aria-label="Tools" className="text-ui">
      <h2 className="border-b border-rule-hair px-2 pb-1 text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
        Tools
      </h2>

      {/* Plain links, not `RailLink`: `NavLink` computes `aria-current` from the
          path alone, so every entry that differs only by query string would be
          announced as the current page at the same time. */}
      <RailGroup>
        <ToolLink to={`/wiki/${slug}`}>Read the article</ToolLink>
        <ToolLink to={`/wiki/${slug}/edit`}>Edit this article</ToolLink>
      </RailGroup>

      <RailGroup label="Jump to">
        <ToolLink to={hrefForPage(1)}>Newest revisions</ToolLink>
        {lastPage > 1 && (
          <ToolLink to={hrefForPage(lastPage)}>Oldest revisions</ToolLink>
        )}
      </RailGroup>
    </nav>
  );
}

function ToolLink({ to, children }: { to: string; children: string }) {
  return (
    <li>
      <Link
        to={to}
        className="block rounded-chrome px-2 py-1 text-link transition-colors duration-100 hover:bg-panel hover:text-link-hover motion-reduce:transition-none"
      >
        {children}
      </Link>
    </li>
  );
}

/**
 * A skeleton with the table's geometry, not a spinner: the reader's eye is
 * already where the first row will be. Static-tinted, no shimmer.
 */
function HistorySkeleton() {
  return (
    <div aria-busy="true" className="space-y-1.5">
      <Skeleton className="h-8 w-full" />
      {Array.from({ length: 8 }, (_, index) => (
        <Skeleton key={index} className="h-7 w-full" />
      ))}
      <span className="sr-only">Loading the revision history…</span>
    </div>
  );
}
