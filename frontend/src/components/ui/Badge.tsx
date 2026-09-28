import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

/**
 * Two badges, and the difference matters.
 *
 * A CATEGORY badge (`color` given) renders the database hex as a **2px left
 * rule only** — never as a text colour, never as a background. The previous
 * component used an arbitrary `Category.color` as both the text colour and a
 * 14% background, which measured between 1.93:1 and 3.75:1 for the four
 * seeded colours. That construction cannot be made safe by picking better
 * hexes, because the corpus will grow to ~14 categories. As a 2px graphical
 * accent the hex has no text-contrast requirement at all, so this is safe
 * for *any* input colour, forever — and it echoes the maintenance-banner
 * left-rule language, so the system has one idea instead of two.
 *
 * A VARIANT badge (Stub / Featured / Disambiguation) is ink plus a hairline.
 * No colour, because none of those three states means anything chromatic.
 */

export type BadgeVariant = "default" | "stub" | "featured" | "disambiguation";

interface BadgeProps extends ComponentProps<"span"> {
  /** A category hex. Rendered as a leading 2px rule and nothing else. */
  color?: string;
  variant?: BadgeVariant;
}

const VARIANT_LABELLED =
  "inline-flex items-center rounded-chrome border border-rule px-1.5 " +
  "text-2xs font-medium tracking-[0.04em] text-ink-2 uppercase";

export function Badge({
  className,
  color,
  variant = "default",
  style,
  children,
  ...props
}: BadgeProps) {
  if (color) {
    return (
      <span
        className={cn(
          "inline-flex items-baseline gap-1.5 border-l-2 pl-1.5 text-ui text-ink",
          className,
        )}
        style={{ borderLeftColor: color, ...style }}
        {...props}
      >
        {children}
      </span>
    );
  }

  return (
    <span
      className={cn(
        VARIANT_LABELLED,
        variant === "default" && "tracking-normal normal-case",
        className,
      )}
      style={style}
      {...props}
    >
      {children}
    </span>
  );
}
