import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { tokens } from "@/lib/tokens";
import { useAuthStore } from "@/store/auth";

/**
 * A gate in front of the routes that need a session.
 *
 * Two things it gets right that the old version did not:
 *
 * 1. **It asks the tokens, not a persisted boolean.** `useAuthStore` now derives
 *    `isAuthenticated` from storage, and this component reads the tokens as well,
 *    so the gate is correct even in the instant before the persisted store has
 *    rehydrated. A gate that trusts a flag written in a previous session admits a
 *    reader with no credentials at all, and the page behind it then fails one
 *    request at a time.
 * 2. **It preserves the whole location, not just the pathname.** A red link
 *    points at `/new?title=Photosynthesis`. Sending an anonymous reader to
 *    `/login` and then back to a bare `/new` throws away the one piece of
 *    information that made the red link worth clicking. `search` and `hash`
 *    travel with it.
 *
 * The redirect `replace`s, so Back from `/login` returns to the article the
 * reader came from rather than bouncing through the gate again.
 */
export function ProtectedRoute({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const location = useLocation();

  const hasToken = (() => {
    try {
      return Boolean(tokens.access() ?? tokens.refresh());
    } catch {
      // Blocked storage reads as signed out, rather than throwing out of a route.
      return false;
    }
  })();

  if (!isAuthenticated && !hasToken) {
    return (
      <Navigate
        to="/login"
        replace
        state={{
          from: `${location.pathname}${location.search}${location.hash}`,
        }}
      />
    );
  }

  return <>{children}</>;
}
