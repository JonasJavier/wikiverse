import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes with conflict resolution. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/* =====================================================================
   Numbers
   =====================================================================
   `tabular-nums` is set on `body`, so every number these helpers produce
   is already in tabular figures without a call site asking. Group
   separators are explicit ("en") rather than locale-default, because a
   revision id that changes shape with the reader's locale is a bug.
   ===================================================================== */

const GROUPED = new Intl.NumberFormat("en", { useGrouping: true });

/** `1423` -> `"1,423"`. The default presentation for any count in the UI. */
export function formatNumber(n: number): string {
  return GROUPED.format(n);
}

/**
 * Compact counts for dense metadata: `1234` -> `"1.2k"`, `2_500_000` ->
 * `"2.5M"`. Use `formatNumber` wherever the exact figure is the point
 * (byte sizes, revision counts, result totals).
 */
export function formatCount(n: number): string {
  if (Math.abs(n) < 1000) return String(n);
  if (Math.abs(n) < 1_000_000) {
    return `${(n / 1000).toFixed(1).replace(/\.0$/, "")}k`;
  }
  return `${(n / 1_000_000).toFixed(1).replace(/\.0$/, "")}M`;
}

/** U+2212 MINUS SIGN. Never a hyphen: a hyphen next to a digit reads wrong. */
export const MINUS = "−";

/** U+2014 EM DASH, the "there is no value here" glyph. */
export const EM_DASH = "—";

/**
 * A signed byte delta, exactly as a wiki prints it: `"+1,423"`, `"−96"`,
 * `"0"`. The sign is always explicit so colour is never the only channel
 * carrying the meaning (WCAG 1.4.1).
 *
 * `null` means "this row has no byte information at all" — every talk row
 * in Recent Changes, the watchlist and contributions — and renders as an em
 * dash rather than a misleading `0`.
 */
export function formatByteDelta(delta: number | null): string {
  if (delta === null) return EM_DASH;
  if (delta === 0) return "0";
  if (delta > 0) return `+${formatNumber(delta)}`;
  return `${MINUS}${formatNumber(Math.abs(delta))}`;
}

/**
 * Which of the three delta colours a value takes: `--delta-pos`,
 * `--delta-neg` or `--delta-null`. Kept beside the formatter so the colour
 * and the sign can never disagree.
 */
export function byteDeltaTone(
  delta: number | null,
): "positive" | "negative" | "null" {
  if (delta === null || delta === 0) return "null";
  return delta > 0 ? "positive" : "negative";
}

/** `193713` -> `"193,713 bytes"`. The history-row presentation. */
export function formatBytes(bytes: number): string {
  return `${formatNumber(bytes)} bytes`;
}

/**
 * `9216` -> `"9 KB"`. The list-row presentation. 1 KB = 1024 bytes, and
 * anything under 1 KB reports as `"1 KB"` rather than `"0 KB"`, because a
 * stub is small, not empty.
 */
export function formatKb(bytes: number): string {
  return `${Math.max(1, Math.round(bytes / 1024))} KB`;
}

/* =====================================================================
   Dates and times
   =====================================================================
   Day-first, spelled-out month: "26 September 2026". That is the reference
   -work convention and it is unambiguous for every reader, which
   "9/26/2026" is not.
   ===================================================================== */

const DAY_MONTH_YEAR = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
});

const HOUR_MINUTE = new Intl.DateTimeFormat("en-GB", {
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
});

/** `"26 September 2026"`. Use for "Retrieved", "Joined", "Created". */
export function formatDate(iso: string): string {
  return DAY_MONTH_YEAR.format(new Date(iso));
}

/**
 * `"16:41, 26 September 2026"` — the revision-history and diff-header
 * format, time first, exactly as a wiki prints a timestamp.
 */
export function formatDateTime(iso: string): string {
  const d = new Date(iso);
  return `${HOUR_MINUTE.format(d)}, ${DAY_MONTH_YEAR.format(d)}`;
}

/** `"16:41"`. For a feed already grouped under a day heading. */
export function formatTime(iso: string): string {
  return HOUR_MINUTE.format(new Date(iso));
}

const RELATIVE_UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ["year", 60 * 60 * 24 * 365],
  ["month", 60 * 60 * 24 * 30],
  ["week", 60 * 60 * 24 * 7],
  ["day", 60 * 60 * 24],
  ["hour", 60 * 60],
  ["minute", 60],
];

const RELATIVE = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

/**
 * `"3 days ago"`, `"last month"`, `"just now"`. Always pair it with a
 * `<time dateTime={iso} title={formatDateTime(iso)}>` so the exact instant
 * is one hover or one screen-reader stop away — a relative time alone is
 * not enough for a revision history.
 */
export function formatRelativeTime(iso: string): string {
  const seconds = (Date.parse(iso) - Date.now()) / 1000;
  for (const [unit, secondsInUnit] of RELATIVE_UNITS) {
    if (Math.abs(seconds) >= secondsInUnit) {
      return RELATIVE.format(Math.round(seconds / secondsInUnit), unit);
    }
  }
  return "just now";
}

/* =====================================================================
   Misc
   ===================================================================== */

/** Two-letter fallback inside an `Avatar`. */
export function initials(name: string): string {
  return name.slice(0, 2).toUpperCase();
}

/**
 * The React key for a Recent-Changes / watchlist / contributions row.
 * `id` is unique only WITHIN a kind (an edit row is a Revision id, a talk
 * row is a TalkMessage id), so the kind has to be part of the key. Having
 * one helper means the three feeds cannot drift apart.
 */
export function changeRowKey(row: { kind: string; id: number }): string {
  return `${row.kind}-${row.id}`;
}

/**
 * The scroll behaviour to pass to `scrollIntoView` / `scrollTo`.
 *
 * `scroll-behavior: smooth` is deliberately absent from the stylesheet
 * (DECISIONS §18) because it fights focus management and hurts the
 * footnote jump. Programmatic scrolling therefore chooses per call, and
 * honours the reader's motion preference.
 */
export function scrollBehavior(): ScrollBehavior {
  if (typeof window === "undefined" || !window.matchMedia) return "auto";
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ? "auto"
    : "smooth";
}
