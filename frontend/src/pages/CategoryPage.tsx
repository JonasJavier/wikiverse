import { Link, useParams, useSearchParams } from "react-router-dom";

import {
  CATEGORY_PAGE_SIZE,
  subcategoriesOf,
  useCategories,
  useCategory,
  useCategoryArticles,
} from "@/api/categories";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Panel } from "@/components/mainpage/Panel";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import type { ArticleListItem } from "@/lib/types";
import { formatNumber, scrollBehavior } from "@/lib/utils";

interface LetterGroup {
  letter: string;
  articles: ArticleListItem[];
}

/** Group by initial, the way a category page is read. Digits and symbols fall
 *  under `#`, so every article has a home and the jump bar is complete. */
function groupByInitial(articles: ArticleListItem[]): LetterGroup[] {
  const groups = new Map<string, ArticleListItem[]>();
  for (const article of articles) {
    const first = article.title.trim().charAt(0).toLocaleUpperCase("en");
    const letter = /\p{L}/u.test(first) ? first : "#";
    const bucket = groups.get(letter);
    if (bucket) bucket.push(article);
    else groups.set(letter, [article]);
  }
  return [...groups.entries()]
    .map(([letter, rows]) => ({ letter, articles: rows }))
    .sort((a, b) => {
      if (a.letter === "#") return 1;
      if (b.letter === "#") return -1;
      return a.letter.localeCompare(b.letter, "en");
    });
}

const anchorId = (letter: string) =>
  `pages-${letter === "#" ? "other" : letter.toLowerCase()}`;

/**
 * One category's pages: subcategories first, then the articles as a dense
 * alphabetical list grouped by initial, 50 to a page.
 *
 * This is the reading order a category page actually has on a wiki, and it is
 * why the old 12-per-page card grid was wrong twice: it buried the
 * subcategories and it made 24 entries feel like a shop.
 *
 * The category's own colour appears only as the 2px rule on the `h1`
 * (DECISIONS §9). The page number lives in the URL, so `Next 50` is a real
 * link, the back button works and page 2 is crawlable.
 */
export function CategoryPage() {
  const { slug = "" } = useParams();
  const [params] = useSearchParams();
  const page = Math.max(1, Number(params.get("page") ?? "1") || 1);

  const { data: category, isPending: loadingCategory, isError } = useCategory(slug);
  const { data: categories } = useCategories();
  const { data, isPending: loadingArticles } = useCategoryArticles(slug, page);

  const subcategories = subcategoriesOf(categories, slug);
  const name = category?.name ?? slug;
  const articles = data?.results ?? [];
  const groups = groupByInitial(articles);
  const shown = articles.length;
  const count = data?.count ?? 0;

  useDocumentMeta({
    title: `Category: ${name}`,
    description:
      category?.description ||
      `Every Wikiverse article in the ${name} category.`,
    canonical: `/category/${slug}`,
  });

  const hrefFor = (next: number) => {
    const updated = new URLSearchParams(params);
    if (next <= 1) updated.delete("page");
    else updated.set("page", String(next));
    const query = updated.toString();
    return query ? `/category/${slug}?${query}` : `/category/${slug}`;
  };

  if (isError) {
    return (
      <WikiFrame rail={<Sidebar />}>
        <div className="pt-4">
          <h1 className="font-serif text-h1 font-normal text-ink">
            Category: {slug}
          </h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <EmptyState
            className="mt-4"
            title="This category does not exist."
            hint={
              <>
                It may have been renamed.{" "}
                <Link to="/categories" className="text-link hover:underline">
                  See every category
                </Link>
                .
              </>
            }
          />
        </div>
      </WikiFrame>
    );
  }

  return (
    <WikiFrame rail={<Sidebar />}>
      <div className="pt-4">
        <nav aria-label="Breadcrumb" className="text-ui text-ink-2">
          <Link to="/" className="text-link hover:underline">
            Main page
          </Link>
          <span aria-hidden="true" className="px-1.5">
            ›
          </span>
          <Link to="/categories" className="text-link hover:underline">
            Categories
          </Link>
          <span aria-hidden="true" className="px-1.5">
            ›
          </span>
          <span className="text-ink">{name}</span>
        </nav>

        <div className="mt-2">
          <h1
            className="border-l-2 pl-3 font-serif text-h1 font-normal text-balance text-ink"
            style={{ borderLeftColor: category?.color || "var(--rule)" }}
          >
            Category: {name}
          </h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          {category?.description && (
            <p className="mt-1.5 text-ui text-ink-2">{category.description}</p>
          )}
          <p className="mt-0.5 text-ui text-ink-2 tabular-nums">
            {loadingArticles || loadingCategory
              ? "Counting the pages in this category."
              : `Pages in this category — ${formatNumber(shown)} shown of ${formatNumber(count)} total.`}
          </p>
        </div>

        {subcategories.length > 0 && (
          <Panel title="Subcategories" className="mt-4">
            <ul className="columns-1 gap-x-6 text-ui sm:columns-2 tools:columns-3">
              {subcategories.map((child) => (
                <li key={child.slug} className="mb-1 break-inside-avoid">
                  <Link
                    to={`/category/${child.slug}`}
                    className="border-l-2 pl-1.5 text-link visited:text-link-visited hover:underline"
                    style={{ borderLeftColor: child.color || "var(--rule)" }}
                  >
                    {child.name}
                  </Link>
                  <span className="ml-1.5 tabular-nums text-ink-2">
                    ({child.article_count.toLocaleString("en")})
                  </span>
                </li>
              ))}
            </ul>
          </Panel>
        )}

        <section className="mt-6" aria-busy={loadingArticles || undefined}>
          <h2 className="font-serif text-h2 font-normal text-ink">
            Pages in “{name}”
          </h2>
          <hr className="mt-1.5 border-0 border-t border-rule-hair" />

          {loadingArticles ? (
            <div className="mt-3 space-y-1.5">
              {Array.from({ length: 12 }).map((_, index) => (
                <Skeleton key={index} className="h-4 w-2/3" />
              ))}
            </div>
          ) : articles.length === 0 ? (
            <EmptyState
              className="mt-3"
              title="No published pages in this category yet."
              hint={
                <>
                  <Link
                    to={`/new?category=${encodeURIComponent(slug)}`}
                    className="text-link hover:underline"
                  >
                    Write the first one
                  </Link>
                  .
                </>
              }
            />
          ) : (
            <>
              {groups.length > 1 && (
                <nav
                  aria-label="Jump to initial"
                  className="mt-2 flex flex-wrap items-baseline gap-x-2.5 gap-y-1 border-b border-rule-hair pb-2 text-ui"
                >
                  {groups.map((group) => (
                    <a
                      key={group.letter}
                      href={`#${anchorId(group.letter)}`}
                      onClick={(event) => {
                        // Programmatic, so the reader's motion preference is
                        // honoured per jump (DECISIONS §18).
                        const target = document.getElementById(
                          anchorId(group.letter),
                        );
                        if (!target) return;
                        event.preventDefault();
                        target.scrollIntoView({ behavior: scrollBehavior() });
                      }}
                      className="text-link hover:underline"
                    >
                      {group.letter}
                      <span className="ml-0.5 text-2xs tabular-nums text-ink-2">
                        {group.articles.length}
                      </span>
                    </a>
                  ))}
                </nav>
              )}

              <div className="mt-3 space-y-4">
                {groups.map((group) => (
                  <div key={group.letter}>
                    <h3
                      id={anchorId(group.letter)}
                      className="scroll-mt-24 border-b border-rule-hair pb-0.5 font-serif text-h4 font-normal text-ink-2"
                    >
                      {group.letter}
                    </h3>
                    <ul className="mt-1.5 columns-1 gap-x-8 text-read sm:columns-2 tools:columns-3">
                      {group.articles.map((article) => (
                        <li
                          key={article.id}
                          className="mb-1 break-inside-avoid font-serif leading-snug"
                        >
                          <Link
                            to={`/wiki/${article.slug}`}
                            className="text-link visited:text-link-visited hover:underline"
                          >
                            {article.title}
                          </Link>
                          {article.is_stub && (
                            <span className="ml-1.5 font-sans text-2xs text-ink-3">
                              stub
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              <Pagination
                page={page}
                count={count}
                pageSize={CATEGORY_PAGE_SIZE}
                hrefFor={hrefFor}
              />
            </>
          )}
        </section>
      </div>
    </WikiFrame>
  );
}
