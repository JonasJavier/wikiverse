import { Link, useSearchParams } from "react-router-dom";

import { buildCategoryTree, useCategories } from "@/api/categories";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { CategoryTree } from "@/components/mainpage/CategoryTree";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { cn, formatNumber } from "@/lib/utils";

type Sort = "name" | "size";

/**
 * The categories index — a dense two-level index, not a card grid.
 *
 * Deleted here: the 3-up grid of rounded cards with a 3px coloured top border,
 * a colour-tinted count pill (measured 1.93:1 to 3.75:1 against its own
 * background), a `line-clamp-2` gloss, a hover lift and an "Explore →" arrow
 * that slid on hover. Six categories filled a screen.
 *
 * What replaces it: every category, every subcategory, every count and every
 * gloss in multi-column text — the whole taxonomy on one screen. The colour
 * survives as a 2px leading rule (DECISIONS §9), which is the only place it is
 * safe.
 *
 * The sort lives in the URL (`?sort=size`), so the view is shareable and the
 * back button works.
 */
export function CategoriesPage() {
  const [params, setParams] = useSearchParams();
  const sort: Sort = params.get("sort") === "size" ? "size" : "name";

  const { data: categories, isPending, isError } = useCategories();
  const branches = buildCategoryTree(categories, sort);

  const total = categories?.length ?? 0;
  const articles = branches.reduce((sum, branch) => sum + branch.total, 0);

  useDocumentMeta({
    title: "Categories",
    description:
      "Every category in Wikiverse, with its subcategories, article counts and descriptions.",
    canonical: "/categories",
  });

  const setSort = (next: Sort) => {
    const updated = new URLSearchParams(params);
    if (next === "name") updated.delete("sort");
    else updated.set("sort", next);
    setParams(updated, { replace: true });
  };

  return (
    <WikiFrame rail={<Sidebar />}>
      <div className="pt-4">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          Categories
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2 tabular-nums">
          {isPending
            ? "Loading the taxonomy."
            : `${formatNumber(total)} categor${total === 1 ? "y" : "ies"}, ${formatNumber(articles)} article${articles === 1 ? "" : "s"} between them.`}
        </p>

        <nav
          aria-label="Sort categories"
          className="mt-3 flex items-baseline gap-3 border-b border-rule-hair pb-2 text-ui"
        >
          <span className="text-ink-2">Sort by</span>
          <SortLink active={sort === "name"} onClick={() => setSort("name")}>
            name
          </SortLink>
          <SortLink active={sort === "size"} onClick={() => setSort("size")}>
            size
          </SortLink>
        </nav>

        <div className="mt-4">
          {isError ? (
            <EmptyState
              title="The categories could not be loaded."
              hint={
                <>
                  The API did not answer.{" "}
                  <Link to="/browse" className="text-link hover:underline">
                    Browse all articles
                  </Link>{" "}
                  instead.
                </>
              }
            />
          ) : isPending ? (
            <div aria-busy="true" className="space-y-4">
              {Array.from({ length: 6 }).map((_, index) => (
                <div key={index} className="space-y-1.5">
                  <Skeleton className="h-5 w-2/5" />
                  <Skeleton className="h-4 w-3/5" />
                </div>
              ))}
            </div>
          ) : (
            <CategoryTree branches={branches} variant="index" />
          )}
        </div>
      </div>
    </WikiFrame>
  );
}

/**
 * A button, not a link: the sort is a view preference written into the query
 * string by the page, and two `<Link>`s here would each need the whole
 * surviving parameter set spliced into them.
 */
function SortLink({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-current={active ? "true" : undefined}
      className={cn(
        "rounded-chrome",
        active
          ? "font-semibold text-ink"
          : "cursor-pointer text-link hover:underline",
      )}
    >
      {children}
    </button>
  );
}
