import { cn } from "@/lib/utils";
import { WikiLink } from "./WikiLink";

/**
 * Canonical phrasings only.
 *
 * Free-text hatnotes are deliberately not authorable: a wiki's tone stays
 * consistent because the six sentences it is allowed to say are the six
 * sentences below, and a typed discriminated union is how that is enforced at
 * the call site instead of in review.
 */
export type HatnoteSpec =
  /** "For other uses, see X (disambiguation)." */
  | { variant: "other-uses"; target: string }
  /** "Not to be confused with X." */
  | { variant: "not-to-be-confused"; target: string }
  /** "This article is about A. For B, see C." */
  | { variant: "about"; about: string; other: string; target: string }
  /** "Main article: X" */
  | { variant: "main-article"; target: string }
  /** "See also: X, Y" */
  | { variant: "see-also"; targets: string[] }
  /** "X redirects here. For other uses, see Y." */
  | { variant: "redirect"; from: string; target: string };

export interface HatnoteProps {
  spec: HatnoteSpec;
  className?: string;
}

/**
 * A hatnote: italic, no border, no fill, directly under the title block.
 *
 * It sits BEFORE the infobox in DOM order, which MOS:LAYOUT requires for
 * screen-reader order and which is easy to get wrong once the infobox floats —
 * the float makes the wrong order look right.
 *
 * Below 768px it becomes a small panel-filled note rather than an italic line,
 * because at phone width an unbordered italic paragraph above the lead reads as
 * part of the article rather than as a note about it.
 */
export function Hatnote({ spec, className }: HatnoteProps) {
  return (
    <div
      role="note"
      className={cn(
        "hatnote max-w-[var(--measure-prose)] italic",
        "mb-2 rounded-chrome bg-panel px-2 py-[0.35em] text-[0.8125rem] text-ink-2",
        "md:bg-transparent md:px-0 md:py-0 md:pl-[1.6em] md:text-[length:inherit] md:text-ink",
        className,
      )}
    >
      <HatnoteText spec={spec} />
    </div>
  );
}

function HatnoteText({ spec }: { spec: HatnoteSpec }) {
  switch (spec.variant) {
    case "other-uses":
      return (
        <>
          For other uses, see <WikiLink title={spec.target} />.
        </>
      );

    case "not-to-be-confused":
      return (
        <>
          Not to be confused with <WikiLink title={spec.target} />.
        </>
      );

    case "about":
      return (
        <>
          This article is about {spec.about}. For {spec.other}, see{" "}
          <WikiLink title={spec.target} />.
        </>
      );

    case "main-article":
      return (
        <>
          Main article: <WikiLink title={spec.target} />
        </>
      );

    case "see-also":
      return (
        <>
          See also:{" "}
          {spec.targets.map((target, index) => (
            <span key={target}>
              {index > 0 ? ", " : null}
              <WikiLink title={target} />
            </span>
          ))}
        </>
      );

    case "redirect":
      return (
        <>
          &ldquo;{spec.from}&rdquo; redirects here. For other uses, see{" "}
          <WikiLink title={spec.target} />.
        </>
      );

    default: {
      const unknown: never = spec;
      void unknown;
      return null;
    }
  }
}
