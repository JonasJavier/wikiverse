import { Link } from "react-router-dom";

import type { CategoryBranch, CategoryRow } from "@/api/categories";
import { cn } from "@/lib/utils";

interface CategoryTreeProps {
  branches: CategoryBranch[];
  /**
   * `"columns"` — the main page's dense multi-column list: every category and
   * its count on one screen, subcategories indented under their parent.
   * `"index"` — the categories index: the same tree with its glosses, one
   * `h2` per top-level category.
   */
  variant?: "columns" | "index";
  className?: string;
}

/**
 * The category tree, rendered as text in columns rather than as cards.
 *
 * DECISIONS §9 is the load-bearing rule here: `Category.color` is an arbitrary
 * hex from the taxonomy, so it appears ONLY as a 2px leading bar beside the
 * label — never as a text colour and never as a background behind text. That
 * removes the contrast problem structurally (the label is always `--ink-1` at
 * ≥14.5:1) instead of policing which hexes are allowed, and it is also what
 * stops the list looking like a row of pill-shaped SaaS tags.
 */
export function CategoryTree({
  branches,
  variant = "columns",
  className,
}: CategoryTreeProps) {
  if (branches.length === 0) {
    return <p className="text-ui text-ink-2">No categories yet.</p>;
  }

  if (variant === "index") {
    return (
      <ul className={cn("columns-1 gap-x-8 sm:columns-2 tools:columns-3", className)}>
        {branches.map(({ category, children, total }) => (
          <li key={category.slug} className="mb-4 break-inside-avoid">
            <h2 className="font-serif text-[1.1875rem] font-normal">
              <CategoryLink category={category} />
              <Count value={total} />
            </h2>
            {category.description && (
              <p className="mt-0.5 text-ui leading-snug text-ink-2">
                {category.description}
              </p>
            )}
            {children.length > 0 && (
              <ul className="mt-1 border-l border-rule-hair pl-2.5 text-ui">
                {children.map((child) => (
                  <li key={child.slug} className="mt-0.5">
                    <CategoryLink category={child} />
                    <Count value={child.article_count} />
                    {child.description && (
                      <span className="block text-2xs leading-snug text-ink-2">
                        {child.description}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    );
  }

  return (
    <ul
      className={cn(
        "columns-1 gap-x-6 text-ui sm:columns-2",
        className,
      )}
    >
      {branches.map(({ category, children }) => (
        <li key={category.slug} className="mb-1.5 break-inside-avoid">
          <CategoryLink category={category} />
          <Count value={category.article_count} />
          {children.length > 0 && (
            <ul className="mt-0.5 pl-2.5">
              {children.map((child) => (
                <li key={child.slug} className="text-2xs">
                  <CategoryLink category={child} />
                  <Count value={child.article_count} />
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
}

/**
 * The chip: a 2px rule in the category's colour, the name in ordinary ink.
 * The rule is `borderLeftColor` from the database hex — the one and only place
 * an inline style is correct here, because the value is data.
 */
function CategoryLink({ category }: { category: CategoryRow }) {
  return (
    <Link
      to={`/category/${category.slug}`}
      className="border-l-2 pl-1.5 text-link visited:text-link-visited hover:underline"
      style={{ borderLeftColor: category.color || "var(--rule)" }}
    >
      {category.name}
    </Link>
  );
}

function Count({ value }: { value: number }) {
  return (
    <span className="ml-1.5 tabular-nums text-ink-2">
      ({value.toLocaleString("en")})
    </span>
  );
}
