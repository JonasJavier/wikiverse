import { create } from "zustand";
import { persist } from "zustand/middleware";

import { tokens } from "@/lib/tokens";
import type { AuthTokens, User } from "@/lib/types";

/**
 * `isAuthenticated` is DERIVED FROM THE TOKENS, and is never persisted.
 *
 * The bug this file exists to fix (`survey-frontend.md` §4.10): the old store
 * persisted `{ user, isAuthenticated }` under `wikiverse.auth` while the tokens
 * themselves lived under `wikiverse.access` / `wikiverse.refresh`, and nothing
 * kept the two in sync. Every read of a token bypassed the store entirely. So:
 *
 *   - Clearing site data for the token keys, or a token expiring out of
 *     storage, left the app rendering the avatar menu and admitting the reader
 *     to `/new` with no credentials at all.
 *   - Logging out in one tab left every other tab believing it was signed in,
 *     because there was no `storage` listener.
 *
 * Both are closed here: `isAuthenticated` is recomputed from storage on every
 * mutation and on every cross-tab `storage` event, and only `user` is persisted.
 *
 * A present refresh token counts as a session even when the access token is
 * gone: that is exactly the state the single-flight refresh in `lib/api.ts`
 * recovers from.
 */
function hasSession(): boolean {
  try {
    return Boolean(tokens.access() ?? tokens.refresh());
  } catch {
    // Private mode, blocked storage: treat as signed out rather than throwing
    // out of a store initialiser.
    return false;
  }
}

interface AuthState {
  user: User | null;
  /** Derived from localStorage. NOT persisted — see the note above. */
  isAuthenticated: boolean;
  setSession: (data: AuthTokens) => void;
  setUser: (user: User) => void;
  /**
   * Drop the local session. Does NOT call the API.
   *
   * Use `useLogout()` from `@/api/auth` for a reader-initiated sign-out: DECISIONS
   * §7.2 requires `POST /api/auth/logout/` to blacklist the refresh token first,
   * and that call cannot live here without a cycle through `lib/api.ts`.
   */
  clearSession: () => void;
  /** @deprecated Alias of `clearSession`. Prefer `useLogout()`. */
  logout: () => void;
  /** Recompute `isAuthenticated` from storage. Wired to `storage` events. */
  syncFromStorage: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: hasSession(),
      setSession: (data) => {
        tokens.set(data.access, data.refresh);
        set({ user: data.user, isAuthenticated: hasSession() });
      },
      setUser: (user) => set({ user }),
      clearSession: () => {
        tokens.clear();
        set({ user: null, isAuthenticated: false });
      },
      logout: () => {
        tokens.clear();
        set({ user: null, isAuthenticated: false });
      },
      syncFromStorage: () => {
        const authed = hasSession();
        set((state) =>
          state.isAuthenticated === authed
            ? state
            : // Losing the tokens must also drop the cached profile, or the
              // avatar survives the session that justified it.
              { isAuthenticated: authed, user: authed ? state.user : null },
        );
      },
    }),
    {
      name: "wikiverse.auth",
      /** `user` only. `isAuthenticated` is derived; persisting it is the bug. */
      partialize: (state) => ({ user: state.user }),
      /**
       * Recompute on rehydrate, in the same commit: a persisted `user` with no
       * tokens beside it is a signed-out reader, not a signed-in one.
       */
      merge: (persisted, current) => {
        const stored = persisted as { user?: User | null } | undefined;
        const authed = hasSession();
        return {
          ...current,
          user: authed ? (stored?.user ?? null) : null,
          isAuthenticated: authed,
        };
      },
    },
  ),
);

/**
 * Cross-tab coherence. `storage` fires in every OTHER tab of the origin, which
 * is precisely the tab that used to be wrong.
 */
if (typeof window !== "undefined") {
  window.addEventListener("storage", (event) => {
    if (event.key === null || event.key.startsWith("wikiverse.")) {
      useAuthStore.getState().syncFromStorage();
    }
  });
}
