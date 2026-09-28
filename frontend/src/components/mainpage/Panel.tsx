import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface PanelProps {
  /** Rendered as the panel's `h2`; it is the section heading, not a label. */
  title: string;
  /**
   * A link or a count shown at the right of the header bar, e.g.
   * `All recent changes →`. Kept out of the heading text so the heading a
   * screen reader announces is the section name and nothing else.
   */
  action?: ReactNode;
  /** `aria-busy` while the panel's query is in flight. */
  busy?: boolean;
  className?: string;
  /** Padding is on the body, so a full-bleed list can opt out with `flush`. */
  flush?: boolean;
  children: ReactNode;
}

/**
 * A bordered panel with a serif header bar on `--surface-panel`.
 *
 * This is the main page's and the category page's only container, and it is
 * deliberately not a card: one hairline border, one 2px radius, no shadow, no
 * gradient, no hover state. The header bar sitting on the panel surface while
 * the body sits on the page surface is what makes a stack of these read as a
 * reference work rather than as a dashboard.
 *
 * The heading is `font-normal` on purpose (§2.3): at 19px the serif carries
 * the hierarchy by family and size, and a bold weight here would compete with
 * the article titles inside the panel.
 */
export function Panel({
  title,
  action,
  busy,
  className,
  flush = false,
  children,
}: PanelProps) {
  return (
    <section
      aria-busy={busy || undefined}
      className={cn(
        "rounded-chrome border border-rule bg-page",
        "flex min-w-0 flex-col",
        className,
      )}
    >
      <div className="flex items-baseline justify-between gap-3 border-b border-rule bg-panel px-3 py-1.5">
        <h2 className="font-serif text-[1.1875rem] leading-snug font-normal text-ink">
          {title}
        </h2>
        {action && <span className="shrink-0 text-ui">{action}</span>}
      </div>
      <div className={cn("min-w-0 flex-1", !flush && "px-3 py-3")}>{children}</div>
    </section>
  );
}
