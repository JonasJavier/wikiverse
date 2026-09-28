import { Search } from "lucide-react";
import {
  type FormEvent,
  type KeyboardEvent,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { MIN_SUGGEST_LENGTH, useSuggest } from "@/api/search";
import type { Suggestion } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Long enough to skip the intermediate keystrokes of a typed word. */
const DEBOUNCE_MS = 150;

function useDebounced<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = window.setTimeout(() => setDebounced(value), delay);
    return () => window.clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

interface TypeaheadSearchProps {
  className?: string;
  /** Called after any navigation the box causes — closes the mobile panel. */
  onNavigate?: () => void;
}

/**
 * The masthead search: a WAI-ARIA 1.2 combobox over `GET /api/search/suggest/`.
 *
 * Arrow keys move through the titles, Enter opens the highlighted article (or
 * runs a full search when nothing is highlighted), Escape closes the list and
 * then clears the box. The last row is always "Search for pages containing …",
 * so the full results page is one key away even when a title matches.
 *
 * The list is rendered only while it has something to show; `aria-expanded`
 * tracks that exactly, which is what a screen reader announces.
 */
export function TypeaheadSearch({ className, onNavigate }: TypeaheadSearchProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const listId = useId();
  const rootRef = useRef<HTMLFormElement>(null);

  const [value, setValue] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);

  const term = useDebounced(value.trim(), DEBOUNCE_MS);
  const { data } = useSuggest(term, { enabled: open });
  const suggestions: Suggestion[] = term.length >= MIN_SUGGEST_LENGTH ? (data ?? []) : [];
  const query = value.trim();
  // One extra option: the full-text search row.
  const optionCount = query ? suggestions.length + 1 : 0;
  const expanded = open && optionCount > 0;

  // A route change means the reader went somewhere: the list must not follow them.
  useEffect(() => {
    setOpen(false);
    setActive(-1);
  }, [location.pathname]);

  useEffect(() => {
    function onPointerDown(event: PointerEvent) {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, []);

  function finish(to: string) {
    setOpen(false);
    setActive(-1);
    setValue("");
    navigate(to);
    onNavigate?.();
  }

  function searchFor(q: string) {
    finish(`/search?q=${encodeURIComponent(q)}`);
  }

  function choose(index: number) {
    if (index >= 0 && index < suggestions.length) {
      finish(`/wiki/${suggestions[index].slug}`);
    } else if (query) {
      searchFor(query);
    }
  }

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (active >= 0) choose(active);
    else if (query) searchFor(query);
  }

  function onKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (!open) setOpen(true);
      if (optionCount > 0) setActive((i) => (i + 1) % optionCount);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      if (optionCount > 0) setActive((i) => (i <= 0 ? optionCount - 1 : i - 1));
    } else if (event.key === "Escape") {
      if (expanded) {
        event.preventDefault();
        setOpen(false);
        setActive(-1);
      } else if (value) {
        event.preventDefault();
        setValue("");
      }
    }
  }

  const optionId = (index: number) => `${listId}-opt-${index}`;

  return (
    <form
      ref={rootRef}
      role="search"
      onSubmit={onSubmit}
      className={cn("relative", className)}
    >
      <label htmlFor={`${listId}-input`} className="sr-only">
        Search Wikiverse
      </label>
      <Search
        className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-ink-3"
        aria-hidden="true"
      />
      <input
        id={`${listId}-input`}
        type="search"
        role="combobox"
        autoComplete="off"
        spellCheck={false}
        aria-expanded={expanded}
        aria-controls={listId}
        aria-autocomplete="list"
        aria-activedescendant={expanded && active >= 0 ? optionId(active) : undefined}
        value={value}
        placeholder="Search Wikiverse"
        onChange={(event) => {
          setValue(event.target.value);
          setOpen(true);
          setActive(-1);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
        className={cn(
          "h-9 w-full rounded-chrome border border-rule bg-page pr-3 pl-8 text-ui text-ink",
          "placeholder:text-ink-3 focus:border-focus focus:outline-none",
          "[&::-webkit-search-cancel-button]:hidden",
        )}
      />

      {expanded && (
        <ul
          id={listId}
          role="listbox"
          aria-label="Search suggestions"
          className="absolute inset-x-0 top-full z-50 mt-1 overflow-hidden rounded-chrome border border-rule bg-page py-1 shadow-[var(--shadow-dialog)]"
        >
          {suggestions.map((item, index) => (
            <li
              key={item.slug}
              id={optionId(index)}
              role="option"
              aria-selected={active === index}
              onPointerDown={(event) => event.preventDefault()}
              onClick={() => choose(index)}
              onPointerEnter={() => setActive(index)}
              className={cn(
                "cursor-pointer px-3 py-1.5",
                active === index && "bg-panel",
              )}
            >
              <span className="block truncate text-ui font-medium text-ink">
                {item.title}
              </span>
              {item.short_description && (
                <span className="block truncate text-2xs text-ink-2">
                  {item.short_description}
                </span>
              )}
            </li>
          ))}
          <li
            id={optionId(suggestions.length)}
            role="option"
            aria-selected={active === suggestions.length}
            onPointerDown={(event) => event.preventDefault()}
            onClick={() => choose(suggestions.length)}
            onPointerEnter={() => setActive(suggestions.length)}
            className={cn(
              "flex cursor-pointer items-center gap-2 border-t border-rule-hair px-3 py-2 text-ui text-link",
              suggestions.length === 0 && "border-t-0",
              active === suggestions.length && "bg-panel",
            )}
          >
            <Search className="size-3.5 shrink-0" aria-hidden="true" />
            <span className="truncate">
              Search for pages containing <b className="font-semibold">{query}</b>
            </span>
          </li>
        </ul>
      )}
    </form>
  );
}
