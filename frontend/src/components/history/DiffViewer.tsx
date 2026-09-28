import { type ReactNode, useEffect, useState } from "react";

import { InlineRows, SplitRow } from "@/components/history/DiffLine";
import { useIsShelf } from "@/hooks/useMediaQuery";
import type { DiffHunk, DiffPayload } from "@/lib/types";
import { cn, formatNumber, MINUS } from "@/lib/utils";

/**
 * The diff table.
 *
 * Everything here renders a payload that the server already computed
 * (`backend/apps/articles/diff.py`) — the client never diffs. What it adds is
 * the reading apparatus MediaWiki's diff lacks or hides:
 *
 *  - **Two layouts.** Side-by-side above `shelf`, unified below it, with a
 *    persisted toggle in between. Wikipedia's inline diff is a beta gadget;
 *    here it ships, because six columns do not fit a phone.
 *  - **Line numbers on both sides.** Wikipedia gives you a hunk header and
 *    leaves you to count.
 *  - **A `−` / `+` gutter and a legend**, so the four `--diff-*` tints are
 *    never the only channel carrying "removed" and "added".
 *  - **Honesty about truncation.** Five server-side valves can cut a diff
 *    short; when one fires, the reader is told rather than shown a quietly
 *    wrong comparison.
 */

export type DiffMode = "split" | "inline";

const MODE_KEY = "wikiverse.diff.mode";

function readMode(): DiffMode {
  try {
    return localStorage.getItem(MODE_KEY) === "inline" ? "inline" : "split";
  } catch {
    // Blocked storage is a preference we do without, not an error.
    return "split";
  }
}

interface DiffViewerProps {
  diff: DiffPayload;
  className?: string;
}

export function DiffViewer({ diff, className }: DiffViewerProps) {
  const [preferred, setPreferred] = useState<DiffMode>(readMode);
  const isShelf = useIsShelf();

  // Below `shelf` the six-column layout cannot fit, so unified is not a
  // preference there — it is the only honest rendering. The stored preference
  // is left untouched, so widening the window restores it.
  const mode: DiffMode = isShelf ? preferred : "inline";

  useEffect(() => {
    try {
      localStorage.setItem(MODE_KEY, preferred);
    } catch {
      /* Ignored: see readMode. */
    }
  }, [preferred]);

  const { hunks, stats } = diff;
  const columns = mode === "split" ? 6 : 4;

  return (
    <div className={cn("mt-4", className)}>
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2">
        <Stats diff={diff} />
        {isShelf && <ModeToggle mode={preferred} onChange={setPreferred} />}
      </div>

      {diff.created && (
        <Notice tone="notice">
          This revision created the page, so every line below is an addition.
        </Notice>
      )}
      {diff.title_changed && (
        <Notice tone="notice">
          The article title changed between these two revisions. A title is not
          part of the body, so it does not appear in the table below.
        </Notice>
      )}
      {diff.summary_changed && (
        <Notice tone="notice">
          The article summary changed between these two revisions. The summary
          is stored separately from the body and is not shown below.
        </Notice>
      )}
      {diff.truncated && (
        <Notice tone="content">
          This comparison is incomplete. The revisions are large enough that the
          server stopped short of rendering every line, or a single line was too
          long to compare word by word and is shown as a whole-line change. Some
          differences are therefore not displayed.
        </Notice>
      )}

      {hunks.length === 0 ? (
        <p className="mt-3 rounded-chrome border border-rule-hair bg-panel px-4 py-6 text-ui text-ink-2">
          <strong className="font-medium text-ink">No difference.</strong>{" "}
          {stats.lines_added + stats.lines_removed + stats.lines_changed === 0
            ? "The body of these two revisions is byte for byte identical."
            : "Nothing in the body of the article changed between these two revisions."}
        </p>
      ) : (
        <>
          <Legend />
          <table
            className={cn(
              "mt-2 w-full table-fixed border-collapse",
              "font-mono text-xs leading-[1.6]",
            )}
          >
            <caption className="sr-only">
              {mode === "split"
                ? "Comparison of two revisions, the older revision on the left and the newer on the right."
                : "Comparison of two revisions, removed lines followed by added lines."}{" "}
              Removed text is marked “removed” and added text “added”.
            </caption>

            <colgroup>
              {mode === "split" ? (
                <>
                  <col className="w-12" />
                  <col className="w-7" />
                  <col />
                  <col className="w-12" />
                  <col className="w-7" />
                  <col />
                </>
              ) : (
                <>
                  <col className="w-12" />
                  <col className="w-12" />
                  <col className="w-7" />
                  <col />
                </>
              )}
            </colgroup>

            <tbody>
              {hunks.map((hunk, index) => (
                <HunkBody
                  key={`${hunk.a_start}-${hunk.b_start}`}
                  hunk={hunk}
                  previous={index > 0 ? hunks[index - 1] : null}
                  mode={mode}
                  columns={columns}
                />
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

/* ---------------------------------------------------------------------------
   One hunk: the skipped run above it, its header, then its rows
   ------------------------------------------------------------------------- */

interface HunkBodyProps {
  hunk: DiffHunk;
  previous: DiffHunk | null;
  mode: DiffMode;
  columns: number;
}

function HunkBody({ hunk, previous, mode, columns }: HunkBodyProps) {
  // Everything between two hunks is unchanged, and the payload deliberately
  // omits it. The gap is arithmetic on the old side's line numbers.
  const skipped = previous
    ? hunk.a_start - (previous.a_start + previous.a_lines)
    : 0;

  return (
    <>
      {skipped > 0 && (
        <tr>
          <td
            colSpan={columns}
            className="border-y border-rule-hair bg-panel px-2 py-1.5 text-center font-sans text-xs text-ink-2"
          >
            {formatNumber(skipped)} unchanged{" "}
            {skipped === 1 ? "line" : "lines"}
          </td>
        </tr>
      )}

      <tr>
        {mode === "split" ? (
          <>
            <td colSpan={3} className={HUNK_HEADER}>
              Line {formatNumber(hunk.a_start)}:
            </td>
            <td colSpan={3} className={HUNK_HEADER}>
              Line {formatNumber(hunk.b_start)}:
            </td>
          </>
        ) : (
          <td colSpan={4} className={HUNK_HEADER}>
            Line {formatNumber(hunk.a_start)} {"→"}{" "}
            {formatNumber(hunk.b_start)}:
          </td>
        )}
      </tr>

      {hunk.rows.map((row, index) =>
        mode === "split" ? (
          <SplitRow key={`${row.t}-${row.a}-${row.b}-${index}`} row={row} />
        ) : (
          <InlineRows key={`${row.t}-${row.a}-${row.b}-${index}`} row={row} />
        ),
      )}
    </>
  );
}

const HUNK_HEADER =
  "px-2 pt-3 pb-1 font-sans text-base font-bold tabular-nums text-ink-2";

/* ---------------------------------------------------------------------------
   Apparatus
   ------------------------------------------------------------------------- */

/**
 * The document-wide counts. They come from the FULL opcode stream, so they
 * remain accurate even when a valve cut the rendered hunks short — which is
 * exactly why they are printed above a possibly-truncated table.
 */
function Stats({ diff }: { diff: DiffPayload }) {
  const { lines_added, lines_removed, lines_changed, bytes_added, bytes_removed } =
    diff.stats;

  return (
    <p className="text-ui text-ink-2">
      <span className="tabular-nums text-delta-pos">
        +{formatNumber(bytes_added)}
      </span>
      {" / "}
      <span className="tabular-nums text-delta-neg">
        {MINUS}
        {formatNumber(bytes_removed)}
      </span>{" "}
      bytes
      {" · "}
      <span className="tabular-nums">{formatNumber(lines_added)}</span> added,{" "}
      <span className="tabular-nums">{formatNumber(lines_removed)}</span>{" "}
      removed,{" "}
      <span className="tabular-nums">{formatNumber(lines_changed)}</span> changed
    </p>
  );
}

/**
 * The legend is what makes the single-glyph gutter accessible to a sighted
 * reader who cannot separate the two tints — the same reasoning as the Recent
 * changes legend, and the same 12px size.
 */
function Legend() {
  return (
    <p className="mt-3 text-2xs text-ink-2">
      <span aria-hidden="true">{MINUS}</span> removed from the older revision
      {" · "}
      <span aria-hidden="true">+</span> added in the newer revision
      {" · "}
      highlighted words changed within a line
    </p>
  );
}

interface ModeToggleProps {
  mode: DiffMode;
  onChange: (mode: DiffMode) => void;
}

/**
 * A two-button segmented control rather than a `<select>`: two options, both
 * worth naming, and `aria-pressed` states what a `<select>` would only imply.
 */
function ModeToggle({ mode, onChange }: ModeToggleProps) {
  return (
    <div
      role="group"
      aria-label="Diff display"
      className="inline-flex overflow-hidden rounded-chrome border border-rule"
    >
      <ModeButton pressed={mode === "split"} onClick={() => onChange("split")}>
        Side by side
      </ModeButton>
      <ModeButton
        pressed={mode === "inline"}
        onClick={() => onChange("inline")}
        className="border-l border-rule"
      >
        Inline
      </ModeButton>
    </div>
  );
}

function ModeButton({
  pressed,
  onClick,
  className,
  children,
}: {
  pressed: boolean;
  onClick: () => void;
  className?: string;
  children: string;
}) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      onClick={onClick}
      className={cn(
        "cursor-pointer px-2.5 py-1 text-ui transition-colors duration-100",
        "motion-reduce:transition-none",
        pressed
          ? "bg-panel font-semibold text-ink"
          : "text-link hover:bg-panel hover:text-link-hover",
        className,
      )}
    >
      {children}
    </button>
  );
}

/**
 * A maintenance-banner-shaped note: a 10px colour-coded left rule on the panel
 * surface, which is the one place in this design where a saturated colour is
 * allowed to carry meaning, because the rule is not text and nothing is set on
 * top of it.
 */
function Notice({
  tone,
  children,
}: {
  tone: "notice" | "content";
  children: ReactNode;
}) {
  return (
    <p
      className={cn(
        "mt-3 border-l-[10px] bg-panel px-3 py-2 text-ui text-ink",
        tone === "notice" ? "border-l-banner-notice" : "border-l-banner-content",
      )}
    >
      {children}
    </p>
  );
}
