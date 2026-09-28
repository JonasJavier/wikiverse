import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  CHANGES_FEED_URL,
  changeFiltersWithPage,
  changesQuery,
  contributionsQuery,
  DEFAULT_CHANGE_DAYS,
  DEFAULT_CHANGE_LIMIT,
  DEFAULT_CHANGE_TYPE,
  feedQuery,
  readChangeFilters,
  sinceFromDays,
  writeChangeFilters,
  type ChangeFilterState,
} from "./community";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

/** 14:37:12 UTC — deliberately not on the hour, so flooring is visible. */
const NOW = Date.UTC(2026, 8, 27, 14, 37, 12);
const HOUR_FLOOR = Date.UTC(2026, 8, 27, 14, 0, 0);
const DAY = 86_400_000;

function read(query: string): ChangeFilterState {
  return readChangeFilters(new URLSearchParams(query));
}

function sinceDaysAgo(days: number): string {
  return new Date(HOUR_FLOOR - days * DAY).toISOString();
}

beforeEach(() => {
  vi.useFakeTimers({ now: NOW, toFake: ["Date"] });
});

afterEach(() => {
  vi.useRealTimers();
});

describe("DECISIONS §4 defaults", () => {
  it("type all, days 7, limit 50", () => {
    expect(DEFAULT_CHANGE_TYPE).toBe("all");
    expect(DEFAULT_CHANGE_DAYS).toBe(7);
    expect(DEFAULT_CHANGE_LIMIT).toBe(50);
  });

  it("an empty URL reads as the defaults", () => {
    expect(read("")).toEqual({
      type: "all",
      user: "",
      category: "",
      hideMinor: false,
      hideBot: false,
      days: 7,
      limit: 50,
      before: "",
      page: 1,
    });
  });

  it("an empty URL sends exactly type, since and limit", () => {
    expect(changesQuery(read(""))).toEqual({
      type: "all",
      since: sinceDaysAgo(7),
      limit: 50,
    });
  });
});

describe("the URL → API mapping table (DECISIONS §4)", () => {
  it.each([
    ["type=edit", { type: "edit" }],
    ["type=talk", { type: "talk" }],
    ["user=Ada", { user: "Ada" }],
    ["category=physics", { category: "physics" }],
    ["hideMinor=1", { minor: "0" }],
    ["hideBot=1", { bots: "0" }],
    ["days=30", { since: sinceDaysAgo(30) }],
    ["limit=100", { limit: 100 }],
  ])("?%s", (query, expected) => {
    expect(changesQuery(read(query))).toMatchObject(expected);
  });

  it("maps everything at once", () => {
    expect(
      changesQuery(read("type=edit&user=Ada&category=physics&hideMinor=1&hideBot=1&days=1&limit=100")),
    ).toEqual({
      type: "edit",
      user: "Ada",
      category: "physics",
      minor: "0",
      bots: "0",
      since: sinceDaysAgo(1),
      limit: 100,
    });
  });

  it("never sends minor/bots/user/category when the filter is off or blank", () => {
    const query = changesQuery(read("hideMinor=0&hideBot=&user=%20%20&category="));
    expect(query).not.toHaveProperty("minor");
    expect(query).not.toHaveProperty("bots");
    expect(query).not.toHaveProperty("user");
    expect(query).not.toHaveProperty("category");
  });

  it("never sends `days` — it becomes `since`", () => {
    expect(changesQuery(read("days=30"))).not.toHaveProperty("days");
  });

  it("passes the `before` cursor through", () => {
    expect(changesQuery(read("before=2026-09-01T00:00:00Z")).before).toBe("2026-09-01T00:00:00Z");
  });
});

describe("readChangeFilters", () => {
  it("accepts only the literal affirmatives for the hide flags", () => {
    for (const on of ["1", "true", "yes", "on", " TRUE "]) {
      expect(read(`hideMinor=${encodeURIComponent(on)}`).hideMinor).toBe(true);
    }
    for (const off of ["0", "false", "", "nope"]) {
      expect(read(`hideBot=${off}`).hideBot).toBe(false);
    }
  });

  it("falls back to `all` for an unknown type", () => {
    expect(read("type=bogus").type).toBe("all");
    expect(read("type=ALL").type).toBe("all");
  });

  it("clamps days to 1–365 and limit to 1–100", () => {
    expect(read("days=0").days).toBe(1);
    expect(read("days=1000").days).toBe(365);
    expect(read("days=abc").days).toBe(7);
    expect(read("limit=500").limit).toBe(100);
    expect(read("limit=-5").limit).toBe(1);
    expect(read("limit=").limit).toBe(50);
  });

  it("trims user and category, and reads the page number", () => {
    const state = read("user=%20Ada%20&category=%20physics&page=3");
    expect(state.user).toBe("Ada");
    expect(state.category).toBe("physics");
    expect(state.page).toBe(3);
  });
});

describe("sinceFromDays", () => {
  it("is now minus N days, floored to the hour, in UTC ISO form", () => {
    expect(sinceFromDays(7, NOW)).toBe("2026-09-20T14:00:00.000Z");
    expect(sinceFromDays(1, NOW)).toBe("2026-09-26T14:00:00.000Z");
  });

  it("is stable within the hour, so it can live in a query key", () => {
    expect(sinceFromDays(7, NOW)).toBe(sinceFromDays(7, NOW + 20 * 60_000));
    expect(sinceFromDays(7, NOW)).not.toBe(sinceFromDays(7, NOW + 60 * 60_000));
  });

  it("defaults `now` to the current time", () => {
    expect(sinceFromDays(7)).toBe(sinceFromDays(7, NOW));
  });
});

describe("writeChangeFilters", () => {
  const defaults = read("");

  it("writes nothing for a pristine view", () => {
    expect(writeChangeFilters(defaults, {}).toString()).toBe("");
  });

  it("writes the URL params of the table, not the API params", () => {
    const search = writeChangeFilters(defaults, {
      type: "talk",
      user: "Ada",
      category: "physics",
      hideMinor: true,
      hideBot: true,
      days: 30,
      limit: 100,
    });
    expect(Object.fromEntries(search)).toEqual({
      type: "talk",
      user: "Ada",
      category: "physics",
      hideMinor: "1",
      hideBot: "1",
      days: "30",
      limit: "100",
    });
  });

  it("drops a parameter set back to its default", () => {
    const state = read("days=30&type=edit");
    expect(writeChangeFilters(state, { days: 7, type: "all" }).toString()).toBe("");
  });

  it("always drops the cursor and the page", () => {
    const state = read("before=2026-09-01T00:00:00Z&page=4&hideBot=1");
    expect(writeChangeFilters(state, {}).toString()).toBe("hideBot=1");
  });

  it("round-trips through readChangeFilters", () => {
    const state = read("type=edit&user=Ada&hideMinor=1&days=30&limit=100");
    expect(read(writeChangeFilters(state, {}).toString())).toEqual(state);
  });

  it("keeps the page only for page-numbered feeds, and only past page 1", () => {
    const state = read("hideMinor=1");
    expect(changeFiltersWithPage(state, 3).toString()).toBe("hideMinor=1&page=3");
    expect(changeFiltersWithPage(state, 1).toString()).toBe("hideMinor=1");
  });
});

describe("feedQuery / contributionsQuery", () => {
  it("the watchlist sends since and page, never type or limit", () => {
    const query = feedQuery(read("type=talk&limit=100&page=2&hideMinor=1&hideBot=1"));
    expect(query).toEqual({ since: sinceDaysAgo(7), page: 2, minor: "0", bots: "0" });
  });

  it("contributions are un-windowed: page only", () => {
    expect(contributionsQuery(2)).toEqual({ page: 2 });
  });

  it("the RSS feed lives at /api/feeds/changes.rss (DECISIONS §14)", () => {
    expect(CHANGES_FEED_URL).toBe("http://api.test/api/feeds/changes.rss");
  });
});
