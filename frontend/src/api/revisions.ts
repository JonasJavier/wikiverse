/**
 * Revision history and diffs.
 *
 * Two endpoints, both read-only and both fixed by DECISIONS:
 *
 *   `GET /api/articles/{slug}/revisions/?page=`   §10, page size 50
 *   `GET /api/articles/{slug}/diff/?from=&to=`    §14
 *
 * The diff is computed entirely server-side (`apps/articles/diff.py`): the
 * client never diffs, never re-diffs on a re-render, and never needs a diff
 * library in the bundle. A diff between two historical revisions is immutable
 * and the backend serves it `Cache-Control: immutable`, which is why the query
 * below sets `staleTime: Infinity` — refetching a diff can only ever return
 * the same bytes.
 */

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { DiffPayload, Paginated, Revision, RevisionDetail } from "@/lib/types";

/** DECISIONS §10. The `Pagination` labels ("Previous 50") read this. */
export const REVISIONS_PAGE_SIZE = 50;

/**
 * `?from=0` is not "no value": it is the page-creation diff, against the empty
 * document. `null` means "let the server pick" — the parent of `to`.
 */
export type RevisionRef = number | null;

export const revisionKeys = {
  all: ["revisions"] as const,
  list: (slug: string, page: number) =>
    ["revisions", slug, "list", page] as const,
  detail: (slug: string, id: number) =>
    ["revisions", slug, "detail", id] as const,
  diff: (slug: string, from: RevisionRef, to: RevisionRef) =>
    ["revisions", slug, "diff", from ?? "parent", to ?? "latest"] as const,
};

/**
 * One page of history, newest first.
 *
 * `placeholderData: keepPreviousData` keeps the previous page on screen while
 * the next one loads, so paging a long history does not flash an empty table
 * and does not lose the reader's scroll position.
 */
export function useRevisions(slug: string, page = 1) {
  return useQuery({
    queryKey: revisionKeys.list(slug, page),
    queryFn: async () => {
      const { data } = await api.get<Paginated<Revision>>(
        `/articles/${slug}/revisions/`,
        { params: { page } },
      );
      return data;
    },
    enabled: Boolean(slug),
    placeholderData: keepPreviousData,
  });
}

/** One revision in full, including `content` and the snapshotted apparatus. */
export function useRevisionDetail(slug: string, id: number | null) {
  return useQuery({
    queryKey: revisionKeys.detail(slug, id ?? 0),
    queryFn: async () => {
      const { data } = await api.get<RevisionDetail>(
        `/articles/${slug}/revisions/${id}/`,
      );
      return data;
    },
    enabled: Boolean(slug) && id !== null,
  });
}

/**
 * The server-rendered diff between two revisions.
 *
 * Both ends are optional and each omission has a defined server-side meaning,
 * so they are forwarded as absent rather than as `0`:
 *   `to` absent   → the article's latest revision
 *   `from` absent → the parent of `to` (or the next older revision)
 *   `from=0`      → the empty document, i.e. the page-creation diff
 */
export function useDiff(slug: string, from: RevisionRef, to: RevisionRef) {
  return useQuery({
    queryKey: revisionKeys.diff(slug, from, to),
    queryFn: async () => {
      const params: Record<string, number> = {};
      if (from !== null) params.from = from;
      if (to !== null) params.to = to;
      const { data } = await api.get<DiffPayload>(`/articles/${slug}/diff/`, {
        params,
      });
      return data;
    },
    enabled: Boolean(slug),
    // Revisions are immutable, so a diff between two of them is too.
    staleTime: Infinity,
  });
}
