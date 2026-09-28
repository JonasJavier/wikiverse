import { create } from "zustand";
import { persist } from "zustand/middleware";

/**
 * Three states, not two.
 *
 * The bug this file exists to fix (`survey-frontend.md` §4.9): the old store
 * evaluated `systemTheme()` once, at module load, wrote the answer into
 * persisted state, and never listened to the media query again. Two
 * consequences, both real:
 *
 *   1. Changing the OS appearance did nothing for the lifetime of the stored
 *      value — and `persist` makes that lifetime "forever".
 *   2. The type had no `"system"` member, so the first click on the theme
 *      toggle permanently opted the reader out of following their OS with no
 *      way back.
 *
 * `"system"` is therefore a first-class, and the DEFAULT, choice. Only an
 * explicit choice is persisted; `resolved` is derived and never stored.
 */
export type ThemeChoice = "light" | "dark" | "system";
export type ResolvedTheme = "light" | "dark";

export const THEME_STORAGE_KEY = "wikiverse.theme";

const DARK_QUERY = "(prefers-color-scheme: dark)";

function prefersDark(): boolean {
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia(DARK_QUERY).matches;
}

function resolve(choice: ThemeChoice): ResolvedTheme {
  if (choice === "system") return prefersDark() ? "dark" : "light";
  return choice;
}

interface ThemeState {
  /** What the reader asked for. Persisted. */
  choice: ThemeChoice;
  /**
   * What is actually painted. Derived from `choice` plus the OS, never
   * persisted, and kept current by a `matchMedia` listener.
   *
   * Retains the name `theme` because that is what call sites read.
   */
  theme: ResolvedTheme;
  setChoice: (choice: ThemeChoice) => void;
  /** light → dark → system → light. */
  cycle: () => void;
  /** Kept for the two-state call sites: writes an explicit light/dark choice. */
  setTheme: (theme: ResolvedTheme) => void;
  toggle: () => void;
  /** Called by the `matchMedia` listener; only moves `theme`. */
  syncSystem: () => void;
}

const ORDER: ThemeChoice[] = ["light", "dark", "system"];

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      choice: "system",
      theme: resolve("system"),
      setChoice: (choice) => set({ choice, theme: resolve(choice) }),
      cycle: () => {
        const next = ORDER[(ORDER.indexOf(get().choice) + 1) % ORDER.length];
        set({ choice: next, theme: resolve(next) });
      },
      setTheme: (theme) => set({ choice: theme, theme }),
      toggle: () => {
        const next: ResolvedTheme = get().theme === "dark" ? "light" : "dark";
        set({ choice: next, theme: next });
      },
      syncSystem: () => {
        if (get().choice !== "system") return;
        const next = resolve("system");
        if (next !== get().theme) set({ theme: next });
      },
    }),
    {
      name: THEME_STORAGE_KEY,
      /**
       * `theme` is derived. Persisting it is what let a stale OS answer outlive
       * the OS setting that produced it.
       */
      partialize: (state) => ({ choice: state.choice }),
      /**
       * `merge` rather than `onRehydrateStorage`, deliberately: it runs BEFORE
       * the rehydrated state is committed, so `theme` is recomputed from the
       * restored `choice` in the same `set`. Recomputing it afterwards leaves
       * one render in which `choice` is the reader's and `theme` is still the
       * initial-state guess — i.e. a flash of the wrong theme.
       *
       * It also absorbs the v1 payload, which was `{ theme: "light" | "dark" }`
       * with no `choice` at all. That is read as an explicit choice rather than
       * thrown away.
       */
      merge: (persisted, current) => {
        const stored = persisted as
          | { choice?: ThemeChoice; theme?: string }
          | undefined;
        const choice: ThemeChoice =
          stored?.choice ??
          (stored?.theme === "light" || stored?.theme === "dark"
            ? stored.theme
            : current.choice);
        return { ...current, choice, theme: resolve(choice) };
      },
    },
  ),
);

/** Apply a resolved theme to `<html>`. The `.dark` class drives every token. */
export function applyTheme(theme: ResolvedTheme): void {
  if (typeof document === "undefined") return;
  const root = document.documentElement;
  root.classList.toggle("dark", theme === "dark");
  // Makes form controls, scrollbars and the caret follow the theme even where
  // our own CSS does not reach.
  root.style.colorScheme = theme;
}

/**
 * Wire the OS listener and paint the initial theme.
 *
 * Called at module scope below rather than from a React effect. `main.tsx`
 * imports the app before rendering it, so the `.dark` class is on `<html>`
 * before React's first commit — which removes the full-viewport white flash
 * that `survey-frontend.md` §4.9 measured on every cold load in dark mode.
 *
 * The earlier *parse-to-script* flash is removed by `public/theme-init.js`, a
 * blocking same-origin script in `index.html` (an inline one would violate
 * `script-src 'self'`, DECISIONS §7.3). It reads the same storage key and must
 * stay in step with `resolve()` above.
 */
function bootstrapTheme(): void {
  if (typeof window === "undefined") return;

  applyTheme(useThemeStore.getState().theme);

  // The OS listener — the whole point of this rewrite. It is attached
  // unconditionally and `syncSystem` decides whether to act, so toggling
  // away from and back to "system" needs no subscription bookkeeping.
  window.matchMedia?.(DARK_QUERY).addEventListener("change", () => {
    useThemeStore.getState().syncSystem();
  });

  // Repaint on every change to the resolved theme, including changes made in
  // another tab via the `persist` storage sync.
  useThemeStore.subscribe((state, previous) => {
    if (state.theme !== previous.theme) applyTheme(state.theme);
  });
}

bootstrapTheme();
