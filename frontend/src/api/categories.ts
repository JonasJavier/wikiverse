/**
 * The category tree and the articles inside a category.
 *
 * `GET /api/categories/` is unpaginated by design (the taxonomy is two levels
 * and ~14 rows), so the whole tree arrives in one request and both the
 * categories index and the "Browse by category" panel can be dense: every
 * category, its count and its gloss, on one screen.
 *
 * Articles in a category come from the viewset's own action,
 * `GET /api/categories/{slug}/articles/`, which includes articles attached
 * through `extra_categories` (DECISIONS §13) and pages at 50 (DECISIONS §10).
 * `/api/articles/?category=` is NOT the same query — it sees only the primary
 * foreign key.
 */

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type {
  ArticleListItem,
  Category,
  CategoryRef,
  Paginated,
} from "@/lib/types";

/** DECISIONS §10: the category article listing pages at 50. */
export const CATEGORY_PAGE_SIZE = 50;

/**
 * A category exactly as `CategorySerializer` sends it.
 *
 * `parent` is declared as a `SlugRelatedField`, so the wire format is a SLUG
 * STRING, while `Category.parent` in lib/types.ts is a nested `CategoryRef`.
 * Accepting both shapes here (and reading them through `parentSlug`) means the
 * tree is correct against the serializer as it stands today and stays correct
 * if the serializer is later changed to nest the parent — without this module
 * redefining `Category`.
 */
export interface CategoryRow extends Omit<Category, "parent"> {
  parent: string | CategoryRef | null;
}

/** The parent's slug, whichever of the two wire shapes arrived. */
export function parentSlug(parent: CategoryRow["parent"]): string | null {
  if (!parent) return null;
  if (typeof parent === "string") return parent || null;
  return parent.slug || null;
}

/** A top-level category with its children resolved, for the two-level tree. */
export interface CategoryBranch {
  category: CategoryRow;
  children: CategoryRow[];
  /** The branch's own count plus every child's — what a tree row should show. */
  total: number;
}

export const categoryKeys = {
  all: ["categories"] as const,
  list: ["categories", "list"] as const,
  detail: (slug: string) => ["categories", "detail", slug] as const,
  articles: (slug: string, page: number) =>
    ["categories", "detail", slug, "articles", page] as const,
};

export function useCategories() {
  return useQuery({
    queryKey: categoryKeys.list,
    queryFn: async () => {
      const { data } = await api.get<CategoryRow[]>("/categories/");
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
}

export function useCategory(slug: string) {
  return useQuery({
    queryKey: categoryKeys.detail(slug),
    queryFn: async () => {
      const { data } = await api.get<CategoryRow>(`/categories/${slug}/`);
      return data;
    },
    enabled: Boolean(slug),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * `GET /api/categories/{slug}/articles/?page=` — page size 50, ordered by
 * title so the letter grouping on the category page is the server's order and
 * not a client-side re-sort of one page.
 */
export function useCategoryArticles(slug: string, page: number) {
  return useQuery({
    queryKey: categoryKeys.articles(slug, page),
    queryFn: async () => {
      const { data } = await api.get<Paginated<ArticleListItem>>(
        `/categories/${slug}/articles/`,
        { params: { page, page_size: CATEGORY_PAGE_SIZE } },
      );
      return data;
    },
    enabled: Boolean(slug),
    placeholderData: keepPreviousData,
  });
}

/**
 * Group a flat category list into the two-level tree the taxonomy actually
 * describes. Sorting is stable and explicit: `order` then `name` for the
 * alphabetical view, `total` descending for the by-size view.
 *
 * A child whose parent is missing from the payload is promoted to the top
 * level rather than dropped — a category that exists must be reachable.
 */
export function buildCategoryTree(
  categories: CategoryRow[] | undefined,
  sort: "name" | "size" = "name",
): CategoryBranch[] {
  if (!categories?.length) return [];

  const bySlug = new Map(categories.map((c) => [c.slug, c]));
  const roots: CategoryRow[] = [];
  const childrenOf = new Map<string, CategoryRow[]>();

  for (const category of categories) {
    const parent = parentSlug(category.parent);
    if (parent && bySlug.has(parent) && parent !== category.slug) {
      const siblings = childrenOf.get(parent);
      if (siblings) siblings.push(category);
      else childrenOf.set(parent, [category]);
    } else {
      roots.push(category);
    }
  }

  const byName = (a: CategoryRow, b: CategoryRow) =>
    a.order - b.order || a.name.localeCompare(b.name, "en");

  const branches: CategoryBranch[] = roots.map((category) => {
    const children = (childrenOf.get(category.slug) ?? []).slice().sort(byName);
    return {
      category,
      children,
      total:
        category.article_count +
        children.reduce((sum, child) => sum + child.article_count, 0),
    };
  });

  if (sort === "size") {
    return branches.sort(
      (a, b) => b.total - a.total || a.category.name.localeCompare(b.category.name, "en"),
    );
  }
  return branches.sort((a, b) => byName(a.category, b.category));
}

/** The subcategories of one category, for the panel above a category listing. */
export function subcategoriesOf(
  categories: CategoryRow[] | undefined,
  slug: string,
): CategoryRow[] {
  if (!categories?.length || !slug) return [];
  return categories
    .filter((c) => parentSlug(c.parent) === slug)
    .sort((a, b) => a.order - b.order || a.name.localeCompare(b.name, "en"));
}
