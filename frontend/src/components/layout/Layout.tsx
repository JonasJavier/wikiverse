import { Outlet, ScrollRestoration, useLocation } from "react-router-dom";

import { useMe } from "@/api/auth";
import { ErrorBoundary } from "@/components/ui/ErrorBoundary";
import { ToastViewport } from "@/components/ui/Toast";
import { SiteFooter } from "./SiteFooter";
import { SiteHeader } from "./SiteHeader";
import { SkipLink } from "./SkipLink";

/**
 * What mounts where (design-ui §3.11).
 *
 * The skip link is the first focusable element; `<main id="content">` is its
 * target and carries `tabIndex={-1}` so the jump moves keyboard focus, not just
 * the scroll position. Pages bring their own `WikiFrame`, so each decides its
 * rails. The error boundary is keyed on the location, so navigating away from a
 * broken page clears it. The theme is applied by `store/theme.ts` itself.
 */
export function Layout() {
  const location = useLocation();
  // Validate / hydrate the persisted session against the backend.
  useMe();

  return (
    <div className="flex min-h-full flex-col bg-shell">
      <SkipLink />
      <SiteHeader />
      <main id="content" tabIndex={-1} className="min-h-[60vh] flex-1 focus:outline-none">
        <ErrorBoundary resetKey={location.pathname}>
          <Outlet />
        </ErrorBoundary>
      </main>
      <SiteFooter />
      <ToastViewport />
      <ScrollRestoration />
    </div>
  );
}
