import { cn } from "@/lib/utils";

/**
 * A static placeholder block, not an animated one.
 *
 * The old version ran an infinite `shimmer` keyframe across every loading
 * block on the page. An infinite animation on a reader-facing surface was
 * the worst accessibility item in the previous stylesheet, and it bought
 * nothing: a plain panel-coloured rectangle already reads as "not here yet".
 *
 * `aria-hidden` because the block is decorative — the surrounding region
 * owns the `aria-busy` / live-region announcement.
 */
export function Skeleton({ className }: { className?: string }) {
  return (
    <div aria-hidden="true" className={cn("skeleton rounded-chrome", className)} />
  );
}
