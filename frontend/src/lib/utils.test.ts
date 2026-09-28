import { afterEach, describe, expect, it, vi } from "vitest";

import {
  byteDeltaTone,
  changeRowKey,
  cn,
  EM_DASH,
  formatByteDelta,
  formatBytes,
  formatCount,
  formatDate,
  formatDateTime,
  formatKb,
  formatNumber,
  formatRelativeTime,
  formatTime,
  initials,
  MINUS,
  scrollBehavior,
} from "./utils";
import { stubMatchMedia } from "@/test/render";

afterEach(() => {
  vi.useRealTimers();
});

describe("cn (tailwind-merge with the custom type scale)", () => {
  it("keeps a colour and a custom font size together", () => {
    // Regression: `text-ui` used to be read as a colour and evicted `text-page`,
    // which rendered every primary button's label ink-on-ink.
    const merged = cn("bg-ink text-page", "text-ui").split(" ");
    expect(merged).toEqual(expect.arrayContaining(["bg-ink", "text-page", "text-ui"]));
  });

  it("lets a later custom font size replace an earlier one", () => {
    expect(cn("text-ui", "text-h1")).toBe("text-h1");
    expect(cn("text-2xs font-bold", "text-read")).toBe("font-bold text-read");
  });

  it("still resolves ordinary conflicts and drops falsy inputs", () => {
    expect(cn("px-2", false, null, undefined, "px-4")).toBe("px-4");
    expect(cn("text-ink", "text-link")).toBe("text-link");
  });
});

describe("numbers", () => {
  it("groups with commas regardless of the reader's locale", () => {
    expect(formatNumber(1423)).toBe("1,423");
    expect(formatNumber(193713)).toBe("193,713");
    expect(formatBytes(193713)).toBe("193,713 bytes");
  });

  it.each([
    [999, "999"],
    [1000, "1k"],
    [1234, "1.2k"],
    [2_500_000, "2.5M"],
    [-1500, "-1.5k"],
  ])("formatCount(%i) → %s", (n, out) => {
    expect(formatCount(n)).toBe(out);
  });

  it("reports sizes in whole KB, never 0 KB", () => {
    expect(formatKb(9216)).toBe("9 KB");
    expect(formatKb(10)).toBe("1 KB");
    expect(formatKb(0)).toBe("1 KB");
  });
});

describe("byte deltas", () => {
  it.each([
    [1423, "+1,423", "positive"],
    [-96, `${MINUS}96`, "negative"],
    [-12345, "−12,345", "negative"],
    [0, "0", "null"],
    [null, EM_DASH, "null"],
  ] as const)("%j → %s (%s)", (delta, text, tone) => {
    expect(formatByteDelta(delta)).toBe(text);
    expect(byteDeltaTone(delta)).toBe(tone);
  });

  it("uses U+2212 MINUS SIGN, never a hyphen", () => {
    expect(formatByteDelta(-1).charCodeAt(0)).toBe(0x2212);
    expect(formatByteDelta(-1)).not.toContain("-");
  });
});

describe("dates (test zone pinned to UTC−4 in vitest.config.ts)", () => {
  it("runs in the pinned zone", () => {
    expect(Intl.DateTimeFormat().resolvedOptions().timeZone).toBe("America/Santo_Domingo");
  });

  it("formats a date-only accessed_on as that calendar day, in any zone", () => {
    // `new Date("2026-09-26")` is UTC midnight: 20:00 on the 25th in UTC−4.
    expect(formatDate("2026-09-26")).toBe("26 September 2026");
    expect(formatDate("2026-01-01")).toBe("1 January 2026");
  });

  it("formats a timestamp in the reader's own zone", () => {
    expect(formatDate("2026-09-26T02:00:00Z")).toBe("25 September 2026");
    expect(formatDateTime("2026-09-26T20:41:00Z")).toBe("16:41, 26 September 2026");
    expect(formatTime("2026-09-26T20:41:00Z")).toBe("16:41");
  });

  it("formats relative times against now", () => {
    vi.useFakeTimers({ now: Date.parse("2026-09-27T12:00:00Z"), toFake: ["Date"] });
    expect(formatRelativeTime("2026-09-27T11:59:30Z")).toBe("just now");
    expect(formatRelativeTime("2026-09-27T11:55:00Z")).toBe("5 minutes ago");
    expect(formatRelativeTime("2026-09-24T12:00:00Z")).toBe("3 days ago");
    expect(formatRelativeTime("2026-09-26T12:00:00Z")).toBe("yesterday");
  });
});

describe("misc", () => {
  it("initials are the first two letters, upper-cased", () => {
    expect(initials("ada")).toBe("AD");
    expect(initials("élodie")).toBe("ÉL");
    expect(initials("x")).toBe("X");
  });

  it("initials never split an astral character into a lone surrogate", () => {
    const out = initials("𝒳avier");
    expect(Array.from(out)).toEqual(["𝒳", "A"]);
    expect(out).not.toMatch(/[\uD800-\uDFFF](?![\uDC00-\uDFFF])/u);
  });

  it("change-row keys combine kind and id (DECISIONS §4)", () => {
    expect(changeRowKey({ kind: "edit", id: 7 })).toBe("edit-7");
    expect(changeRowKey({ kind: "talk", id: 7 })).toBe("talk-7");
  });

  it("scrollBehavior honours prefers-reduced-motion", () => {
    stubMatchMedia((query) => query.includes("reduce"));
    expect(scrollBehavior()).toBe("auto");
    stubMatchMedia(() => false);
    expect(scrollBehavior()).toBe("smooth");
  });
});
