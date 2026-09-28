import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import type { SearchResult } from "@/lib/types";
import { formatDateTime, formatKb, formatNumber } from "@/lib/utils";
import { Snippet } from "./Snippet";

/**
 * One search result: a row, not a card.
 *
 * A row can be dense, scannable and identical from the first hit to the
 * fortieth; the 3-up card grid this replaces could be none of those. The
 * hairline separator is the only chrome, and there is no full-row click
 * overlay, so the snippet text stays selectable.
 *
 * The size line is derived here rather than served: `byte_size` and
 * `word_count` are the two numbers the API sends, and "9 KB (1,430 words)" is
 * the wiki presentation of them. 1 KB = 1024 bytes and anything under a
 * kilobyte reports as "1 KB", because a stub is small rather than empty.
 *
 * The category colour appears as a 2px left rule and nowhere else — never as
 * a fill and never as a text colour (DECISIONS §9), so an arbitrary hex from
 * the taxonomy can never produce an unreadable chip.
 */
export function ResultRow({ result }: { result: SearchResult }) {
  const { slug, title, title_snippet, snippet, category, updated_at } = result;

  return (
    <li className="border-b border-rule-hair py-3 last:border-0">
      <Link
        to={`/wiki/${slug}`}
        className="font-serif text-[1.1875rem] leading-snug text-link visited:text-link-visited hover:underline"
      >
        <Snippet text={title_snippet} fallback={title} />
      </Link>

      {snippet && (
        <p className="mt-1 text-ui text-ink">
          <Snippet text={snippet} />
        </p>
      )}

      <p className="mt-1 flex flex-wrap items-baseline gap-x-1.5 text-xs text-ink-2 tabular-nums">
        <span>
          {formatKb(result.byte_size)} ({formatNumber(result.word_count)} words)
        </span>
        {category && (
          <>
            <Separator />
            <Link
              to={`/category/${category.slug}`}
              className="text-ink-2 hover:text-ink hover:underline"
            >
              <Badge color={category.color} className="text-xs">
                {category.name}
              </Badge>
            </Link>
          </>
        )}
        <Separator />
        <time dateTime={updated_at} title={formatDateTime(updated_at)}>
          {formatDateTime(updated_at)}
        </time>
      </p>
    </li>
  );
}

function Separator() {
  return (
    <span aria-hidden="true" className="text-ink-3">
      ·
    </span>
  );
}

/**
 * The loading placeholder matches the row's geometry — title, snippet, meta —
 * so the list does not reflow when the real rows arrive. Static tint, no
 * shimmer: an infinite animation on a reader-facing surface is the one thing
 * the previous stylesheet got most wrong.
 */
export function ResultRowSkeleton() {
  return (
    <li className="border-b border-rule-hair py-3 last:border-0">
      <Skeleton className="h-5 w-2/3" />
      <Skeleton className="mt-2 h-4 w-full" />
      <Skeleton className="mt-1 h-4 w-5/6" />
      <Skeleton className="mt-2 h-3 w-40" />
    </li>
  );
}
