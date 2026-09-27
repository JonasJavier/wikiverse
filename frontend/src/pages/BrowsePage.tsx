import { Link, useNavigate, useSearchParams } from "react-router-dom";

import { useArticles } from "@/api/articles";
import { useCategories } from "@/api/categories";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import type { ArticleListItem } from "@/lib/types";
import { cn, formatDate, formatKb, formatNumber } from "@/lib/utils";

/** DECISIONS §10: `/api/articles/` is 20 per page. */
const PAGE_SIZE = 20;

/** U+2013 EN DASH. */
const EN_DASH = "–";

/**
 * Every value here is in `ArticleViewSet.ordering_fields`; a value outside this
 * list is discarded rather than forwarded, so a hand-edited URL cannot make the
 * API answer 400.
 */
const ORDERINGS = [
  { value: "title", label: "Title A–Z" },
  { value: "-updated_at", label: "Recently updated" },
  { value: "-view_count", label: "Most viewed" },
  { value: "-word_count", label: "Longest" },
] as const;

const DEFAULT_ORDERING = "title";

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

/** The bucket for a title that does not begin with a Latin letter. */
const OTHER = "#";

const CONTROL =
  "h-8 rounded-chrome border border-rule bg-page px-2 text-ui text-ink " +
  "transition-colors duration-100";

interface BrowseQuery {
  category: string;
  ordering: string;
  page: number;
}

function readQuery(params: URLSearchParams): BrowseQuery {
  const ordering = params.get("ordering") ?? "";
  const page = Number.parseInt(params.get("page") ?? "1", 10);

  return {
    category: params.get("category") ?? "",
    ordering: ORDERINGS.some((o) => o.value === ordering)
      ? ordering
      : DEFAULT_ORDERING,
    page: Number.isFinite(page) && page > 0 ? page : 1,
  };
}

function browseHref(query: BrowseQuery): string {
  const params = new URLSearchParams();
  if (query.category) params.set("category", query.category);
  if (query.ordering !== DEFAULT_ORDERING) params.set("ordering", query.ordering);
  if (query.page > 1) params.set("page", String(query.page));
  const qs = params.toString();
  return qs ? `/browse?${qs}` : "/browse";
}

/**
 * The initial a title files under. Diacritics are folded first, so `Éire` files
 * under E rather than into the `#` bucket — a reader looking for it under E is
 * right, and the alphabet does not grow a hole per accent.
 */
function initialOf(title: string): string {
  const first = title
    .trim()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .charAt(0)
    .toLocaleUpperCase();
  return /^[A-Z]$/.test(first) ? first : OTHER;
}

interface LetterGroup {
  letter: string;
  articles: ArticleListItem[];
}

/** Consecutive runs, not a bucket map: the list is already sorted by title. */
function groupByInitial(articles: ArticleListItem[]): LetterGroup[] {
  const groups: LetterGroup[] = [];
  for (const article of articles) {
    const letter = initialOf(article.title);
    const last = groups[groups.length - 1];
    if (last && last.letter === letter) last.articles.push(article);
    else groups.push({ letter, articles: [article] });
  }
  return groups;
}

/**
 * `/browse?category=&ordering=&page=` — the index of every article.
 *
 * A DENSE LIST, not a card grid. The 3-up grid this replaces showed nine
 * articles per screen and told you almost nothing about any of them; twenty
 * rows carry a title, a gloss, a size, a category and a date each, which is
 * what an index is for.
 *
 * All three controls live in the URL, so a filtered index is shareable, the
 * back button works and page 2 is crawlable.
 */
export function BrowsePage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const query = readQuery(params);

  const { data: categories } = useCategories();
  const { data, isLoading, isFetching, isError, refetch } = useArticles({
    category: query.category || undefined,
    ordering: query.ordering,
    page: query.page,
    page_size: PAGE_SIZE,
  });

  useDocumentMeta({
    title: "Browse all articles",
    description:
      "An index of every article in Wikiverse, by title, category, size and date.",
    canonical: "/browse",
  });

  function patch(next: Partial<BrowseQuery>) {
    navigate(browseHref({ ...query, ...next, page: next.page ?? 1 }));
  }

  const count = data?.count ?? 0;
  const articles = data?.results ?? [];
  const start = (query.page - 1) * PAGE_SIZE + 1;
  const end = Math.min(query.page * PAGE_SIZE, count);
  const alphabetical = query.ordering === "title";
  const groups = alphabetical ? groupByInitial(articles) : [];
  const activeCategory = categories?.find((c) => c.slug === query.category);

  return (
    <WikiFrame>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          All articles
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          {data
            ? `Every article in Wikiverse — ${formatNumber(count)} in total${
                activeCategory ? ` in ${activeCategory.name}` : ""
              }.`
            : "Every article in Wikiverse, listed alphabetically."}
        </p>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 border-y border-rule-hair py-2 text-ui">
        <label className="flex items-center gap-1.5 text-ink-2">
          Category
          <select
            value={query.category}
            onChange={(event) => patch({ category: event.target.value })}
            className={CONTROL}
          >
            <option value="">All categories</option>
            {categories?.map((category) => (
              <option key={category.slug} value={category.slug}>
                {category.name}
              </option>
            ))}
          </select>
        </label>

        <label className="flex items-center gap-1.5 text-ink-2">
          Order
          <select
            value={query.ordering}
            onChange={(event) => patch({ ordering: event.target.value })}
            className={CONTROL}
          >
            {ORDERINGS.map((ordering) => (
              <option key={ordering.value} value={ordering.value}>
                {ordering.label}
              </option>
            ))}
          </select>
        </label>

        {query.category && (
          <span className="inline-flex items-center rounded-chrome border border-rule bg-panel py-0.5 pl-2 text-ui text-ink">
            <span className="text-ink-2">Category:&nbsp;</span>
            {activeCategory?.name ?? query.category}
            <button
              type="button"
              onClick={() => patch({ category: "" })}
              aria-label="Remove the category filter"
              className="cursor-pointer px-1.5 text-ink-2 hover:text-ink"
            >
              <span aria-hidden="true">×</span>
            </button>
          </span>
        )}
      </div>

      {alphabetical && groups.length > 0 && (
        <JumpBar present={new Set(groups.map((group) => group.letter))} />
      )}

      {count > 0 && (
        <p className="mt-3 text-xs tabular-nums text-ink-2">
          Showing {formatNumber(start)}
          {EN_DASH}
          {formatNumber(end)} of {formatNumber(count)}
        </p>
      )}

      <div
        aria-busy={isLoading || isFetching}
        className={cn(
          "mt-2",
          isFetching && !isLoading && "opacity-60 transition-opacity duration-100",
        )}
      >
        {isError ? (
          <LoadError onRetry={() => void refetch()} />
        ) : isLoading ? (
          <ul>
            {Array.from({ length: 8 }, (_, index) => (
              <ListRowSkeleton key={index} />
            ))}
          </ul>
        ) : count === 0 ? (
          <EmptyState
            title="No articles match these filters."
            hint={
              query.category
                ? "This category has no published articles yet."
                : "The encyclopedia is still being written."
            }
            action={
              query.category ? (
                <Button variant="secondary" onClick={() => patch({ category: "" })}>
                  Clear the filter
                </Button>
              ) : undefined
            }
          />
        ) : alphabetical ? (
          groups.map((group) => (
            <section key={group.letter}>
              <h2
                id={`letter-${group.letter === OTHER ? "other" : group.letter}`}
                className="mt-4 border-b border-rule pb-0.5 font-serif text-h2 font-normal text-ink"
              >
                {group.letter}
              </h2>
              <ul>
                {group.articles.map((article) => (
                  <ArticleRow key={article.slug} article={article} />
                ))}
              </ul>
            </section>
          ))
        ) : (
          <ul>
            {articles.map((article) => (
              <ArticleRow key={article.slug} article={article} />
            ))}
          </ul>
        )}
      </div>

      {!isError && count > 0 && (
        <Pagination
          page={query.page}
          count={count}
          pageSize={PAGE_SIZE}
          variant="numbered"
          hrefFor={(page) => browseHref({ ...query, page })}
        />
      )}
    </WikiFrame>
  );
}

/**
 * The letter bar jumps to a heading ON THIS PAGE, which is what it can honestly
 * do: `/api/articles/` has no initial-letter facet, so a letter cannot be a
 * server-side filter without a backend change. Letters with no titles on the
 * page are rendered as plain text rather than as `aria-disabled` links —
 * `aria-disabled` announces the state but does not prevent activation, so a
 * "disabled" link still navigates, which is worse than not offering it.
 *
 * A plain `<a href="#…">` rather than a router `Link`: the browser's own
 * fragment navigation is what scrolls, and `scroll-padding-top` in the base
 * layer is what keeps the heading clear of the sticky sub-header.
 */
function JumpBar({ present }: { present: Set<string> }) {
  const letters = [...ALPHABET, OTHER];

  return (
    <nav
      aria-label="Jump to a letter on this page"
      className="mt-3 flex flex-wrap items-center gap-x-1 gap-y-1 text-ui tabular-nums"
    >
      {letters.map((letter) =>
        present.has(letter) ? (
          <a
            key={letter}
            href={`#letter-${letter === OTHER ? "other" : letter}`}
            className="rounded-chrome px-1 font-medium text-link hover:underline"
          >
            {letter}
          </a>
        ) : (
          <span
            key={letter}
            title={`No titles under ${letter} on this page`}
            className="px-1 text-ink-3"
          >
            {letter}
          </span>
        ),
      )}
    </nav>
  );
}

/**
 * One index row. Kept local to this page on purpose: the shared
 * `ArticleListRow` belongs to the article surface and is being written by
 * another hand, and importing a file that does not exist yet would break the
 * build for everybody. Swap it in when it lands; the markup is §4.23's.
 */
function ArticleRow({ article }: { article: ArticleListItem }) {
  const { slug, title, short_description, summary, category, is_stub } = article;

  return (
    <li className="border-b border-rule-hair py-2.5 last:border-0">
      <div className="flex flex-wrap items-baseline gap-2">
        <Link
          to={`/wiki/${slug}`}
          className="font-serif text-[1.125rem] leading-snug text-link visited:text-link-visited hover:underline"
        >
          {title}
        </Link>
        {is_stub && <Badge variant="stub">Stub</Badge>}
      </div>

      {(short_description || summary) && (
        <p className="mt-0.5 text-ui text-ink-2">{short_description || summary}</p>
      )}

      <p className="mt-0.5 flex flex-wrap items-baseline gap-x-1.5 text-xs tabular-nums text-ink-2">
        <span>
          {formatKb(article.byte_size)} ({formatNumber(article.word_count)} words)
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
        <time dateTime={article.updated_at}>{formatDate(article.updated_at)}</time>
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

function ListRowSkeleton() {
  return (
    <li className="border-b border-rule-hair py-2.5 last:border-0">
      <Skeleton className="h-5 w-1/2" />
      <Skeleton className="mt-2 h-4 w-3/4" />
      <Skeleton className="mt-2 h-3 w-40" />
    </li>
  );
}

function LoadError({ onRetry }: { onRetry: () => void }) {
  return (
    <div
      role="alert"
      className="rounded-chrome border border-rule-hair bg-panel px-4 py-6 text-ui"
    >
      <p className="font-medium text-ink">The index could not be loaded.</p>
      <p className="mt-1 text-ink-2">
        The connection to the server failed. Nothing is lost — try again.
      </p>
      <div className="mt-3">
        <Button variant="secondary" onClick={onRetry}>
          Try again
        </Button>
      </div>
    </div>
  );
}
