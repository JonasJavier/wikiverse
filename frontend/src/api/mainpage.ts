/**
 * The main page's own data: `GET /api/main-page/`, the newest few change-feed
 * rows, and the red-link oracle.
 *
 * DECISIONS §5 defines one endpoint for the whole front page, cached in Redis
 * server-side, so the reader pays exactly one request for Featured article,
 * Did you know…, On this day and the site statistics. "In the news" is cut and
 * has no hook here.
 */

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type {
  ChangeFeed,
  MainPage,
  MainPageFeatured,
  OnThisDayEntry,
  SiteStats,
} from "@/lib/types";

/* =====================================================================
   Response shapes: two narrow widenings of the types in lib/types.ts
   =====================================================================
   Both exist because the serializer is more permissive than the type, and
   a page that trusts the narrower type renders a blank panel instead of a
   fallback. Neither redefines a type — each is expressed in terms of the
   canonical one, so a fix in lib/types.ts propagates here.

   1. `featured` is `allow_null=True` in `MainPageSerializer`, and the view's
      fallback (most-viewed article) still returns null on a database with no
      published articles at all. `MainPage.featured` is non-nullable.
   2. `OnThisDaySerializer` declares `year`, `month` and `day` with
      `allow_null=True`, mirroring the nullable `MainPageBlock` columns.
      `OnThisDayEntry` types all three as `number`.
   ===================================================================== */

/** One "On this day" row as the serializer can actually send it. */
export type OnThisDayRow = {
  [K in keyof OnThisDayEntry]: K extends "body"
    ? OnThisDayEntry[K]
    : OnThisDayEntry[K] | null;
};

/**
 * `SiteStatsSerializer` also carries `words` and `stubs`, which `SiteStats`
 * does not declare. They are optional here so the statistics sentence can
 * use them when present without asserting they exist.
 */
export interface MainPageStats extends SiteStats {
  words?: number;
  stubs?: number;
}

export interface MainPageResponse extends Omit<MainPage, "featured" | "otd" | "stats"> {
  featured: MainPageFeatured | null;
  otd: OnThisDayRow[];
  stats: MainPageStats;
}

export const mainPageKeys = {
  all: ["main-page"] as const,
  page: ["main-page", "payload"] as const,
  /** Namespaced under `main-page` so it cannot collide with a full changes feed. */
  latestChanges: (limit: number) => ["main-page", "latest-changes", limit] as const,
};

/** `GET /api/main-page/` — the whole front page in one request (DECISIONS §5). */
export function useMainPage() {
  return useQuery({
    queryKey: mainPageKeys.page,
    queryFn: async () => {
      const { data } = await api.get<MainPageResponse>("/main-page/");
      return data;
    },
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * The newest `limit` rows of `GET /api/changes/`, for the main page's Recent
 * changes panel. No `days` window: the feed's default is "no time filter", and
 * a front page that shows nothing because the corpus was seeded last week is
 * worse than one that shows the real latest edits.
 */
export function useLatestChanges(limit = 8) {
  return useQuery({
    queryKey: mainPageKeys.latestChanges(limit),
    queryFn: async () => {
      const { data } = await api.get<ChangeFeed>("/changes/", {
        params: { limit },
      });
      return data;
    },
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData,
  });
}
