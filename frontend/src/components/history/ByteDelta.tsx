import { byteDeltaTone, cn, formatByteDelta, formatNumber } from "@/lib/utils";

/**
 * Past this many bytes the delta goes bold, exactly as MediaWiki does. It is
 * the "somebody changed a lot here" signal that makes a history page scannable
 * without reading a single summary.
 */
export const BOLD_THRESHOLD = 500;

interface ByteDeltaProps {
  /** Signed. `null` means the row carries no byte information at all. */
  value: number | null;
  className?: string;
}

/** The three colour tokens, keyed by the tone `byteDeltaTone` reports. */
const TONE = {
  positive: "text-delta-pos",
  negative: "text-delta-neg",
  null: "text-delta-null",
} as const;

/**
 * A signed byte delta: `+1,423`, `−96`, `0`, or an em dash when there is no
 * byte information.
 *
 * Three channels carry the meaning, and the visual one is deliberately the
 * least important of them:
 *
 *  1. **The sign.** Always explicit, and a MINUS SIGN (U+2212) rather than a
 *     hyphen. Colour is therefore never the only channel (WCAG 1.4.1), which
 *     matters here more than anywhere else in the app: red/green deltas are
 *     exactly the pair ~8% of men cannot separate.
 *  2. **Weight.** Bold past ±500 bytes, so magnitude survives greyscale.
 *  3. **Colour.** `--delta-pos` / `--delta-neg` / `--delta-null`.
 *
 * The visible glyph is `aria-hidden` and paired with a full sentence for a
 * screen reader, because "plus one comma four two three" is not what a reader
 * of a history page needs to hear on every row.
 */
export function ByteDelta({ value, className }: ByteDeltaProps) {
  const tone = byteDeltaTone(value);
  const label = describe(value);

  return (
    <span
      title={label}
      className={cn(
        "tabular-nums",
        TONE[tone],
        value !== null && Math.abs(value) >= BOLD_THRESHOLD && "font-bold",
        className,
      )}
    >
      <span aria-hidden="true">{formatByteDelta(value)}</span>
      <span className="sr-only">{label}</span>
    </span>
  );
}

function describe(value: number | null): string {
  if (value === null) return "no size information";
  if (value === 0) return "no change in size";
  const bytes = `${formatNumber(Math.abs(value))} bytes`;
  return value > 0 ? `${bytes} added` : `${bytes} removed`;
}
