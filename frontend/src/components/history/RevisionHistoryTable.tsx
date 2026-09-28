import { Link } from "react-router-dom";

import { ByteDelta } from "@/components/history/ByteDelta";
import { Button } from "@/components/ui/Button";
import type { Revision } from "@/lib/types";
import { cn, formatBytes, formatDateTime, formatNumber } from "@/lib/utils";

/**
 * MediaWiki's revision history, including the two-radio comparison control,
 * because that control is what teaches a reader the diff model: you do not
 * "open a diff", you pick two points in a history and ask what happened
 * between them.
 *
 * Two deliberate departures from MediaWiki:
 *
 *  1. **It is a real `<table>`** with `<caption>`, `scope="col"` headers and a
 *     `scope="row"` timestamp, not a `<ul>` of flowed text. Eight columns of
 *     numbers, flags and deltas *are* tabular data, and MediaWiki's list
 *     markup is precisely why its history page is close to unusable with a
 *     screen reader: every cell arrives as an unlabelled fragment.
 *  2. **The invalid pair is unreachable, not rejected.** Rows at or newer than
 *     the selected newer revision have their "older" radio disabled and vice
 *     versa, so "older on the left" is enforced by the control instead of
 *     validated after the fact. Nothing here can ever submit a backwards diff.
 *
 * The selection lives in the URL (`?oldid=&diff=`), which is what makes a
 * pending comparison shareable and — because the URL carries the slug too —
 * what makes the old "selection survives a navigation to another article" bug
 * structurally impossible rather than merely fixed.
 */

interface RevisionHistoryTableProps {
  slug: string;
  /** For the caption. The `h1` above the table owns the visible title. */
  title: string;
  revisions: Revision[];
  /** Total across every page, from the envelope's `count`. */
  count: number;
  /**
   * The article's newest revision id. `cur` is a diff against it, so without
   * it (on page 2 and beyond, before the article detail resolves) the link is
   * rendered as plain text rather than pointed somewhere wrong.
   */
  latestId: number | null;
  /** Selected OLDER revision, or null. */
  oldid: number | null;
  /** Selected NEWER revision, or null. */
  newid: number | null;
  onSelect: (side: "old" | "new", id: number) => void;
  onCompare: () => void;
}

const CELL = "px-2 py-1.5 align-baseline";
const NOWRAP = "whitespace-nowrap";
const HEAD =
  "px-2 pb-1 text-left align-bottom text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase";

export function RevisionHistoryTable({
  slug,
  title,
  revisions,
  count,
  latestId,
  oldid,
  newid,
  onSelect,
  onCompare,
}: RevisionHistoryTableProps) {
  const canCompare = oldid !== null && newid !== null && oldid < newid;

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (canCompare) onCompare();
      }}
    >
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 border-b border-rule pb-2">
        <Button size="sm" variant="secondary" type="submit" disabled={!canCompare}>
          Compare selected revisions
        </Button>
        <span className="text-ui tabular-nums text-ink-2">
          {formatNumber(count)} {count === 1 ? "revision" : "revisions"}
        </span>
      </div>

      {/* Announced once per change, not per keystroke: a radio group emits one
          change event per selection, which is exactly the granularity a reader
          wants here. */}
      <p aria-live="polite" className="sr-only">
        {selectionSentence(revisions, oldid, newid, canCompare)}
      </p>

      <table className="w-full border-collapse text-ui">
        <caption className="sr-only">
          Revision history of {title}. {formatNumber(count)}{" "}
          {count === 1 ? "revision" : "revisions"} in total, newest first. Pick
          an older and a newer revision with the radio buttons in the first two
          columns, then activate “Compare selected revisions”.
        </caption>

        <thead>
          <tr className="border-b border-rule">
            <th scope="col" className={cn(HEAD, "w-8 px-1")}>
              Older
            </th>
            <th scope="col" className={cn(HEAD, "w-8 px-1")}>
              Newer
            </th>
            <th scope="col" className={cn(HEAD, NOWRAP)}>
              Diff
            </th>
            <th scope="col" className={cn(HEAD, NOWRAP)}>
              Date and time
            </th>
            <th scope="col" className={cn(HEAD, NOWRAP)}>
              Editor
            </th>
            <th scope="col" className={cn(HEAD, NOWRAP)}>
              Size
            </th>
            <th scope="col" className={cn(HEAD, NOWRAP)}>
              Change
            </th>
            <th scope="col" className={HEAD}>
              Edit summary
            </th>
          </tr>
        </thead>

        <tbody>
          {revisions.map((revision) => (
            <HistoryRow
              key={revision.id}
              slug={slug}
              revision={revision}
              latestId={latestId}
              oldid={oldid}
              newid={newid}
              onSelect={onSelect}
            />
          ))}
        </tbody>
      </table>

      <div className="mt-2 border-t border-rule pt-2">
        <Button size="sm" variant="secondary" type="submit" disabled={!canCompare}>
          Compare selected revisions
        </Button>
      </div>
    </form>
  );
}

/* ---------------------------------------------------------------------------
   One row
   ------------------------------------------------------------------------- */

interface HistoryRowProps {
  slug: string;
  revision: Revision;
  latestId: number | null;
  oldid: number | null;
  newid: number | null;
  onSelect: (side: "old" | "new", id: number) => void;
}

function HistoryRow({
  slug,
  revision,
  latestId,
  oldid,
  newid,
  onSelect,
}: HistoryRowProps) {
  const { id, parent, editor, comment, created_at, byte_size, byte_delta } =
    revision;
  const when = formatDateTime(created_at);
  const isLatest = latestId !== null && id === latestId;

  // Revisions are append-only and their ids ascend with time, so an id
  // comparison is a chronological comparison — and it works across page
  // boundaries, which a row-index comparison would not.
  const olderDisabled = newid !== null && id >= newid;
  const newerDisabled = oldid !== null && id <= oldid;

  /** The diff that shows what THIS revision did. `from=0` is the creation. */
  const selfDiff = `/wiki/${slug}/diff?from=${parent ?? 0}&to=${id}`;

  return (
    <tr className="border-b border-rule-hair even:bg-panel/40">
      <td className="w-8 px-1 py-1.5 align-baseline">
        <input
          type="radio"
          name="oldid"
          value={id}
          checked={oldid === id}
          disabled={olderDisabled}
          onChange={() => onSelect("old", id)}
          aria-label={`Select the revision of ${when} as the older revision`}
          className="cursor-pointer accent-ink disabled:cursor-not-allowed disabled:opacity-40"
        />
      </td>
      <td className="w-8 px-1 py-1.5 align-baseline">
        <input
          type="radio"
          name="diff"
          value={id}
          checked={newid === id}
          disabled={newerDisabled}
          onChange={() => onSelect("new", id)}
          aria-label={`Select the revision of ${when} as the newer revision`}
          className="cursor-pointer accent-ink disabled:cursor-not-allowed disabled:opacity-40"
        />
      </td>

      <td className={cn(CELL, NOWRAP, "text-ink-2")}>
        {isLatest || latestId === null ? (
          <span className="text-ink-3">cur</span>
        ) : (
          <Link
            to={`/wiki/${slug}/diff?from=${id}&to=${latestId}`}
            title={`Compare the revision of ${when} with the current revision`}
            className="text-link hover:underline"
          >
            cur
          </Link>
        )}
        {" | "}
        {parent === null ? (
          <span className="text-ink-3">prev</span>
        ) : (
          <Link
            to={selfDiff}
            title={`Compare the revision of ${when} with the one before it`}
            className="text-link hover:underline"
          >
            prev
          </Link>
        )}
      </td>

      {/* The timestamp is the row's header: every other cell in the row is
          "the editor OF this revision", "the size OF this revision". */}
      <th scope="row" className={cn(CELL, NOWRAP, "text-left font-normal")}>
        <Link
          to={selfDiff}
          title="The changes this revision introduced"
          className="tabular-nums text-link hover:underline"
        >
          <time dateTime={created_at}>{when}</time>
        </Link>
      </th>

      <td className={cn(CELL, NOWRAP)}>
        {editor ? (
          <Link
            to={`/u/${editor.username}`}
            className="text-link hover:underline"
          >
            {editor.username}
          </Link>
        ) : (
          <span className="text-ink-3">anonymous</span>
        )}
      </td>

      <td className={cn(CELL, NOWRAP, "tabular-nums text-ink-2")}>
        {formatBytes(byte_size)}
      </td>

      <td className={cn(CELL, NOWRAP)}>
        <ByteDelta value={byte_delta} />
      </td>

      <td className={CELL}>
        <Flags revision={revision} />
        {comment ? (
          <span className="italic text-ink-2">{comment}</span>
        ) : (
          <span className="italic text-ink-3">No edit summary</span>
        )}
        {revision.tags.length > 0 && (
          <span className="ml-1.5 text-2xs text-ink-2">
            Tags: {revision.tags.join(", ")}
          </span>
        )}
      </td>
    </tr>
  );
}

/**
 * The single-letter edit flags.
 *
 * `<abbr title>` alone is not enough — title text is not announced by several
 * screen readers and is unreachable by touch — so each flag also carries a
 * visually-hidden expansion. That is the same reasoning as the Recent changes
 * legend, applied per flag.
 */
function Flags({ revision }: { revision: Revision }) {
  return (
    <>
      {revision.is_page_creation && (
        <Flag letter="N" label="new page" />
      )}
      {revision.is_minor && <Flag letter="m" label="minor edit" />}
    </>
  );
}

function Flag({ letter, label }: { letter: string; label: string }) {
  return (
    <>
      <abbr title={label[0].toUpperCase() + label.slice(1)} className="text-flag font-bold text-ink no-underline">
        <span aria-hidden="true">{letter}</span>
        <span className="sr-only">{label}</span>
      </abbr>{" "}
    </>
  );
}

/* ---------------------------------------------------------------------------
   The live-region sentence
   ------------------------------------------------------------------------- */

function describeRevision(
  revisions: Revision[],
  id: number | null,
): string | null {
  if (id === null) return null;
  const found = revisions.find((revision) => revision.id === id);
  return found
    ? `the revision of ${formatDateTime(found.created_at)}`
    : `revision ${id}`;
}

function selectionSentence(
  revisions: Revision[],
  oldid: number | null,
  newid: number | null,
  canCompare: boolean,
): string {
  const older = describeRevision(revisions, oldid);
  const newer = describeRevision(revisions, newid);

  if (canCompare) return `Ready to compare ${older} with ${newer}.`;
  if (older && !newer) return `${capitalise(older)} selected as the older side.`;
  if (newer && !older) return `${capitalise(newer)} selected as the newer side.`;
  return "Select an older and a newer revision to compare.";
}

function capitalise(value: string): string {
  return value[0].toUpperCase() + value.slice(1);
}
