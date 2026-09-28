/**
 * The community surface: recent changes, the watchlist, contributions,
 * talk pages and watching.
 *
 * Four things in here are contract, not preference:
 *
 *  1. **The URL is the source of truth for every feed.** `readChangeFilters`
 *     parses a `URLSearchParams` into state and `changesQuery` /
 *     `feedQuery` translate that state into API parameters using the exact
 *     mapping table in DECISIONS §4. Nothing in this app filters a change
 *     feed from `useState`.
 *  2. **`days=N` becomes `since=<now − N days>`**, not `days=N`. The backend
 *     accepts either (`_parse_since` in `views.py` reads `since` first, then
 *     `days`), but DECISIONS §4 names `since` as the API parameter and that
 *     is what the contract test asserts.
 *  3. **`/api/changes/` is a timestamp cursor, not a page number.** Its
 *     envelope is `{results, next_before, has_more}` and it never reports a
 *     count, because an honest `count` over a merged, append-at-the-head
 *     stream does not exist. `/api/watchlist/` and the contributions
 *     endpoint ARE page-numbered (50 per page, DECISIONS §10).
 *  4. **One row shape for three feeds.** All three deserialise to
 *     `ChangeRow`, which is why one component renders all three.
 */

import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { type ArticleDetail, articleKeys } from "@/api/articles";
import { api, API_BASE_URL } from "@/lib/api";
import type {
  ChangeFeed,
  ChangeRow,
  ChangeTypeFilter,
  Paginated,
  PublicUser,
  TalkMessage,
  TalkMessageInput,
  TalkThread,
  TalkThreadDetail,
  TalkThreadInput,
} from "@/lib/types";

/* =====================================================================
   Constants
   ===================================================================== */

/** DECISIONS §10: `/api/changes/`, `/api/watchlist/` and contributions. */
export const FEED_PAGE_SIZE = 50;

/** DECISIONS §4 defaults. */
export const DEFAULT_CHANGE_TYPE: ChangeTypeFilter = "all";
export const DEFAULT_CHANGE_DAYS = 7;
export const DEFAULT_CHANGE_LIMIT = FEED_PAGE_SIZE;

/**
 * The day windows the filter bar offers. The backend clamps `days` to
 * 1–365, so every one of these survives the round trip.
 */
export const CHANGE_DAY_OPTIONS = [1, 7, 30] as const;

/**
 * The row limits the filter bar offers.
 *
 * design-ui §5.10 lists `50 / 100 / 250`, but `_bounded(..., high=100)` in
 * `views.py` clamps `limit` at **100**, so a "250 changes" control would
 * silently return 100 and lie about it. Two truthful options beat three
 * where one is fiction.
 */
export const CHANGE_LIMIT_OPTIONS = [50, 100] as const;

/** DECISIONS §14. Absolute, because the feed is served by the API host. */
export const CHANGES_FEED_URL = `${API_BASE_URL}/feeds/changes.rss`;

const MS_PER_HOUR = 3_600_000;
const MS_PER_DAY = 86_400_000;

/* =====================================================================
   Query keys
   ===================================================================== */

export const communityKeys = {
  all: ["community"] as const,
  changes: () => ["community", "changes"] as const,
  changesList: (params: ChangesQuery) =>
    ["community", "changes", params] as const,
  watchlist: () => ["community", "watchlist"] as const,
  watchlistPage: (params: FeedQuery) =>
    ["community", "watchlist", params] as const,
  contributions: (username: string) =>
    ["community", "contributions", username] as const,
  contributionsPage: (username: string, params: FeedQuery) =>
    ["community", "contributions", username, params] as const,
  profile: (username: string) => ["community", "profile", username] as const,
  talkThreads: (slug: string) => ["community", "talk", "list", slug] as const,
  talkThread: (id: number) => ["community", "talk", "detail", id] as const,
};

/* =====================================================================
   URL → state → API query  (DECISIONS §4, exactly)
   =====================================================================

   | URL param    | API param          | Default |
   | ------------ | ------------------ | ------- |
   | type         | type               | all     |
   | user         | user               | —       |
   | category     | category           | —       |
   | hideMinor=1  | minor=0            | off     |
   | hideBot=1    | bots=0             | off     |
   | days=N       | since=<now−N days> | 7       |
   | limit        | limit              | 50      |

   Two params exist beyond the table because the endpoints define them and a
   reader needs them: `before` (the `/api/changes/` cursor, so "show older
   changes" is a shareable URL) and `page` (the page-numbered feeds).
   ===================================================================== */

/** The filter bar's state. Parsed from the URL, never held in `useState`. */
export interface ChangeFilterState {
  type: ChangeTypeFilter;
  /** `""` means "no filter" — a blank `?user=` must not become `user=`. */
  user: string;
  category: string;
  hideMinor: boolean;
  hideBot: boolean;
  days: number;
  limit: number;
  /** `/api/changes/` cursor: show rows strictly older than this instant. */
  before: string;
  /** 1-based, for the page-numbered feeds. */
  page: number;
}

/** What `/api/changes/` is actually sent. */
export interface ChangesQuery {
  type: ChangeTypeFilter;
  since: string;
  limit: number;
  user?: string;
  category?: string;
  /** Present ONLY when hiding: `minor=0`. Absence means "show them". */
  minor?: "0";
  bots?: "0";
  before?: string;
}

/**
 * What `/api/watchlist/` and the contributions endpoint are sent.
 *
 * `since` is optional because the two feeds want different defaults, and the
 * backend's `_parse_since` returns `None` when neither `since` nor `days` is
 * present — i.e. "no time filter at all". A watchlist is a *recent* view, so
 * it is windowed; a contributions list is a person's whole record, so
 * windowing it to seven days would hide almost all of it.
 */
export interface FeedQuery {
  since?: string;
  page: number;
  minor?: "0";
  bots?: "0";
}

function intParam(raw: string | null, fallback: number, low: number, high: number): number {
  const parsed = Number.parseInt(raw ?? "", 10);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.min(high, Math.max(low, parsed));
}

function changeType(raw: string | null): ChangeTypeFilter {
  return raw === "edit" || raw === "talk" ? raw : DEFAULT_CHANGE_TYPE;
}

/**
 * `hideMinor=1` / `hideBot=1`. Only the literal affirmatives count, so a
 * stale `hideMinor=0` in somebody's bookmark reads as "off" rather than as
 * "present, therefore true".
 */
function flagOn(raw: string | null): boolean {
  if (raw === null) return false;
  return ["1", "true", "yes", "on"].includes(raw.trim().toLowerCase());
}

export function readChangeFilters(search: URLSearchParams): ChangeFilterState {
  return {
    type: changeType(search.get("type")),
    user: search.get("user")?.trim() ?? "",
    category: search.get("category")?.trim() ?? "",
    hideMinor: flagOn(search.get("hideMinor")),
    hideBot: flagOn(search.get("hideBot")),
    days: intParam(search.get("days"), DEFAULT_CHANGE_DAYS, 1, 365),
    limit: intParam(search.get("limit"), DEFAULT_CHANGE_LIMIT, 1, 100),
    before: search.get("before")?.trim() ?? "",
    page: intParam(search.get("page"), 1, 1, 10_000),
  };
}

/**
 * `days=N` → `since=<now − N days>`, with **now floored to the hour**.
 *
 * The flooring is not cosmetic. `since` lands in a TanStack Query key, so a
 * value recomputed to the millisecond on every render would produce a new
 * key on every render and refetch the feed forever. Flooring to the hour
 * makes the key stable for up to an hour; the Refresh button invalidates
 * explicitly, which is the control design-ui §5.10 asks for anyway ("no
 * auto-refresh, no polling — an encyclopedia's changes feed that moves under
 * the cursor is hostile").
 */
export function sinceFromDays(days: number, now: number = Date.now()): string {
  const hour = Math.floor(now / MS_PER_HOUR) * MS_PER_HOUR;
  return new Date(hour - days * MS_PER_DAY).toISOString();
}

export function changesQuery(state: ChangeFilterState): ChangesQuery {
  const query: ChangesQuery = {
    type: state.type,
    since: sinceFromDays(state.days),
    limit: state.limit,
  };
  if (state.user) query.user = state.user;
  if (state.category) query.category = state.category;
  if (state.hideMinor) query.minor = "0";
  if (state.hideBot) query.bots = "0";
  if (state.before) query.before = state.before;
  return query;
}

/**
 * The watchlist. No `type` (its queryset is revisions only, so `type=talk`
 * would have nothing to return — critique #21) and no `limit` (the page size
 * is fixed at 50 by DECISIONS §10).
 */
export function feedQuery(state: ChangeFilterState): FeedQuery {
  const query: FeedQuery = {
    since: sinceFromDays(state.days),
    page: state.page,
  };
  if (state.hideMinor) query.minor = "0";
  if (state.hideBot) query.bots = "0";
  return query;
}

/**
 * Contributions: page number only, deliberately un-windowed. A contributor's
 * record is the whole record; `?days=7` on a profile would show almost
 * nothing and would look like an empty account.
 */
export function contributionsQuery(page: number): FeedQuery {
  return { page };
}

/**
 * Write filter state back to the URL, dropping every parameter that is at
 * its default so a pristine view has a clean, canonical, shareable address.
 *
 * `page` and `before` are always dropped: changing any filter invalidates
 * the position in the feed, and leaving a cursor behind is how a reader ends
 * up staring at an empty page after narrowing a range.
 */
export function writeChangeFilters(
  state: ChangeFilterState,
  patch: Partial<ChangeFilterState>,
): URLSearchParams {
  const next = { ...state, ...patch, before: "", page: 1 };
  const search = new URLSearchParams();

  if (next.type !== DEFAULT_CHANGE_TYPE) search.set("type", next.type);
  if (next.user) search.set("user", next.user);
  if (next.category) search.set("category", next.category);
  if (next.hideMinor) search.set("hideMinor", "1");
  if (next.hideBot) search.set("hideBot", "1");
  if (next.days !== DEFAULT_CHANGE_DAYS) search.set("days", String(next.days));
  if (next.limit !== DEFAULT_CHANGE_LIMIT) search.set("limit", String(next.limit));

  return search;
}

/** The same, for a page-numbered feed: keeps `page`, keeps the filters. */
export function changeFiltersWithPage(
  state: ChangeFilterState,
  page: number,
): URLSearchParams {
  const search = writeChangeFilters(state, {});
  if (page > 1) search.set("page", String(page));
  return search;
}

/* =====================================================================
   Feeds
   ===================================================================== */

/** `GET /api/changes/` — the merged edit + talk stream. */
export function useChanges(params: ChangesQuery) {
  return useQuery({
    queryKey: communityKeys.changesList(params),
    queryFn: async () => {
      const { data } = await api.get<ChangeFeed>("/changes/", { params });
      return data;
    },
    placeholderData: keepPreviousData,
  });
}

/** `GET /api/watchlist/` — changes to the caller's watched articles. */
export function useWatchlist(params: FeedQuery, enabled = true) {
  return useQuery({
    queryKey: communityKeys.watchlistPage(params),
    queryFn: async () => {
      const { data } = await api.get<Paginated<ChangeRow>>("/watchlist/", {
        params,
      });
      return data;
    },
    enabled,
    placeholderData: keepPreviousData,
  });
}

/** `GET /api/users/{username}/contributions/` (DECISIONS §17). */
export function useContributions(username: string, params: FeedQuery) {
  return useQuery({
    queryKey: communityKeys.contributionsPage(username, params),
    queryFn: async () => {
      const { data } = await api.get<Paginated<ChangeRow>>(
        `/users/${encodeURIComponent(username)}/contributions/`,
        { params },
      );
      return data;
    },
    enabled: Boolean(username),
    placeholderData: keepPreviousData,
  });
}

/**
 * `GET /api/auth/users/{username}/` — anybody's public profile.
 *
 * `PublicUser` deliberately carries no `email`; nothing in this app may
 * render one for a user other than the signed-in reader themselves.
 */
export function usePublicProfile(username: string) {
  return useQuery({
    queryKey: communityKeys.profile(username),
    queryFn: async () => {
      const { data } = await api.get<PublicUser>(
        `/auth/users/${encodeURIComponent(username)}/`,
      );
      return data;
    },
    enabled: Boolean(username),
    retry: false,
    staleTime: 60_000,
  });
}

/* =====================================================================
   Talk
   ===================================================================== */

/**
 * A thread as the LIST endpoint serves it.
 *
 * `TalkThreadSerializer` (the list row) has no `article` key — only
 * `TalkThreadDetailSerializer` does, because on a list nested under
 * `/articles/{slug}/talk/` the article is the route. This is derived from
 * the contract type rather than being a second hand-written shape, so the
 * two cannot drift.
 */
export type TalkThreadListItem = Omit<TalkThread, "article">;

/** `GET /api/articles/{slug}/talk/` — thread headers, 20 per page. */
export function useTalkThreads(slug: string) {
  return useQuery({
    queryKey: communityKeys.talkThreads(slug),
    queryFn: async () => {
      const { data } = await api.get<Paginated<TalkThreadListItem>>(
        `/articles/${slug}/talk/`,
      );
      return data;
    },
    enabled: Boolean(slug),
  });
}

/**
 * `GET /api/talk/threads/{id}/` — one thread with its messages.
 *
 * The list endpoint does not embed messages, so each rendered thread loads
 * its own. That is a request per thread, and it is the right trade here: a
 * thread is the unit a reply, an edit and a deletion all invalidate, so
 * per-thread caching keeps a reply from refetching the whole talk page.
 */
export function useTalkThread(id: number, enabled = true) {
  return useQuery({
    queryKey: communityKeys.talkThread(id),
    queryFn: async () => {
      const { data } = await api.get<TalkThreadDetail>(`/talk/threads/${id}/`);
      return data;
    },
    enabled: enabled && Number.isFinite(id),
  });
}

/** `POST /api/articles/{slug}/talk/` — opens a thread and its first message. */
export function useCreateTalkThread(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: TalkThreadInput) => {
      const { data } = await api.post<TalkThreadDetail>(
        `/articles/${slug}/talk/`,
        input,
      );
      return data;
    },
    onSuccess: (thread) => {
      qc.setQueryData(communityKeys.talkThread(thread.id), thread);
      qc.invalidateQueries({ queryKey: communityKeys.talkThreads(slug) });
      // `talk_thread_count` on the article changed.
      qc.invalidateQueries({ queryKey: articleKeys.detail(slug) });
      qc.invalidateQueries({ queryKey: communityKeys.changes() });
    },
  });
}

export interface ReplyInput extends TalkMessageInput {
  threadId: number;
}

/** `POST /api/articles/{slug}/talk/{threadId}/messages/`. */
export function useCreateTalkMessage(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ threadId, ...body }: ReplyInput) => {
      const { data } = await api.post<TalkMessage>(
        `/articles/${slug}/talk/${threadId}/messages/`,
        body,
      );
      return data;
    },
    onSuccess: (_message, variables) => {
      qc.invalidateQueries({
        queryKey: communityKeys.talkThread(variables.threadId),
      });
      qc.invalidateQueries({ queryKey: communityKeys.talkThreads(slug) });
      qc.invalidateQueries({ queryKey: communityKeys.changes() });
    },
  });
}

export interface EditMessageInput {
  id: number;
  threadId: number;
  body: string;
}

/** `PATCH /api/talk/messages/{id}/`. Author or staff only (server-enforced). */
export function useUpdateTalkMessage(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, body }: EditMessageInput) => {
      const { data } = await api.patch<TalkMessage>(`/talk/messages/${id}/`, {
        body,
      });
      return data;
    },
    onSuccess: (_message, variables) => {
      qc.invalidateQueries({
        queryKey: communityKeys.talkThread(variables.threadId),
      });
      qc.invalidateQueries({ queryKey: communityKeys.talkThreads(slug) });
    },
  });
}

/**
 * `DELETE /api/talk/messages/{id}/` — a SOFT delete.
 *
 * The row survives so replies are not orphaned and the audit trail holds;
 * the serializer withholds `body` and `author` from non-staff afterwards.
 * The UI therefore renders a tombstone, never an empty bubble.
 */
export function useDeleteTalkMessage(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id }: { id: number; threadId: number }) => {
      await api.delete(`/talk/messages/${id}/`);
    },
    onSuccess: (_void, variables) => {
      qc.invalidateQueries({
        queryKey: communityKeys.talkThread(variables.threadId),
      });
      qc.invalidateQueries({ queryKey: communityKeys.talkThreads(slug) });
      qc.invalidateQueries({ queryKey: communityKeys.changes() });
    },
  });
}

/* =====================================================================
   Watching
   ===================================================================== */

/**
 * `POST` / `DELETE /api/articles/{slug}/watch/` (DECISIONS §17).
 *
 * Optimistic against the article detail cache, which is where `is_watched`
 * lives, so the star flips on the click rather than on the round trip. The
 * snapshot taken in `onMutate` is restored in `onError`; the *toast* is
 * raised by the caller, because only the caller knows the article title and
 * a rollback the reader cannot see is worse than no optimism at all.
 */
export function useToggleWatch(slug: string) {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async (next: boolean) => {
      if (next) {
        await api.post(`/articles/${slug}/watch/`);
      } else {
        await api.delete(`/articles/${slug}/watch/`);
      }
      return next;
    },

    onMutate: async (next) => {
      const key = articleKeys.detail(slug);
      await qc.cancelQueries({ queryKey: key });
      const previous = qc.getQueryData<ArticleDetail>(key);
      if (previous) {
        qc.setQueryData<ArticleDetail>(key, { ...previous, is_watched: next });
      }
      return { previous };
    },

    onError: (_error, _next, context) => {
      if (context?.previous) {
        qc.setQueryData(articleKeys.detail(slug), context.previous);
      }
    },

    onSettled: () => {
      qc.invalidateQueries({ queryKey: articleKeys.detail(slug) });
      qc.invalidateQueries({ queryKey: communityKeys.watchlist() });
    },
  });
}
