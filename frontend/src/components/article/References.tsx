import type { MouseEvent } from "react";

import type { Reference } from "@/lib/types";
import { cn, formatDate } from "@/lib/utils";
import { MarkdownInline } from "./Markdown";
import {
  backlinkLetter,
  citeNoteId,
  citeRefId,
  jumpToAnchor,
  parseIdentifier,
  useFootnoteScope,
} from "./markdownUtils";

/** Two columns above this many references, and only at `shelf` and wider. */
const TWO_COLUMN_THRESHOLD = 20;

export interface ReferencesProps {
  references: Reference[];
  /** The id the TOC targets. `"references"` unless a page needs its own. */
  id?: string;
  heading?: string;
}

/**
 * The reference list: `<ol class="reflist">` at 90% with hanging indent.
 *
 * Two details carry most of the authenticity and cost nothing:
 *   - a reference cited once gets a single `^` backlink; one cited three times
 *     gets `^ a b c`, each letter a separate anchor back to its own marker;
 *   - every entry ends `Retrieved 26 September 2026`, month spelled out, from
 *     `Reference.accessed_on`.
 *
 * `identifier` is ONE free-text field for ISBN, DOI and arXiv (DECISIONS §11),
 * so the label is sniffed from the prefix rather than stored.
 */
export function References({ references, id = "references", heading = "References" }: ReferencesProps) {
  const { totals } = useFootnoteScope();
  if (references.length === 0) return null;

  const ordered = [...references].sort((a, b) => a.order - b.order);

  return (
    <>
      <h2 id={id}>{heading}</h2>
      {/*
        A bare caret is announced as "circumflex", so every backlink is described
        by this one hidden label instead of carrying a wordy aria-label each.
      */}
      <span id="footnote-label" className="sr-only">
        Jump to a cited source
      </span>
      <ol
        className={cn("reflist", references.length > TWO_COLUMN_THRESHOLD && "reflist-2")}
      >
        {ordered.map((reference) => (
          <li key={reference.key} id={citeNoteId(reference.key)}>
            <Backlinks refKey={reference.key} total={totals[reference.key] ?? 0} />
            <Citation reference={reference} />
          </li>
        ))}
      </ol>
    </>
  );
}

function Backlinks({ refKey, total }: { refKey: string; total: number }) {
  function jump(event: MouseEvent<HTMLAnchorElement>, markerId: string) {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    jumpToAnchor(markerId);
  }

  // Cited nowhere: no backlink to offer, and an anchor to a non-existent id
  // would be a keyboard trap that goes nowhere.
  if (total === 0) {
    return (
      <span className="mw-cite-backlink" aria-hidden="true">
        ^
      </span>
    );
  }

  if (total === 1) {
    const markerId = citeRefId(refKey, 0);
    return (
      <span className="mw-cite-backlink">
        <a href={`#${markerId}`} onClick={(event) => jump(event, markerId)}>
          ^
        </a>
      </span>
    );
  }

  return (
    <span className="mw-cite-backlink">
      <span aria-hidden="true">^ </span>
      {Array.from({ length: total }, (_unused, n) => {
        const markerId = citeRefId(refKey, n);
        return (
          <a
            key={markerId}
            href={`#${markerId}`}
            className="backlink-letter"
            onClick={(event) => jump(event, markerId)}
          >
            {backlinkLetter(n)}
            {n < total - 1 ? " " : null}
          </a>
        );
      })}
    </span>
  );
}

function Citation({ reference }: { reference: Reference }) {
  const identifier = parseIdentifier(reference.identifier);

  // Reference titles go through the same renderer as everything else: no raw
  // HTML, `skipHtml`, and with links flattened so a citation title containing a
  // link cannot nest an anchor inside the anchor wrapping it.
  const title = <MarkdownInline content={reference.title} plainLinks />;

  return (
    <cite className="citation">
      {reference.authors ? <>{reference.authors} </> : null}
      {reference.published_on ? <>({reference.published_on}). </> : null}
      {reference.url ? (
        <a className="external" href={reference.url} target="_blank" rel="noreferrer noopener">
          &ldquo;{title}&rdquo;
        </a>
      ) : (
        <>&ldquo;{title}&rdquo;</>
      )}
      {reference.publisher ? (
        <>
          . <i>{reference.publisher}</i>
        </>
      ) : null}
      {identifier ? (
        <>
          .{" "}
          <span className={`cite-${identifier.kind}`}>
            {identifier.label ? `${identifier.label}${identifier.label.endsWith(":") ? "" : " "}` : null}
            {identifier.href ? (
              <a className="external" href={identifier.href} target="_blank" rel="noreferrer noopener">
                {identifier.value}
              </a>
            ) : (
              identifier.value
            )}
          </span>
        </>
      ) : null}
      {reference.accessed_on ? <>. Retrieved {formatDate(reference.accessed_on)}</> : null}.
      {reference.quote ? (
        <>
          {" "}
          <span className="text-ink-2">&ldquo;{reference.quote}&rdquo;</span>
        </>
      ) : null}
    </cite>
  );
}
