import type { PreviewCard } from "@/lib/types";
import type { PreviewPosition } from "./markdownUtils";

export interface HoverPreviewCardProps {
  /** Matches the trigger's `aria-describedby`. */
  id: string;
  data: PreviewCard;
  position: PreviewPosition;
  onPointerEnter: () => void;
  onPointerLeave: () => void;
}

/**
 * Page Previews: the small card a wikilink raises on hover or keyboard focus.
 *
 * The timing triple that makes it feel right — 150ms dwell before the fetch,
 * a 500ms floor before it may paint, 300ms of grace after the pointer leaves —
 * lives in `useHoverPreview`, which is where the behaviour is. This file is
 * only the card.
 *
 * `role="tooltip"` with `aria-describedby` on the trigger, `Escape` dismisses,
 * and the card is never the only route to the information: the same extract is
 * the search-result snippet and the typeahead gloss.
 *
 * Positioned in document coordinates and rendered through a portal, so the
 * float is not clipped by the article column's `min-w-0` grid track and does not
 * need a wrapper element inside the prose. `useHoverPreview` closes the card on
 * scroll, which is why absolute positioning is safe here.
 */
export function HoverPreviewCard({
  id,
  data,
  position,
  onPointerEnter,
  onPointerLeave,
}: HoverPreviewCardProps) {
  return (
    <div
      id={id}
      role="tooltip"
      onPointerEnter={onPointerEnter}
      onPointerLeave={onPointerLeave}
      style={{
        left: position.left,
        top: position.top,
        // Flipping above the trigger is a transform rather than a second
        // measurement pass: the card's height is not known until it paints.
        transform: position.flipped ? "translateY(calc(-100% - 4px))" : undefined,
      }}
      className="pointer-events-auto absolute z-40 w-[20rem] overflow-hidden rounded-chrome border border-rule bg-page shadow-[var(--shadow-menu)] motion-safe:animate-[preview-in_120ms_ease-out]"
    >
      {data.lead_image_url ? (
        <img
          src={data.lead_image_url}
          // The card is decorative relative to the link it describes: the title
          // and the extract below carry every fact. A duplicated alt would make
          // a screen reader read the subject twice.
          alt=""
          className="block h-[9rem] w-full border-b border-rule-hair object-cover"
          loading="lazy"
          decoding="async"
        />
      ) : null}

      <div className="p-3">
        <p className="font-serif text-[1.0625rem] leading-snug text-ink">{data.title}</p>
        {data.short_description ? (
          <p className="mt-0.5 text-2xs text-ink-3">{data.short_description}</p>
        ) : null}
        {data.extract ? (
          <p className="mt-1.5 text-ui leading-normal text-ink-2">{data.extract}</p>
        ) : null}
      </div>
    </div>
  );
}
