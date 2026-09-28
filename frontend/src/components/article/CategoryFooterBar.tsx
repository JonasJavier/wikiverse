import { Fragment } from "react";
import { Link } from "react-router-dom";

import type { CategoryRef } from "@/lib/types";
import { cn } from "@/lib/utils";

export interface CategoryFooterBarProps {
  /** Every category, PRIMARY FIRST (DECISIONS §13). */
  categories: readonly CategoryRef[];
  className?: string;
}

/**
 * The category footer bar: full content width, at the very bottom, one panel
 * strip reading `Categories: A | B | C`.
 *
 * This is one of the four elements that carry the whole encyclopedia effect, and
 * it is why DECISIONS §13 gave articles real secondary categories instead of a
 * single-item list — a bar with one entry looks like a breadcrumb, a bar with
 * four looks like a reference work.
 *
 * The category's own hex NEVER becomes a text or background colour here
 * (DECISIONS §9). The bar is ordinary ink on panel; colour, where it appears at
 * all, is a 2px leading rule handled by `Badge`.
 */
export function CategoryFooterBar({ categories, className }: CategoryFooterBarProps) {
  if (categories.length === 0) return null;

  return (
    <nav
      aria-label="Categories"
      className={cn(
        "catbar mt-5 rounded-chrome border border-rule bg-panel px-2.5 py-1.5 font-sans text-ui",
        className,
      )}
    >
      <span className="font-semibold text-ink">Categories</span>
      <span className="text-ink-2">: </span>
      {categories.map((category, index) => (
        <Fragment key={category.slug}>
          {index > 0 ? (
            <span className="px-1 text-ink-3" aria-hidden="true">
              |
            </span>
          ) : null}
          <Link to={`/category/${category.slug}`}>{category.name}</Link>
        </Fragment>
      ))}
    </nav>
  );
}
