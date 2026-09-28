import { cn } from "@/lib/utils";

/**
 * Button styling, in its own module.
 *
 * It lives here rather than in `Button.tsx` for one concrete reason
 * (DECISIONS §18): `react-refresh/only-export-components` flags a non-
 * component export from a file that also exports a component, and the lint
 * gate runs with `--max-warnings=0`. Splitting it is what lets that gate be
 * clean. It stays exported because `<Link className={buttonVariants(...)}>`
 * is how a router link is given a button's shape.
 */

export type ButtonVariant =
  | "primary"
  | "secondary"
  | "ghost"
  | "outline"
  | "danger";

export type ButtonSize = "sm" | "md" | "lg" | "icon";

/**
 * THE PRIMARY BUTTON IS INK, NOT THE ACCENT. A page whose only saturated
 * elements are its links is the entire point of this design; a blue Save
 * button would compete with every wikilink on the page. Verified:
 * `--surface-page` text on an `--ink-1` fill measures 15.47:1 in light and
 * 13.60:1 in dark.
 *
 * No shadow on any variant. No `transition-all` — colours only.
 */
const VARIANTS: Record<ButtonVariant, string> = {
  primary: "bg-ink text-page hover:bg-ink/90",
  secondary: "border border-rule bg-panel text-ink hover:bg-inset",
  ghost: "text-link hover:bg-panel",
  outline: "border border-rule bg-page text-ink hover:bg-panel",
  danger:
    "border border-danger bg-page text-danger hover:bg-danger hover:text-page",
};

/**
 * Heights are 7 / 8 / 10, down from 8 / 10 / 12. This is a dense document
 * interface: a 40px button sitting beside 14px rail text is the SaaS
 * proportion, and it was one of the things that made the old app read as a
 * template.
 */
const SIZES: Record<ButtonSize, string> = {
  sm: "h-7 px-2 text-ui gap-1.5",
  md: "h-8 px-3 text-ui gap-1.5",
  lg: "h-10 px-4 text-base gap-2",
  icon: "size-8",
};

export function buttonVariants({
  variant = "primary",
  size = "md",
}: { variant?: ButtonVariant; size?: ButtonSize } = {}): string {
  return cn(
    "inline-flex cursor-pointer items-center justify-center rounded-chrome",
    "font-medium whitespace-nowrap transition-colors duration-100",
    // Focus is the ONE global :focus-visible rule in index.css. Nothing here
    // sets outline-none, because doing so is how the old build ended up with
    // seven controls that had no visible focus at all.
    "disabled:pointer-events-none disabled:opacity-50",
    VARIANTS[variant],
    SIZES[size],
  );
}
