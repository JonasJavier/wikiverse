import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

/**
 * Form controls.
 *
 * Two deliberate decisions:
 *
 * 1. `text-base` (16px) is not negotiable. Any smaller and iOS Safari zooms
 *    the viewport on focus, which on a document-shaped page throws the
 *    reader out of the layout entirely.
 * 2. Nothing here sets `outline-none` or its own focus ring. Focus is the
 *    single global `:focus-visible` rule in `index.css`, in `--focus` —
 *    which is a brighter, more saturated blue than `--link`, so a focused
 *    control is never mistaken for a link. The old controls each set
 *    `focus:ring-ring`, where `--ring` was the link colour.
 */
const FIELD_BASE =
  "w-full rounded-chrome border border-rule bg-page px-2.5 py-1.5 " +
  "text-base text-ink placeholder:text-ink-3 " +
  "transition-colors duration-100 " +
  "disabled:cursor-not-allowed disabled:opacity-50 " +
  "aria-[invalid=true]:border-danger";

export function Input({ className, ...props }: ComponentProps<"input">) {
  return <input className={cn(FIELD_BASE, className)} {...props} />;
}

interface TextareaProps extends ComponentProps<"textarea"> {
  /**
   * The editor body: mono voice on the inset surface, which is what makes
   * wiki markup legible while it is being written.
   */
  code?: boolean;
}

export function Textarea({ className, code, ...props }: TextareaProps) {
  return (
    <textarea
      className={cn(
        FIELD_BASE,
        "resize-y",
        code && "bg-inset font-mono text-xs leading-relaxed",
        className,
      )}
      {...props}
    />
  );
}

export function Label({ className, ...props }: ComponentProps<"label">) {
  return (
    <label
      className={cn("mb-1 block text-ui font-medium text-ink", className)}
      {...props}
    />
  );
}

/** Helper text under a control. Reference it with `aria-describedby`. */
export function FieldHint({ className, ...props }: ComponentProps<"p">) {
  return <p className={cn("mt-1 text-xs text-ink-2", className)} {...props} />;
}

/**
 * A validation message. `role="alert"` so it is announced when it appears;
 * the control itself must carry `aria-invalid` and `aria-describedby`.
 */
export function FieldError({ className, ...props }: ComponentProps<"p">) {
  return (
    <p
      role="alert"
      className={cn("mt-1 text-xs text-danger", className)}
      {...props}
    />
  );
}
