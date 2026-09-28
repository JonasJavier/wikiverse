import type { MouseEvent } from "react";

import { citeNoteId, citeRefId, jumpToAnchor, useFootnoteScope } from "./markdownUtils";

export interface FootnoteMarkerProps {
  /** The `refkey` from `[^refkey]`, matching a `Reference.key`. */
  refKey: string;
  /** 0-based occurrence index of THIS marker among markers citing `refKey`. */
  index: number;
}

/**
 * The in-text citation marker: `[12]`.
 *
 * The bracket spans are not decoration. They are what lets a future "hide
 * brackets" preference exist, and `white-space: nowrap` on `.reference` is what
 * stops `[12]` breaking across a line — a small thing that looks very wrong
 * when it is missing.
 *
 * Ids are the exact formats in DECISIONS §14: the marker is
 * `cite_ref-{key}-{n}` and it points at `cite_note-{key}`. `n` is allocated
 * before render by `buildFootnoteScope`, never by a counter that a StrictMode
 * double render would advance twice.
 *
 * `:visited` is suppressed on footnote markers in `index.css`, deliberately:
 * visited-purple is a navigation signal for ARTICLE links, and every footnote on
 * a page the reader has scrolled past would turn purple, destroying the signal
 * everywhere it matters.
 */
export function FootnoteMarker({ refKey, index }: FootnoteMarkerProps) {
  const { numbers } = useFootnoteScope();
  const number = numbers[refKey];

  // A marker with no reference is an authoring error the corpus validator is
  // supposed to catch. Render it visibly rather than silently dropping it:
  // a missing citation that looks like a citation is worse than one that
  // announces itself.
  if (number === undefined) {
    return (
      <sup
        className="reference"
        title={`No reference in this article has the key “${refKey}”`}
      >
        <span className="cite-bracket">[</span>?<span className="cite-bracket">]</span>
      </sup>
    );
  }

  const noteId = citeNoteId(refKey);

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    // Let the browser handle a modified click: opening a citation in a new tab
    // is a real thing readers do.
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    // `ref-flash` rather than `:target`: it restarts on a repeat click, which
    // `:target` cannot, and it is a background change rather than motion, so it
    // survives `prefers-reduced-motion`.
    jumpToAnchor(noteId, "ref-flash");
  }

  return (
    <sup className="reference" id={citeRefId(refKey, index)}>
      <a href={`#${noteId}`} onClick={handleClick} aria-describedby="footnote-label">
        <span className="cite-bracket">[</span>
        {number}
        <span className="cite-bracket">]</span>
      </a>
    </sup>
  );
}
