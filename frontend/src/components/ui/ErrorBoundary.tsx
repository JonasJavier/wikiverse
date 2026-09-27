import { Component, type ErrorInfo, type ReactNode } from "react";
import { Link, isRouteErrorResponse, useRouteError } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { buttonVariants } from "@/components/ui/buttonVariants";

/**
 * A short, human-transcribable reference for the failure.
 *
 * Sentry is not installed in this build, so there is no `eventId` to display.
 * design-ui §4.19 is right that a reference code is what makes an error page
 * look professional rather than apologetic, so one is generated locally and
 * logged alongside the stack. When Sentry lands, replace the body of this
 * function with `Sentry.captureException(...)` and print the returned id — the
 * fallback's markup does not change.
 */
function reference(): string {
  return Math.random().toString(36).slice(2, 8).toUpperCase();
}

export interface ErrorFallbackProps {
  title?: string;
  message?: ReactNode;
  /** The reference code shown to the reader. */
  eventId?: string | null;
  /** Omitted when there is nothing a retry could fix. */
  onRetry?: () => void;
}

/**
 * The fallback surface. Deliberately the same title-block signature as every
 * other page — serif h1, a rule, a 14px line under it — because an error page
 * that abandons the site's typography reads as a crash rather than a page.
 */
export function ErrorFallback({
  title = "Something went wrong",
  message = "This page could not be displayed. The failure has been logged.",
  eventId,
  onRetry,
}: ErrorFallbackProps) {
  return (
    <div className="mx-auto max-w-[40rem] px-4 py-12">
      <h1 className="font-serif text-h1 font-normal text-ink text-balance">{title}</h1>
      <hr className="mt-1.5 border-0 border-t border-rule" />
      <p className="mt-3 text-read text-ink">{message}</p>
      {eventId && (
        <p className="mt-2 text-ui text-ink-2">
          Reference: <code className="font-mono text-ink">{eventId}</code>
        </p>
      )}
      <div className="mt-4 flex flex-wrap gap-2">
        {onRetry && <Button onClick={onRetry}>Try again</Button>}
        {/* A router link given a button's shape, rather than a <button> wrapping
            an <a>, which is invalid and unfocusable in the useful order. */}
        <Link to="/" className={buttonVariants({ variant: "secondary" })}>
          Main page
        </Link>
      </div>
    </div>
  );
}

interface ErrorBoundaryProps {
  children: ReactNode;
  /**
   * Changing this resets the boundary. `Layout.tsx` passes the router
   * `location.key`, so navigating away from a broken route clears the error
   * instead of stranding the reader on the fallback for the rest of the session.
   */
  resetKey?: string | number;
  fallback?: (props: {
    error: Error;
    eventId: string;
    reset: () => void;
  }) => ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
  eventId: string;
  resetKey: string | number | undefined;
}

/**
 * A real class component. React 19 still ships no hook for this — `useEffect`
 * cannot catch a render-phase throw, which is the case that matters.
 */
export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = {
    error: null,
    eventId: "",
    resetKey: this.props.resetKey,
  };

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { error, eventId: reference() };
  }

  /**
   * Reset on a changed `resetKey`, in the derived-state phase rather than in an
   * effect. Doing it in `componentDidUpdate` renders the stale fallback once
   * more before clearing it, which flashes an error page on a page that is fine.
   */
  static getDerivedStateFromProps(
    props: ErrorBoundaryProps,
    state: ErrorBoundaryState,
  ): Partial<ErrorBoundaryState> | null {
    if (props.resetKey !== state.resetKey) {
      return { error: null, eventId: "", resetKey: props.resetKey };
    }
    return null;
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // The one console call in the app that is not debug noise: without it the
    // reference code shown to the reader corresponds to nothing.
    console.error(`[wikiverse ${this.state.eventId}]`, error, info.componentStack);
  }

  private reset = (): void => {
    this.setState({ error: null, eventId: "" });
  };

  render(): ReactNode {
    const { error, eventId } = this.state;
    if (!error) return this.props.children;

    if (this.props.fallback) {
      return this.props.fallback({ error, eventId, reset: this.reset });
    }

    return <ErrorFallback eventId={eventId} onRetry={this.reset} />;
  }
}

/**
 * For the router's `errorElement`. A loader or router failure never reaches the
 * boundary above — it is handled by the data router before render — so the route
 * tree needs its own. A 404 from the router is reported as what it is rather
 * than as a crash.
 */
export function RouteErrorFallback() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <ErrorFallback
        title={error.status === 404 ? "Page not found" : `Error ${error.status}`}
        message={
          error.status === 404
            ? "There is no page at this address. It may have been deleted, or the link may be wrong."
            : error.statusText || "The request could not be completed."
        }
      />
    );
  }

  return (
    <ErrorFallback
      message={
        error instanceof Error
          ? error.message
          : "This page could not be displayed."
      }
    />
  );
}
