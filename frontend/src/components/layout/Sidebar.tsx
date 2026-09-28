import { type ReactNode, useCallback, useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";

/* ---------------------------------------------------------------------------
   Rail primitives. Exported because the Tools rail, the table of contents and
   anything else that lives in a rail must be the same 14px object — Wikipedia's
   measured rail size, and small enough that a rail full of links reads as
   apparatus rather than as a second navigation bar.
   ------------------------------------------------------------------------- */

/**
 * A labelled group of rail links, separated from its neighbour by a hairline.
 *
 * The label is a real `<h2>`/`<h3>` when `labelledBy` is not used elsewhere: a
 * rail whose groups are unlabelled `<div>`s gives a screen reader a flat list of
 * twelve links with no structure.
 */
export function RailGroup({
  label,
  children,
  className,
}: {
  label?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("border-b border-rule-hair py-3 last:border-0", className)}>
      {label && (
        <h3 className="mb-1 px-2 text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
          {label}
        </h3>
      )}
      <ul className="list-none">{children}</ul>
    </div>
  );
}

const RAIL_ITEM =
  "block rounded-chrome px-2 py-1 transition-colors duration-100 motion-reduce:transition-none";

/**
 * `aria-current="page"` comes from `NavLink`, which computes it from the router
 * rather than from a hand-maintained prop — the active state therefore cannot
 * desync from the URL.
 *
 * `end` defaults to true only for `/`, because `NavLink` otherwise marks the main
 * page active on every route in the site.
 */
export function RailLink({
  to,
  children,
  end,
}: {
  to: string;
  children: ReactNode;
  end?: boolean;
}) {
  return (
    <li>
      <NavLink
        to={to}
        end={end ?? to === "/"}
        className={({ isActive }) =>
          cn(
            RAIL_ITEM,
            isActive
              ? "bg-panel font-semibold text-ink"
              : "text-link hover:bg-panel hover:text-link-hover",
          )
        }
      >
        {children}
      </NavLink>
    </li>
  );
}

/** A rail entry that performs an action rather than navigating. */
export function RailButton({
  onClick,
  children,
}: {
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <li>
      <button
        type="button"
        onClick={onClick}
        className={cn(RAIL_ITEM, "w-full text-left text-link hover:bg-panel hover:text-link-hover")}
      >
        {children}
      </button>
    </li>
  );
}

/* ---------------------------------------------------------------------------
   The site navigation rail.
   ------------------------------------------------------------------------- */

const RAIL_PIN_KEY = "wikiverse.rail.nav";

function readPinned(): boolean {
  try {
    return localStorage.getItem(RAIL_PIN_KEY) !== "hidden";
  } catch {
    // Blocked storage: show the rail. A collapsed rail is the worse default.
    return true;
  }
}

/**
 * Site navigation, in the left rail.
 *
 * Pinnable, like Vector's: the `Hide` / `Show` toggle is persisted under
 * `wikiverse.rail.nav`. Fifteen lines, and one of the details that reads as a
 * real wiki rather than as a sidebar someone drew.
 *
 * `Watchlist` and `My contributions` appear only when signed in — a rail link to
 * a protected route that bounces the reader to `/login` is worse than no link.
 */
export function Sidebar({ className }: { className?: string }) {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [shown, setShown] = useState(readPinned);

  useEffect(() => {
    try {
      localStorage.setItem(RAIL_PIN_KEY, shown ? "shown" : "hidden");
    } catch {
      /* Blocked storage is not an error worth surfacing for a rail preference. */
    }
  }, [shown]);

  return (
    <nav aria-label="Site" className={cn("text-ui", className)}>
      <div className="flex items-baseline justify-between border-b border-rule-hair pb-1">
        <h2 className="px-2 text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
          Wikiverse
        </h2>
        <button
          type="button"
          onClick={() => setShown((value) => !value)}
          aria-expanded={shown}
          aria-controls="site-rail-groups"
          className="rounded-chrome px-1 text-2xs text-link hover:underline"
        >
          {shown ? "hide" : "show"}
        </button>
      </div>

      {shown && (
        <div id="site-rail-groups">
          <RailGroup label="Navigation">
            <RailLink to="/">Main page</RailLink>
            <RailLink to="/browse">Browse</RailLink>
            <RailLink to="/categories">Categories</RailLink>
            {/* DECISIONS §4 fixes this route as `/changes`; design-ui §3.8's
                `/recent-changes` is superseded. */}
            <RailLink to="/changes">Recent changes</RailLink>
            <RailLink to="/random">Random article</RailLink>
          </RailGroup>

          <RailGroup label="Contribute">
            <RailLink to="/new">Create an article</RailLink>
            {isAuthenticated && <RailLink to="/watchlist">Watchlist</RailLink>}
            {isAuthenticated && user && (
              <RailLink to={`/u/${user.username}`}>My contributions</RailLink>
            )}
            <RailLink to="/about">About</RailLink>
          </RailGroup>
        </div>
      )}
    </nav>
  );
}

/**
 * The same navigation, rendered flat for the masthead disclosure below `shelf`.
 *
 * A separate export rather than a prop on `Sidebar`, because the two are never
 * mounted at the same time and the disclosure has no pin toggle, no group
 * headings and no hairlines — collapsing them into one component would mean a
 * `variant` prop threaded through every line.
 */
export function SidebarLinks({ onNavigate }: { onNavigate?: () => void }) {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const close = useCallback(() => onNavigate?.(), [onNavigate]);

  const item = ({ isActive }: { isActive: boolean }) =>
    cn(
      "block rounded-chrome px-2 py-2 text-ui",
      isActive
        ? "bg-panel font-semibold text-ink"
        : "text-link hover:bg-panel hover:text-link-hover",
    );

  return (
    <ul className="list-none">
      {[
        { to: "/", label: "Main page", end: true },
        { to: "/browse", label: "Browse" },
        { to: "/categories", label: "Categories" },
        { to: "/changes", label: "Recent changes" },
        { to: "/random", label: "Random article" },
        { to: "/new", label: "Create an article" },
        ...(isAuthenticated ? [{ to: "/watchlist", label: "Watchlist" }] : []),
        ...(isAuthenticated && user
          ? [{ to: `/u/${user.username}`, label: "My contributions" }]
          : []),
        { to: "/about", label: "About" },
      ].map((link) => (
        <li key={link.to}>
          <NavLink to={link.to} end={link.end} onClick={close} className={item}>
            {link.label}
          </NavLink>
        </li>
      ))}
    </ul>
  );
}
