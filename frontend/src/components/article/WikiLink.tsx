import type { ReactNode } from "react";
import { createPortal } from "react-dom";
import { Link } from "react-router-dom";

import { useMediaQuery } from "@/hooks/useMediaQuery";
import { cn } from "@/lib/utils";
import { HoverPreviewCard } from "./HoverPreviewCard";
import {
  createPageHref,
  redLinkTitle,
  useHoverPreview,
  useLinkResolution,
  wikiHref,
} from "./markdownUtils";

export interface WikiLinkProps {
  /** The EXACT article title from `[[Title]]`, not a slug. */
  title: string;
  /** `[[Title#Section]]` — the section to jump to on arrival. */
  anchor?: string;
  /** The display text. Defaults to the title, as MediaWiki does. */
  children?: ReactNode;
  className?: string;
}

/**
 * An internal `[[wikilink]]`, in one of its two states.
 *
 * BLUE (or the visited purple, which is a navigation primitive rather than
 * decoration — a wiki reader navigates by remembering what they have already
 * read) when the target exists, and **RED** when it does not.
 *
 * The red state is a deliberate product decision, not a defect to hide
 * (DECISIONS §19): the corpus ships 63 of 120 planned articles, so a large
 * minority of links point at titles nobody has written. A red link states that
 * fact, says so in its `title` attribute for anyone who cannot see the colour,
 * and points at `/new?title=<Title>` so a reader can start the article in one
 * click. That is what a real wiki looks like.
 *
 * Existence is resolved page-level, never per link — see
 * `useArticleLinkResolver`. A link whose state is genuinely unknown renders
 * blue: a missing red link is a small loss, an invented one is a lie about the
 * corpus.
 */
export function WikiLink({ title, anchor, children, className }: WikiLinkProps) {
  const resolve = useLinkResolution();
  const { slug, exists } = resolve(title);

  // No previews on touch: a tap goes straight to the article, so a card would
  // only be a second thing to dismiss. `(hover: none)` is the honest test —
  // pointer width is not.
  const coarsePointer = useMediaQuery("(hover: none)");
  const preview = useHoverPreview(slug, exists !== false && !coarsePointer);

  const label = children ?? title;

  if (exists === false) {
    return (
      <Link
        to={createPageHref(title)}
        // Both class names: `.is-redlink` (DECISIONS §19) and MediaWiki's own
        // `.new`, because index.css honours either convention.
        className={cn("is-redlink new", className)}
        title={redLinkTitle(title)}
      >
        {label}
      </Link>
    );
  }

  return (
    <>
      <Link to={wikiHref(slug, anchor)} className={className} {...preview.trigger}>
        {label}
      </Link>
      {preview.open && preview.position && preview.data
        ? createPortal(
            <HoverPreviewCard
              id={preview.id}
              data={preview.data}
              position={preview.position}
              {...preview.card}
            />,
            document.body,
          )
        : null}
    </>
  );
}
