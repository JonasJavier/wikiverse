import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { api } from "@/lib/api";
import type {
  Article,
  ArticleInput,
  CategoryRef,
  ArticleListItem,
  Backlink,
  PageInfo,
  Paginated,
  PreviewCard,
  Revision,
  RevisionDetail,
  SiteStats,
} from "@/lib/types";

/* =====================================================================
   Types the article detail endpoint does not serve YET
   =====================================================================
   `ArticleDetailSerializer` (backend `apps/articles/serializers.py`) currently
   exposes no outgoing-link resolution and no `see_also`, even though the data
   exists in the `ArticleLink` model and in the seed corpus. Both are declared
   here as OPTIONAL extensions of `Article` rather than edited into
   `src/lib/types.ts`, for two reasons: `types.ts` is a shared file five agents
   are touching at once, and an optional field means `tsc -b` passes against
   today's API while the renderer lights up the moment the serializer grows.

   Fold these into `types.ts` once the backend serves them.
   ===================================================================== */

/**
 * One row of an article's outgoing `[[wikilinks]]`, resolved server-side.
 *
 * Field names mirror the `ArticleLink` model so the serializer can expose it
 * verbatim: `to_title`, `to_slug`, and `exists` for `to_article IS NOT NULL`.
 */
export interface ArticleLinkTarget {
  to_title: string;
  to_slug: string;
  /** `false` is a RED LINK: the target is planned but unwritten. */
  exists: boolean;
  occurrences?: number;
}

export interface ArticleExtras {
  /** Every `[[wikilink]]` in the body, resolved. Authoritative when present. */
  links?: ArticleLinkTarget[];
  /** `## See also` targets, rendered from data rather than hand-written. */
  see_also?: string[];
  /**
   * Every category, PRIMARY FIRST (DECISIONS §13).
   *
   * `ArticleDetailSerializer.get_categories` already emits this; only
   * `types.ts` is missing it, so it is declared optional here rather than
   * edited into a file five agents are writing at once.
   */
  categories?: CategoryRef[];
}

/** What `GET /api/articles/{slug}/` returns, plus the two pending fields. */
export type ArticleDetail = Article & ArticleExtras;

/** One row of `GET /api/wanted/` — a red link, ranked by inbound count. */
export interface WantedPage {
  title: string;
  slug: string;
  incoming: number;
}

export interface ArticleQuery {
  search?: string;
  category?: string;
  author?: string;
  ordering?: string;
  page?: number;
  page_size?: number;
}

/**
 * `/api/wanted/` page size. `max_page_size` is 100 and the corpus plans 120
 * articles of which 57 are unwritten, so one page covers every red-link target
 * the seed can produce. See `useWantedSlugs` for why that matters.
 */
const WANTED_PAGE_SIZE = 100;

export const articleKeys = {
  all: ["articles"] as const,
  list: (params: ArticleQuery) => ["articles", "list", params] as const,
  detail: (slug: string) => ["articles", "detail", slug] as const,
  revisions: (slug: string) => ["articles", slug, "revisions"] as const,
  revision: (slug: string, id: number) =>
    ["articles", slug, "revisions", id] as const,
  preview: (slug: string) => ["articles", "preview", slug] as const,
  info: (slug: string) => ["articles", slug, "info"] as const,
  backlinks: (slug: string) => ["articles", slug, "backlinks"] as const,
  popular: ["articles", "popular"] as const,
  stats: ["articles", "stats"] as const,
  wanted: ["wanted"] as const,
};

export function useArticles(params: ArticleQuery = {}) {
  return useQuery({
    queryKey: articleKeys.list(params),
    queryFn: async () => {
      const { data } = await api.get<Paginated<ArticleListItem>>("/articles/", {
        params,
      });
      return data;
    },
    placeholderData: keepPreviousData,
  });
}

export function useArticle(slug: string) {
  return useQuery({
    queryKey: articleKeys.detail(slug),
    queryFn: async () => {
      const { data } = await api.get<ArticleDetail>(`/articles/${slug}/`);
      return data;
    },
    enabled: Boolean(slug),
  });
}

/**
 * `GET /api/articles/{slug}/preview/` — the hover card's payload.
 *
 * `staleTime: Infinity` is deliberate: a preview is a title, a gloss and a
 * thumbnail, none of which changes while a reader is on one page, and this
 * endpoint fires on hover. Once fetched, moving the pointer back and forth over
 * the same link costs nothing.
 */
export function usePreviewCard(slug: string, enabled: boolean) {
  return useQuery({
    queryKey: articleKeys.preview(slug),
    queryFn: async () => {
      const { data } = await api.get<PreviewCard>(`/articles/${slug}/preview/`);
      return data;
    },
    enabled: enabled && Boolean(slug),
    staleTime: Infinity,
    gcTime: 30 * 60_000,
    retry: false,
  });
}

/**
 * `GET /api/wanted/` — every red-link target in the corpus, most-wanted first.
 *
 * ONE request per session, shared by every article. It is the fallback the red
 * links currently run on; see `useArticleLinkResolver`.
 */
export function useWantedPages(enabled = true) {
  return useQuery({
    queryKey: articleKeys.wanted,
    queryFn: async () => {
      const { data } = await api.get<Paginated<WantedPage>>("/wanted/", {
        params: { page_size: WANTED_PAGE_SIZE },
      });
      return data;
    },
    enabled,
    staleTime: 10 * 60_000,
    gcTime: 60 * 60_000,
    retry: false,
  });
}

/** `GET /api/articles/{slug}/info/` — the Tools rail's "This page" figures. */
export function usePageInfo(slug: string, enabled = true) {
  return useQuery({
    queryKey: articleKeys.info(slug),
    queryFn: async () => {
      const { data } = await api.get<PageInfo>(`/articles/${slug}/info/`);
      return data;
    },
    enabled: enabled && Boolean(slug),
  });
}

/** `GET /api/articles/{slug}/backlinks/` — "what links here". */
export function useBacklinks(slug: string, enabled = true) {
  return useQuery({
    queryKey: articleKeys.backlinks(slug),
    queryFn: async () => {
      const { data } = await api.get<Paginated<Backlink>>(
        `/articles/${slug}/backlinks/`,
      );
      return data;
    },
    enabled: enabled && Boolean(slug),
  });
}

export function usePopularArticles() {
  return useQuery({
    queryKey: articleKeys.popular,
    queryFn: async () => {
      const { data } = await api.get<ArticleListItem[]>("/articles/popular/");
      return data;
    },
  });
}

export function useSiteStats() {
  return useQuery({
    queryKey: articleKeys.stats,
    queryFn: async () => {
      const { data } = await api.get<SiteStats>("/articles/stats/");
      return data;
    },
  });
}

export function useArticleRevisions(slug: string) {
  return useQuery({
    queryKey: articleKeys.revisions(slug),
    queryFn: async () => {
      const { data } = await api.get<Paginated<Revision>>(
        `/articles/${slug}/revisions/`,
      );
      return data;
    },
    enabled: Boolean(slug),
  });
}

export function useRevisionDetail(slug: string, id: number | null) {
  return useQuery({
    queryKey: articleKeys.revision(slug, id ?? 0),
    queryFn: async () => {
      const { data } = await api.get<RevisionDetail>(
        `/articles/${slug}/revisions/${id}/`,
      );
      return data;
    },
    enabled: Boolean(slug) && id !== null,
  });
}

export async function fetchRandomArticle(): Promise<Article> {
  const { data } = await api.get<Article>("/articles/random/");
  return data;
}

export function useCreateArticle() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: ArticleInput) => {
      const { data } = await api.post<Article>("/articles/", input);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: articleKeys.all });
    },
  });
}

export function useUpdateArticle(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: Partial<ArticleInput>) => {
      const { data } = await api.patch<Article>(`/articles/${slug}/`, input);
      return data;
    },
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: articleKeys.all });
      qc.setQueryData(articleKeys.detail(data.slug), data);
    },
  });
}

export function useDeleteArticle() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (slug: string) => {
      await api.delete(`/articles/${slug}/`);
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: articleKeys.all });
    },
  });
}

/**
 * `POST` / `DELETE /api/articles/{slug}/watch/`.
 *
 * The cached detail is patched rather than invalidated: re-fetching a whole
 * article, body and all, to flip one boolean is exactly the kind of thing that
 * makes a star feel slow.
 */
export function useWatchArticle(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (watch: boolean) => {
      if (watch) await api.post(`/articles/${slug}/watch/`);
      else await api.delete(`/articles/${slug}/watch/`);
      return watch;
    },
    onSuccess: (watching) => {
      qc.setQueryData<ArticleDetail>(articleKeys.detail(slug), (current) =>
        current ? { ...current, is_watched: watching } : current,
      );
      qc.invalidateQueries({ queryKey: ["watchlist"] });
    },
  });
}
