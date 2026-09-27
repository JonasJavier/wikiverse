import { Link } from "react-router-dom";

import { cn } from "@/lib/utils";

/**
 * An original mark: an open codex whose gutter carries a small orbit.
 *
 * Drawn in `currentColor` with no gradient and no fill-on-fill, so it is legible
 * at 20px, inverts for free in dark mode, and prints. It is NOT a puzzle globe,
 * not a derivative of one, and carries no Wikipedia wordmark — deliberately, for
 * the trademark reason recorded in `survey-wikipedia.md`.
 */
export function WikiverseMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      className={className}
    >
      {/* The two leaves of an open book. */}
      <path d="M12 6.2C10.3 4.9 8 4.3 5 4.3a1 1 0 0 0-1 1v12.1a1 1 0 0 0 1 1c3 0 5.3.6 7 1.9" />
      <path d="M12 6.2c1.7-1.3 4-1.9 7-1.9a1 1 0 0 1 1 1v12.1a1 1 0 0 1-1 1c-3 0-5.3.6-7 1.9" />
      {/* The gutter. */}
      <path d="M12 6.2v14" />
      {/* The orbit: a reference work that cross-references itself. */}
      <ellipse cx="12" cy="11.4" rx="4.4" ry="2.1" transform="rotate(-24 12 11.4)" />
    </svg>
  );
}

interface LogoProps {
  withText?: boolean;
  className?: string;
  /** Rendered as a plain span rather than a link — for the footer masthead. */
  asLink?: boolean;
}

/**
 * The wordmark: serif, weight 400, ONE colour.
 *
 * The old version set "verse" in the accent. A two-tone wordmark is a startup
 * tell, and under this system the accent means "this is a link" — spending it on
 * half a word spends the one signal the page has.
 */
export function Logo({ withText = true, className, asLink = true }: LogoProps) {
  const inner = (
    <>
      <WikiverseMark className="size-6 shrink-0" />
      {withText && (
        <span className="font-serif text-[1.375rem] leading-none font-normal tracking-tight text-ink">
          Wikiverse
        </span>
      )}
    </>
  );

  if (!asLink) {
    return (
      <span className={cn("flex shrink-0 items-center gap-2 text-ink", className)}>
        {inner}
      </span>
    );
  }

  return (
    <Link
      to="/"
      aria-label="Wikiverse, main page"
      className={cn(
        "flex shrink-0 items-center gap-2 rounded-chrome text-ink hover:text-ink",
        className,
      )}
    >
      {inner}
    </Link>
  );
}
