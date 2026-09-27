import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface EmptyStateProps {
  title: string;
  /** One sentence of context. `description` is the legacy name for the same thing. */
  hint?: ReactNode;
  description?: ReactNode;
  action?: ReactNode;
  className?: string;
  /**
   * Accepted and ignored. The empty state has no icon and no illustration by
   * design; this exists only so call sites written against the old signature
   * keep compiling while they are rewritten. Remove it with the last caller.
   *
   * @deprecated
   */
  icon?: LucideIcon;
}

/**
 * A bordered panel with a sentence in it. No icon, no illustration, no
 * centred 16rem of air.
 *
 * **No `<h3>`.** The old version emitted an `h3` with no `h1` or `h2` above
 * it, producing a heading-order failure on every empty page in the app. The
 * page owns its `h1`; an empty state is a paragraph.
 */
export function EmptyState({
  title,
  hint,
  description,
  action,
  className,
}: EmptyStateProps) {
  const body = hint ?? description;
  return (
    <div
      className={cn(
        "rounded-chrome border border-rule-hair bg-panel px-4 py-6 text-ui",
        className,
      )}
    >
      <p className="font-medium text-ink">{title}</p>
      {body && <p className="mt-1 text-ink-2">{body}</p>}
      {action && <div className="mt-3">{action}</div>}
    </div>
  );
}
