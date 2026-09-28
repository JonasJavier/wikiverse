import { Link } from "react-router-dom";

import type { Author, ChangeRow as ChangeRowData } from "@/lib/types";
import {
  byteDeltaTone,
  changeRowKey,
  cn,
  EM_DASH,
  formatByteDelta,
  formatBytes,
  formatDate,
  formatDateTime,
  formatTime,
} from "@/lib/utils";

/**
 * ONE ROW, THREE FEEDS.
 *
 * Recent changes, the watchlist and contributions all render this component,
 * because `ChangeRowSerializer` gives all three the same shape (DECISIONS
 * §4). That reuse is the reason `byte_delta` is denormalised server-side
 * rather than computed per feed.
 *
 * Two nullability facts drive the whole markup and both come from the
 * serializer, not from taste:
 *
 *   - `byte_size` and `byte_delta` are **null on a talk row**. A talk post
 *     has no article byte count, so the cell is an em dash in `--delta-null`
 *     and never a misleading `0`.
 *   - `thread` is **null on an edit row**, and on a talk row `comment` is a
 *     copy of the thread title. So a talk row prints the thread once, as a
 *     link into the discussion, and an edit row prints the edit summary.
 *
 * Every flag is an `<abbr title>` AND is explained by `<ChangeLegend>`,
 * because a bare single letter is not an accessible affordance. Every signed
 * delta prints its sign explicitly, so colour is never the only channel
 * carrying the meaning (WCAG 1.4.1).
 *
 * `(talk | contribs)` from design-ui §4.12 is deliberately absent: this wiki
 * has no user-talk namespace, and `/u/{username}` IS the contributions page,
 * so both halves would be either dead or a duplicate of the name beside them.
 */

export interface ChangeRowProps {
  row: ChangeRowData;
  /**
   * Mark a row that is still its article's latest revision. On by default on
   * a contributions list, where "is this edit still standing?" is the
   * question the reader actually has.
   */
  showCurrent?: boolean;
  className?: string;
}

export function ChangeRow({ row, showCurrent = true, className }: ChangeRowProps) {
  const tone = byteDeltaTone(row.byte_delta);

  return (
    <li
      className={cn(
        "flex flex-wrap items-baseline gap-x-1.5 gap-y-0.5 py-2.5 text-ui",
        className,
      )}
    >
      {/* Leading actions. An edit has a diff and a history; a talk post has
          neither, so it links into the discussion instead of offering a diff
          that cannot exist. */}
      <span className="text-ink-2">
        {row.kind === "edit" ? (
          <>
            <Link
              to={`/wiki/${row.article.slug}/diff?from=${row.parent_id ?? 0}&to=${row.id}`}
              className="text-link hover:underline"
            >
              diff
            </Link>
            {" | "}
            <Link
              to={`/wiki/${row.article.slug}/history`}
              className="text-link hover:underline"
            >
              hist
            </Link>
          </>
        ) : (
          <Link
            to={`/wiki/${row.article.slug}/talk#c-${row.id}`}
            className="text-link hover:underline"
          >
            talk
          </Link>
        )}
      </span>

      <Flags row={row} showCurrent={showCurrent} />

      <Link
        to={`/wiki/${row.article.slug}`}
        className="font-medium text-link hover:underline"
      >
        {row.article.title}
      </Link>

      <time
        dateTime={row.timestamp}
        title={formatDateTime(row.timestamp)}
        className="tabular-nums text-ink-2"
      >
        {formatTime(row.timestamp)}
      </time>

      {/* The byte cell. `title` carries the absolute size, which is the
          figure a reader comparing two revisions needs and which does not
          fit on the row. */}
      <span
        title={row.byte_size === null ? undefined : formatBytes(row.byte_size)}
        className={cn(
          "tabular-nums",
          tone === "positive" && "text-delta-pos",
          tone === "negative" && "text-delta-neg",
          tone === "null" && "text-delta-null",
          row.byte_delta !== null &&
            Math.abs(row.byte_delta) >= 500 &&
            "font-semibold",
        )}
      >
        {formatByteDelta(row.byte_delta)}
      </span>

      <UserLink user={row.user} />

      {row.kind === "talk" && row.thread ? (
        <span className="text-ink-2">
          {"in "}
          <Link
            to={`/wiki/${row.article.slug}/talk#thread-${row.thread.id}`}
            className="text-link italic hover:underline"
          >
            {row.thread.title}
          </Link>
        </span>
      ) : (
        row.comment && (
          <span className="text-ink-2 italic">({row.comment})</span>
        )
      )}

      {row.tags.length > 0 && (
        <span className="text-2xs text-ink-3">
          Tags: {row.tags.join(", ")}
        </span>
      )}
    </li>
  );
}

/* ---------------------------------------------------------------------
   Flags
   --------------------------------------------------------------------- */

const FLAG =
  "inline-block min-w-3.5 text-center align-baseline text-flag font-semibold " +
  "no-underline decoration-dotted";

function Flags({
  row,
  showCurrent,
}: {
  row: ChangeRowData;
  showCurrent: boolean;
}) {
  const flags: { key: string; letter: string; title: string; className?: string }[] = [];

  if (row.is_page_creation) {
    flags.push({
      key: "new",
      letter: "N",
      title: row.kind === "talk" ? "new discussion topic" : "new page",
      className: "text-ok",
    });
  }
  if (row.is_minor) {
    flags.push({ key: "minor", letter: "m", title: "minor edit" });
  }
  if (row.is_bot) {
    flags.push({ key: "bot", letter: "b", title: "bot edit" });
  }

  if (flags.length === 0 && !(showCurrent && row.is_current)) return null;

  return (
    <span className="flex items-baseline gap-1">
      {flags.map((flag) => (
        <abbr
          key={flag.key}
          title={flag.title}
          className={cn(FLAG, "text-ink-2", flag.className)}
        >
          {flag.letter}
        </abbr>
      ))}
      {showCurrent && row.is_current && (
        <abbr
          title="this is still the article's latest revision"
          className="text-2xs font-medium text-ink-2 no-underline"
        >
          current
        </abbr>
      )}
    </span>
  );
}

function UserLink({ user }: { user: Author | null }) {
  if (!user) {
    return <span className="text-ink-2 italic">(account removed)</span>;
  }
  return (
    <Link to={`/u/${user.username}`} className="text-link hover:underline">
      {user.username}
    </Link>
  );
}

/* ---------------------------------------------------------------------
   Legend
   --------------------------------------------------------------------- */

/**
 * The legend is what makes the single-letter flags accessible, so it is
 * rendered once above every feed and is not optional decoration.
 */
export function ChangeLegend({ className }: { className?: string }) {
  return (
    <p className={cn("text-2xs text-ink-2", className)}>
      <span className="font-semibold text-ok">N</span> new page or topic
      {" · "}
      <span className="font-semibold">m</span> minor edit
      {" · "}
      <span className="font-semibold">b</span> bot edit
      {" · "}
      <span className="font-semibold">current</span> still the latest revision
      {" · "}
      <span className="tabular-nums">(±123)</span> change in bytes
      {" · "}
      <span className="tabular-nums">{EM_DASH}</span> a talk post, which has no
      byte count and no diff
    </p>
  );
}

/* ---------------------------------------------------------------------
   Day grouping
   --------------------------------------------------------------------- */

export interface ChangeDayGroupsProps {
  rows: ChangeRowData[];
  /**
   * `2` on Recent changes and the watchlist, where the page's `h1` is
   * directly above. `3` inside a profile, where an `h2` already names the
   * section — heading order is a gate, not a preference.
   */
  headingLevel?: 2 | 3;
  showCurrent?: boolean;
  className?: string;
}

/**
 * Newest first, grouped under a serif day heading — the shape Wikipedia's
 * Special:RecentChanges has had for twenty years, and the reason a feed of
 * 200 rows stays navigable.
 *
 * The React key is `` `${kind}-${id}` `` (via `changeRowKey`), because `id`
 * is unique only within a kind: an edit row's id is a Revision id and a talk
 * row's is a TalkMessage id, so the two collide roughly as often as you would
 * expect from two independent sequences.
 */
export function ChangeDayGroups({
  rows,
  headingLevel = 2,
  showCurrent = true,
  className,
}: ChangeDayGroupsProps) {
  const groups = groupByDay(rows);
  const Heading = headingLevel === 2 ? "h2" : "h3";

  return (
    <div className={className}>
      {groups.map((group) => (
        <section key={group.key}>
          <Heading className="mt-6 border-b border-rule pb-1 font-serif text-h2 font-normal text-ink first:mt-0">
            {group.label}
          </Heading>
          <ul className="divide-y divide-rule-hair">
            {group.rows.map((row) => (
              <ChangeRow
                key={changeRowKey(row)}
                row={row}
                showCurrent={showCurrent}
              />
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

interface DayGroup {
  key: string;
  label: string;
  rows: ChangeRowData[];
}

/**
 * Grouped on the reader's LOCAL day, which is what `formatDate` prints. Using
 * the ISO string's own date would put a 00:30 edit under yesterday's heading
 * for anybody west of UTC, and the heading would then disagree with the
 * timestamp on the row beneath it.
 */
function groupByDay(rows: ChangeRowData[]): DayGroup[] {
  const groups: DayGroup[] = [];

  for (const row of rows) {
    const date = new Date(row.timestamp);
    const key = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    const last = groups.at(-1);

    if (last && last.key === key) {
      last.rows.push(row);
    } else {
      groups.push({ key, label: formatDate(row.timestamp), rows: [row] });
    }
  }

  return groups;
}
