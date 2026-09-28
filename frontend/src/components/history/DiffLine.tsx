import type { DiffOp, DiffRow } from "@/lib/types";
import { cn, MINUS } from "@/lib/utils";

/**
 * One row of a server-rendered diff, in both layouts.
 *
 * `DiffViewer` owns the table shell, the hunk headers and the mode toggle;
 * this module owns the cells. The split is worth a file because the *op*
 * rendering is the subtle part and it is shared: the payload's round-trip
 * invariant (joining a row's `=` and `-` texts reproduces the old line, its
 * `=` and `+` texts the new line) is what lets one payload drive side-by-side
 * and inline from the same data, and `<DiffOps>` is the single place that
 * property is relied upon.
 *
 * Whitespace is significant — the diffed text is Markdown source, where a
 * leading space changes the rendering — so every content cell is
 * `whitespace-pre-wrap`. A blank line arrives as `ops: []` and renders a
 * no-break space, so the row keeps its height and therefore its tint.
 */

/* ---------------------------------------------------------------------------
   Cell styling. Tints come from the four --diff-* tokens; the 4px leading
   rule is what keeps a row legible when the tint is a 12:1-contrast wash
   rather than a shout.
   ------------------------------------------------------------------------- */

const CELL = "px-2 py-1 align-top break-words whitespace-pre-wrap";
const CONTEXT = "bg-inset border-l-4 border-l-rule-hair";
const DELETED = "bg-diff-del-line border-l-4 border-l-diff-del-word";
const ADDED = "bg-diff-add-line border-l-4 border-l-diff-add-word";
/** The side of a one-sided row that has no line at all. */
const EMPTY = "bg-shell";

const NUM = "w-12 px-1 py-1 text-right align-top tabular-nums text-ink-3 select-none";
const MARKER = "px-0 py-1 text-center align-top text-ink-2 select-none";

const NBSP = " ";

/* ---------------------------------------------------------------------------
   Ops
   ------------------------------------------------------------------------- */

interface DiffOpsProps {
  ops: DiffOp[];
  /** Which reconstruction to render: the old line, or the new one. */
  side: "old" | "new";
}

const WORD = "rounded-[1px] py-[0.15em] font-bold text-ink no-underline";

/**
 * The text of one line, with the changed words wrapped.
 *
 * `<del>` and `<ins>` rather than `<span>`: they are the HTML elements that
 * *mean* removed and added, so the word-level highlight is carried by the
 * markup and not only by the two `--diff-*-word` tints. Their default
 * line-through / underline is removed — a tint plus a strike is noise, and the
 * element still announces.
 */
export function DiffOps({ ops, side }: DiffOpsProps) {
  const changed = side === "old" ? "-" : "+";
  const visible = ops.filter(([kind]) => kind === "=" || kind === changed);

  if (visible.length === 0) {
    // A blank line, or a line that exists only on the other side.
    return <span aria-hidden="true">{NBSP}</span>;
  }

  return (
    <>
      {visible.map(([kind, text], index) =>
        kind === "=" ? (
          <span key={index}>{text}</span>
        ) : side === "old" ? (
          <del key={index} className={cn(WORD, "bg-diff-del-word")}>
            {text}
          </del>
        ) : (
          <ins key={index} className={cn(WORD, "bg-diff-add-word")}>
            {text}
          </ins>
        ),
      )}
    </>
  );
}

/**
 * Whether a row's two sides are in fact identical.
 *
 * Almost always `t === "="`, but not only: the line diff pairs a run of
 * changed lines position by position, so two blank lines inside one changed
 * block arrive as a `~` row with `ops: []`. Painting that as a change — a
 * tinted row with a `−` and a `+` and nothing between them — is a small lie
 * the reader has to stop and check. Verified against the engine: the fixture
 * in `diff.py`'s own docstring produces exactly such a row.
 */
function isUnchanged(row: DiffRow): boolean {
  if (row.t === "=") return true;
  if (row.t !== "~") return false;
  return !row.ops.some(([kind]) => kind !== "=");
}

/* ---------------------------------------------------------------------------
   Side-by-side
   ------------------------------------------------------------------------- */

/**
 * One row of the 6-column side-by-side table:
 * old line number · old marker · old text · new line number · new marker · new text.
 *
 * The marker cells carry the `−` / `+` glyph for sighted readers and a
 * visually-hidden word for everybody else, so the meaning survives both
 * greyscale and a screen reader. Context rows get no marker word at all: a
 * 300-row diff that announces "unchanged" 280 times is unusable.
 */
export function SplitRow({ row }: { row: DiffRow }) {
  const hasOld = row.a !== null;
  const hasNew = row.b !== null;
  const isContext = isUnchanged(row);

  return (
    <tr>
      <Num value={row.a} empty={!hasOld} />
      <Marker kind={!hasOld ? "none" : isContext ? "context" : "removed"} />
      <td className={cn(CELL, !hasOld ? EMPTY : isContext ? CONTEXT : DELETED)}>
        {hasOld && <DiffOps ops={row.ops} side="old" />}
      </td>

      <Num value={row.b} empty={!hasNew} />
      <Marker kind={!hasNew ? "none" : isContext ? "context" : "added"} />
      <td className={cn(CELL, !hasNew ? EMPTY : isContext ? CONTEXT : ADDED)}>
        {hasNew && <DiffOps ops={row.ops} side="new" />}
      </td>
    </tr>
  );
}

/* ---------------------------------------------------------------------------
   Inline / unified
   ------------------------------------------------------------------------- */

/**
 * The same row in the 4-column unified table: old number · new number ·
 * marker · text. A modified row (`~`) becomes two rows, removed above added,
 * which is what makes the mode readable at phone width where six columns
 * cannot be.
 */
export function InlineRows({ row }: { row: DiffRow }) {
  if (isUnchanged(row)) {
    return (
      <tr>
        <Num value={row.a} />
        <Num value={row.b} />
        <Marker kind="context" />
        <td className={cn(CELL, CONTEXT)}>
          <DiffOps ops={row.ops} side="old" />
        </td>
      </tr>
    );
  }

  return (
    <>
      {row.a !== null && (
        <tr>
          <Num value={row.a} />
          <Num value={null} />
          <Marker kind="removed" />
          <td className={cn(CELL, DELETED)}>
            <DiffOps ops={row.ops} side="old" />
          </td>
        </tr>
      )}
      {row.b !== null && (
        <tr>
          <Num value={null} />
          <Num value={row.b} />
          <Marker kind="added" />
          <td className={cn(CELL, ADDED)}>
            <DiffOps ops={row.ops} side="new" />
          </td>
        </tr>
      )}
    </>
  );
}

/* ---------------------------------------------------------------------------
   Gutter cells
   ------------------------------------------------------------------------- */

/**
 * A line number, or nothing where the line does not exist on that side.
 *
 * `aria-hidden` on purpose. The numbers are navigational furniture for the
 * eye; a screen reader gets the position from the hunk header ("Line 48:"),
 * which is a real, announced row, and hearing two numbers before every line of
 * a long diff buries the actual change.
 */
function Num({ value, empty }: { value: number | null; empty?: boolean }) {
  return (
    <td aria-hidden="true" className={cn(NUM, empty && EMPTY)}>
      {value === null ? "" : value}
    </td>
  );
}

type MarkerKind = "removed" | "added" | "context" | "none";

const MARKER_GLYPH: Record<MarkerKind, string> = {
  removed: MINUS,
  added: "+",
  context: "",
  none: "",
};

const MARKER_LABEL: Record<MarkerKind, string> = {
  removed: "removed:",
  added: "added:",
  context: "",
  none: "",
};

/** The `−` / `+` gutter: a glyph for the eye, a word for the screen reader. */
function Marker({ kind }: { kind: MarkerKind }) {
  const label = MARKER_LABEL[kind];
  return (
    <td className={cn(MARKER, kind === "none" && EMPTY)}>
      <span aria-hidden="true">{MARKER_GLYPH[kind] || NBSP}</span>
      {label && <span className="sr-only">{label}</span>}
    </td>
  );
}
