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
 *
 * A `span` displayed as a block, not a `div`: skeletons also stand in for
 * inline text (a byline inside a `<p>`), where a `div` is invalid nesting and
 * React warns about it. Pass `inline-block` to keep one on the text line.
 */
export function Skeleton({ className }: { className?: string }) {
  return (
    <span aria-hidden="true" className={cn("skeleton block rounded-chrome", className)} />
  );
}
