import { RotateCw, Rss } from "lucide-react";
import type { FormEvent, ReactNode } from "react";
import { Link, useSearchParams } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { Input, Label } from "@/components/ui/Field";
import {
  CHANGE_DAY_OPTIONS,
  CHANGE_LIMIT_OPTIONS,
  CHANGES_FEED_URL,
  type ChangeFilterState,
  readChangeFilters,
  writeChangeFilters,
} from "@/api/community";
import type { ChangeTypeFilter } from "@/lib/types";
import { cn, formatDateTime } from "@/lib/utils";

/**
 * THE URL IS THE FILTER STATE. There is no `useState` in this component for
 * anything a reader can see.
 *
 * DECISIONS §4 fixes the vocabulary — `type`, `user`, `category`,
 * `hideMinor=1`, `hideBot=1`, `days=N`, `limit` — and `api/community.ts`
 * owns the translation into API parameters. Consequences that follow for
 * free, and that a `useState` version cannot have: a shareable view, a
 * working back button, functioning scroll restoration, and a crawlable
 * `?days=30`.
 *
 * Every choice is therefore a `<Link>`, not a button with an `onClick`: a
 * filter is a different address, and the browser already knows how to
 * navigate to, remember and bookmark an address. The two free-text fields are
 * the exception, because a keystroke is not a navigation; they submit.
 *
 * Nothing here polls. design-ui §5.10: "an encyclopedia's changes feed that
 * moves under the cursor is hostile." There is a Refresh button and a
 * `Last updated` line instead.
 */

export interface ChangeFiltersProps {
  /**
   * `"changes"` shows everything. `"watchlist"` drops `type` and `limit`,
   * because the watchlist queryset is revisions only (so `type=talk` would
   * have nothing to return) and its page size is fixed at 50 by DECISIONS
   * §10.
   */
  variant?: "changes" | "watchlist";
  /** Explicit refetch. Wired to the feed query's `refetch`. */
  onRefresh?: () => void;
  /** `dataUpdatedAt` from the feed query, for the `Last updated` line. */
  updatedAt?: number;
  busy?: boolean;
  /** Recent changes offers the RSS feed (DECISIONS §14); the watchlist cannot. */
  showFeedLink?: boolean;
  className?: string;
}

export function ChangeFilters({
  variant = "changes",
  onRefresh,
  updatedAt,
  busy = false,
  showFeedLink = false,
  className,
}: ChangeFiltersProps) {
  const [search, setSearch] = useSearchParams();
  const state = readChangeFilters(search);
  const full = variant === "changes";

  /**
   * Every choice is an address. An all-defaults view gets an EMPTY search
   * rather than a bare `"?"`, so the canonical Recent-changes URL is `/changes`
   * and not `/changes?`.
   */
  const to = (patch: Partial<ChangeFilterState>) => {
    const query = writeChangeFilters(state, patch).toString();
    return { search: query ? `?${query}` : "" };
  };

  function apply(patch: Partial<ChangeFilterState>): void {
    setSearch(writeChangeFilters(state, patch));
  }

  function onSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    apply({
      user: String(data.get("user") ?? "").trim(),
      category: String(data.get("category") ?? "").trim(),
    });
  }

  const isFiltered =
    state.type !== "all" ||
    Boolean(state.user) ||
    Boolean(state.category) ||
    state.hideMinor ||
    state.hideBot ||
    state.days !== 7 ||
    state.limit !== 50;

  return (
    <form
      // Remounting on a URL change is what keeps the two uncontrolled text
      // fields honest across the back button: their `defaultValue` is read
      // once, so without the key a reader who navigated back would see the
      // previous query in a box that no longer filters anything.
      key={`${state.user}\u0000${state.category}`}
      onSubmit={onSubmit}
      aria-label="Filter changes"
      className={cn(
        "rounded-chrome border border-rule-hair bg-panel px-3 py-2.5",
        className,
      )}
    >
      <div className="flex flex-wrap items-center gap-x-5 gap-y-2">
        {full && (
          <Segmented label="Show">
            <Segment active={state.type === "all"} to={to({ type: "all" })}>
              All
            </Segment>
            {(["edit", "talk"] as ChangeTypeFilter[]).map((kind) => (
              <Segment
                key={kind}
                active={state.type === kind}
                to={to({ type: kind })}
              >
                {kind === "edit" ? "Edits" : "Talk"}
              </Segment>
            ))}
          </Segmented>
        )}

        <Segmented label="Period">
          {CHANGE_DAY_OPTIONS.map((days) => (
            <Segment
              key={days}
              active={state.days === days}
              to={to({ days })}
              title={`Changes in the last ${days === 1 ? "day" : `${days} days`}`}
            >
              {days === 1 ? "1 day" : `${days} days`}
            </Segment>
          ))}
        </Segmented>

        {full && (
          <Segmented label="Rows">
            {CHANGE_LIMIT_OPTIONS.map((limit) => (
              <Segment
                key={limit}
                active={state.limit === limit}
                to={to({ limit })}
              >
                {limit}
              </Segment>
            ))}
          </Segmented>
        )}

        <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
          <Toggle
            checked={state.hideMinor}
            onChange={(hideMinor) => apply({ hideMinor })}
          >
            Hide minor edits
          </Toggle>
          <Toggle
            checked={state.hideBot}
            onChange={(hideBot) => apply({ hideBot })}
          >
            Hide bot edits
          </Toggle>
        </div>
      </div>

      {full && (
        <div className="mt-2.5 flex flex-wrap items-end gap-x-3 gap-y-2 border-t border-rule-hair pt-2.5">
          <div className="w-44">
            <Label htmlFor="rc-user">Contributor</Label>
            <Input
              id="rc-user"
              name="user"
              defaultValue={state.user}
              autoComplete="off"
              spellCheck={false}
              placeholder="username"
              className="h-8 py-0"
            />
          </div>
          <div className="w-44">
            <Label htmlFor="rc-category">Category</Label>
            <Input
              id="rc-category"
              name="category"
              defaultValue={state.category}
              autoComplete="off"
              spellCheck={false}
              placeholder="category slug"
              className="h-8 py-0"
            />
          </div>
          <Button type="submit" variant="secondary" size="md">
            Apply
          </Button>
          {isFiltered && (
            <Link to={{ search: "" }} className="text-ui text-link hover:underline">
              Reset filters
            </Link>
          )}
        </div>
      )}

      <div className="mt-2.5 flex flex-wrap items-center justify-between gap-x-4 gap-y-1 border-t border-rule-hair pt-2.5 text-2xs text-ink-2">
        <span aria-live="polite">
          {updatedAt ? (
            <>
              Last updated{" "}
              <time dateTime={new Date(updatedAt).toISOString()} className="tabular-nums">
                {formatDateTime(new Date(updatedAt).toISOString())}
              </time>
            </>
          ) : (
            "Not loaded yet"
          )}
        </span>
        <span className="flex items-center gap-3">
          {showFeedLink && (
            <a
              href={CHANGES_FEED_URL}
              className="inline-flex items-center gap-1 text-link hover:underline"
            >
              <Rss aria-hidden="true" className="size-3" />
              RSS
            </a>
          )}
          {onRefresh && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onRefresh}
              disabled={busy}
              className="text-2xs"
            >
              <RotateCw
                aria-hidden="true"
                className={cn("size-3", busy && "motion-safe:animate-spin")}
              />
              Refresh
            </Button>
          )}
        </span>
      </div>
    </form>
  );
}

/* ---------------------------------------------------------------------
   Controls
   --------------------------------------------------------------------- */

function Segmented({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-2xs tracking-[0.04em] text-ink-2 uppercase">
        {label}
      </span>
      <div
        role="group"
        aria-label={label}
        className="inline-flex divide-x divide-rule-hair overflow-hidden rounded-chrome border border-rule"
      >
        {children}
      </div>
    </div>
  );
}

const SEGMENT = "px-2 py-1 text-ui whitespace-nowrap tabular-nums";

function Segment({
  active,
  to,
  title,
  children,
}: {
  active: boolean;
  to: { search: string };
  title?: string;
  children: ReactNode;
}) {
  if (active) {
    /* A link to the view you are already looking at is a dead end for a
       screen-reader user, so the active segment is a span. */
    return (
      <span
        aria-current="true"
        title={title}
        className={cn(SEGMENT, "bg-inset font-semibold text-ink")}
      >
        {children}
      </span>
    );
  }
  return (
    <Link
      to={to}
      title={title}
      className={cn(SEGMENT, "bg-page text-link hover:bg-inset")}
    >
      {children}
    </Link>
  );
}

function Toggle({
  checked,
  onChange,
  children,
}: {
  checked: boolean;
  onChange: (next: boolean) => void;
  children: ReactNode;
}) {
  return (
    <label className="flex items-center gap-1.5 text-ui text-ink">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="size-3.5 shrink-0 accent-[var(--ink-1)]"
      />
      {children}
    </label>
  );
}
