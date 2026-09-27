import type { ReactNode } from "react";
import { Link } from "react-router-dom";

import { cn } from "@/lib/utils";

interface PaginationProps {
  /** 1-based. */
  page: number;
  count: number;
  /** DECISIONS §10: 20 for articles and search, 50 for revisions and feeds. */
  pageSize: number;
  /**
   * Build the URL for a page. Prefer this: a real `<Link>` carrying the page
   * in the URL is what makes back/forward and scroll restoration work.
   */
  hrefFor?: (page: number) => string;
  /** Callback fallback for pages that do not yet keep the page in the URL. */
  onPage?: (page: number) => void;
  /**
   * `"prevnext"` (default) is the encyclopedia idiom. `"numbered"` exists
   * only for a genuinely large listing such as /browse.
   */
  variant?: "prevnext" | "numbered";
  className?: string;
}

/**
 * Prev / next plus an explicit result range, replacing the numbered button
 * strip.
 *
 * Reasons this is the default: the wiki and search-results idiom is prev /
 * next plus a count; numbered buttons over a corpus this size are six
 * buttons of noise; and prev/next carrying `rel="prev"` / `rel="next"` is
 * what a crawler follows.
 *
 * When a direction is unavailable it renders a plain `<span>`, not an
 * `aria-disabled` link. `aria-disabled` announces the state but does not
 * prevent activation, so a "disabled" link still navigates — which is worse
 * than not offering it.
 */
export function Pagination({
  page,
  count,
  pageSize,
  hrefFor,
  onPage,
  variant = "prevnext",
  className,
}: PaginationProps) {
  const totalPages = Math.max(1, Math.ceil(count / pageSize));
  if (totalPages <= 1) return null;

  const start = (page - 1) * pageSize + 1;
  const end = Math.min(page * pageSize, count);
  const hasPrev = page > 1;
  const hasNext = page < totalPages;

  return (
    <nav
      aria-label="Pagination"
      className={cn(
        "mt-6 flex flex-wrap items-center justify-between gap-x-4 gap-y-2",
        "border-t border-rule pt-3 text-ui",
        className,
      )}
    >
      <Step
        to={hasPrev ? page - 1 : null}
        rel="prev"
        hrefFor={hrefFor}
        onPage={onPage}
      >
        {"←"} Previous {pageSize}
      </Step>

      {variant === "numbered" ? (
        <PageNumbers
          page={page}
          totalPages={totalPages}
          hrefFor={hrefFor}
          onPage={onPage}
        />
      ) : (
        /* En dash between the bounds, per DECISIONS §10. */
        <span className="tabular-nums text-ink-2">
          Results {start.toLocaleString("en")}
          {"–"}
          {end.toLocaleString("en")} of {count.toLocaleString("en")}
        </span>
      )}

      <Step
        to={hasNext ? page + 1 : null}
        rel="next"
        hrefFor={hrefFor}
        onPage={onPage}
      >
        Next {pageSize} {"→"}
      </Step>
    </nav>
  );
}

interface StepProps {
  to: number | null;
  rel: "prev" | "next";
  hrefFor?: (page: number) => string;
  onPage?: (page: number) => void;
  children: ReactNode;
}

function Step({ to, rel, hrefFor, onPage, children }: StepProps) {
  if (to === null) {
    return <span className="text-ink-3">{children}</span>;
  }
  if (hrefFor) {
    return (
      <Link to={hrefFor(to)} rel={rel} className="text-link hover:underline">
        {children}
      </Link>
    );
  }
  return (
    <button
      type="button"
      onClick={() => onPage?.(to)}
      className="cursor-pointer text-link hover:underline"
    >
      {children}
    </button>
  );
}

interface PageNumbersProps {
  page: number;
  totalPages: number;
  hrefFor?: (page: number) => string;
  onPage?: (page: number) => void;
}

/**
 * The numbered strip, only for /browse. `aria-current="page"` on the active
 * item is what the old implementation never set, so a screen-reader user had
 * no way to tell which page they were on.
 */
function PageNumbers({ page, totalPages, hrefFor, onPage }: PageNumbersProps) {
  const shown = Array.from({ length: totalPages }, (_, i) => i + 1).filter(
    (p) => p === 1 || p === totalPages || Math.abs(p - page) <= 1,
  );

  const itemClass = (active: boolean) =>
    cn(
      "inline-flex h-7 min-w-7 items-center justify-center rounded-chrome px-1.5",
      "tabular-nums",
      active
        ? "border border-rule bg-panel font-semibold text-ink"
        : "cursor-pointer text-link hover:bg-panel",
    );

  return (
    <ul className="flex items-center gap-1">
      {shown.map((p, i) => (
        <li key={p} className="flex items-center gap-1">
          {i > 0 && p - shown[i - 1] > 1 && (
            <span aria-hidden="true" className="px-0.5 text-ink-3">
              {"…"}
            </span>
          )}
          {p === page ? (
            <span aria-current="page" className={itemClass(true)}>
              {p}
            </span>
          ) : hrefFor ? (
            <Link
              to={hrefFor(p)}
              aria-label={`Page ${p}`}
              className={itemClass(false)}
            >
              {p}
            </Link>
          ) : (
            <button
              type="button"
              aria-label={`Page ${p}`}
              onClick={() => onPage?.(p)}
              className={itemClass(false)}
            >
              {p}
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}
