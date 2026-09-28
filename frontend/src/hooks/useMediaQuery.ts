import { useEffect, useState } from "react";

/**
 * The two layout hinges, as media-query strings.
 *
 * They MUST stay numerically identical to `--breakpoint-shelf` and
 * `--breakpoint-tools` in `index.css`, because a handful of decisions cannot be
 * expressed in CSS alone: which of two mutually exclusive renderings of the
 * Tools rail to mount (a rail or a `<details>`), and whether the sticky
 * sub-header owns a table-of-contents toggle. Rendering both and hiding one
 * with `hidden` would duplicate every `id` inside it, which is an
 * accessibility defect, not a cosmetic one.
 *
 * 60rem / 82rem rather than px so a browser text-size preference moves the
 * hinge with the type, exactly as the CSS variant does.
 */
export const SHELF = "(min-width: 60rem)";
export const TOOLS = "(min-width: 82rem)";
export const REDUCED_MOTION = "(prefers-reduced-motion: reduce)";

/**
 * Subscribe to a media query.
 *
 * The initial value is read synchronously in the `useState` initialiser, so the
 * first paint is already correct and no layout flashes between the two
 * renderings.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => {
    if (typeof window === "undefined" || !window.matchMedia) return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mql = window.matchMedia(query);
    // Re-read: `query` may have changed since the initialiser ran.
    setMatches(mql.matches);
    const onChange = (event: MediaQueryListEvent) => setMatches(event.matches);
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, [query]);

  return matches;
}

/** True at `shelf` and above: the left rail is a real column. */
export function useIsShelf(): boolean {
  return useMediaQuery(SHELF);
}

/** True at `tools` and above: the right rail is a real column. */
export function useIsTools(): boolean {
  return useMediaQuery(TOOLS);
}

/**
 * Reactive `prefers-reduced-motion`. The global CSS block in `index.css` §5
 * already collapses every transition and animation; this is for the handful of
 * behaviours JavaScript owns, such as the scroll behaviour of a footnote jump.
 */
export function usePrefersReducedMotion(): boolean {
  return useMediaQuery(REDUCED_MOTION);
}
