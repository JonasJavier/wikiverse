import type { ReactNode } from "react";

/* =====================================================================
   WHY THIS COMPONENT EXISTS AT ALL
   =====================================================================
   `snippet` and `title_snippet` are built by PostgreSQL's `ts_headline`,
   which re-tokenises the RAW ARTICLE BODY — text any signed-in editor can
   write. The backend therefore asks `ts_headline` for control characters
   (STX/ETX) as its delimiters, runs `html.escape()` over the whole result,
   and only then swaps those two control characters for the literal strings
   `<mark>` and `</mark>` (apps/articles/search.py :: safe_headline_to_marked,
   DECISIONS §3).

   So the string arriving here is escaped text plus exactly two possible
   tags. It is NOT trusted markup, and it must never be treated as markup:

     * `dangerouslySetInnerHTML` would be STORED XSS. The moment any HTML
       path exists here, the question becomes "is every byte of every
       article body safe?", and the answer is no — an editor can type
       `<img src=x onerror=...>` into an article and the search page is
       where it would fire. There is no such path in this app; DECISIONS §0
       invariant 4 forbids it outright.
     * An `innerHTML`/`DOMParser`/regex "sanitiser" would be the same hole
       with more code in front of it, and it would have to be audited every
       time the highlighter changed.

   Instead this component SPLITS THE STRING on the two literal tokens and
   builds React elements from the pieces. Everything that is not a token is
   a plain JavaScript string handed to React as a text node, which React
   escapes on render. The strongest thing an attacker controls in the output
   is therefore where a `<b>` starts and stops — no attributes, no other
   element, no script, and no code path that could ever produce one.

   Unbalanced or nested tokens are harmless by construction: the depth
   counter below clamps at zero, so a stray `</mark>` renders as ordinary
   text rather than leaking into the surrounding output.
   ===================================================================== */

const MARK_OPEN = "<mark>";
const MARK_CLOSE = "</mark>";

/** Captures the two tokens, so `split` keeps them as separate pieces. */
const TOKENS = /(<mark>|<\/mark>)/g;

/**
 * The five (plus one alias) entities `html.escape(s, quote=True)` can emit.
 *
 * The text is escaped, so `Ampère & Ohm` reaches us as `Ampère &amp; Ohm`.
 * Rendering that as a text node would print the entity, so the pieces are
 * decoded — with a fixed table in ONE regex pass, never by assigning to
 * `innerHTML` and reading `textContent` back, and never with chained
 * `.replace()` calls (which decode `&amp;lt;` twice and reintroduce exactly
 * the `<` the backend removed).
 *
 * Nothing outside this table is decoded. A numeric entity an author typed
 * literally stays literal text, which is correct: it was literal text in the
 * article too.
 */
const ENTITIES: Record<string, string> = {
  "&amp;": "&",
  "&lt;": "<",
  "&gt;": ">",
  "&quot;": '"',
  "&#x27;": "'",
  "&#39;": "'",
};

const ENTITY = /&(?:amp|lt|gt|quot|#x27|#39);/g;

function decodeEscapedText(piece: string): string {
  return piece.replace(ENTITY, (entity) => ENTITIES[entity] ?? entity);
}

interface SnippetProps {
  /**
   * `SearchResult.snippet` or `SearchResult.title_snippet`: escaped text
   * containing the two literal `<mark>` tokens. Same component for both.
   */
  text: string;
  /** Rendered when `text` is blank — e.g. the plain title behind a snippet. */
  fallback?: string;
  className?: string;
}

/**
 * Highlighting is **bold only, with no background tint** (survey-wikipedia
 * §6.6, measured). It is cleaner than a yellow `mark` in a dense list, it
 * needs no colour token, and it survives dark mode with no extra work —
 * which is why `--mark` is reserved for the editor's find bar. `text-inherit`
 * keeps a highlighted run inside a link the link's own colour.
 */
export function Snippet({ text, fallback = "", className }: SnippetProps) {
  const source = text || fallback;
  if (!source) return null;

  const pieces = source.split(TOKENS);
  const out: ReactNode[] = [];
  let depth = 0;

  for (let i = 0; i < pieces.length; i += 1) {
    const piece = pieces[i];

    if (piece === MARK_OPEN) {
      depth += 1;
      continue;
    }
    if (piece === MARK_CLOSE) {
      depth = Math.max(0, depth - 1);
      continue;
    }
    if (!piece) continue;

    const value = decodeEscapedText(piece);
    out.push(
      depth > 0 ? (
        <b key={i} className="font-bold text-inherit">
          {value}
        </b>
      ) : (
        value
      ),
    );
  }

  if (className) return <span className={className}>{out}</span>;
  return <>{out}</>;
}
