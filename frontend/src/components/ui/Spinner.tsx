import { Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";

interface SpinnerProps {
  className?: string;
  /**
   * What is loading. Announced once via `role="status"`; pass `null` when a
   * surrounding live region already says it, so a screen reader is not told
   * twice.
   */
  label?: string | null;
}

/**
 * The one place an indeterminate animation is legitimate: it communicates
 * "still working", which no static mark can. Under
 * `prefers-reduced-motion: reduce` the global base layer collapses its
 * duration, so it settles into a static arc rather than spinning — still a
 * visible indicator, no vestibular cost.
 */
export function Spinner({ className, label = "Loading" }: SpinnerProps) {
  return (
    <span role="status" className="inline-flex items-center">
      <Loader2 aria-hidden="true" className={cn("size-4 animate-spin", className)} />
      {label !== null && <span className="sr-only">{label}</span>}
    </span>
  );
}
