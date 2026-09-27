import { useEffect, useMemo, useState } from "react";

import { toReferences, type ReferenceDraft } from "@/api/editor";
import { Markdown } from "@/components/article/Markdown";
import {
  buildFootnoteScope,
  FootnoteContext,
  LinkResolutionContext,
  useArticleLinkResolver,
} from "@/components/article/markdownUtils";
import { cn } from "@/lib/utils";

/** The id this preview's body uses inside the footnote allocation. */
const SOURCE_ID = "content";

interface EditorPreviewProps {
  /** The raw Markdown body, straight from the textarea. */
  content: string;
  /** The title as typed, so the preview carries the same masthead. */
  title: string;
  short_description: string;
  /** The reference drafts, so `[^key]` markers get their real numbers. */
  references: ReferenceDraft[];
  /** Debounce, ms. 250 per design-ui §5.6. */
  delay?: number;
  className?: string;
}

/**
 * The live preview.
 *
 * Four things about it are deliberate:
 *
 * 1. **It is the article renderer, not a second one.** It imports
 *    `components/article/Markdown` — the same component `ArticlePage` uses, with
 *    the same plugin set and the same `skipHtml` posture (DECISIONS §0.4, §0.5).
 *    A preview that renders through a different pipeline is a preview that lies,
 *    and a second renderer is how `dangerouslySetInnerHTML` gets reintroduced by
 *    the back door.
 * 2. **Footnotes are numbered from the draft references**, through the article's
 *    own `buildFootnoteScope`. Without the provider every `[^key]` renders `[?]`,
 *    which is correct but unhelpful while the apparatus is being written; with it
 *    the author sees `[1]`, `[2]` in the order the reference list will print
 *    them, and a genuinely unresolved key still shows `[?]`.
 * 3. **The heading is a `<div>`, not an `<h1>`.** The page already has one `<h1>`
 *    ("Editing …"). A preview that mints a second one breaks the document outline
 *    for every screen reader to gain nothing: the serif face and the rule under
 *    it carry the whole visual signature on their own.
 * 4. **`aria-live` is off.** A region that announced on every keystroke would
 *    make the editor unusable with a screen reader. The author already knows
 *    what they typed; the preview is there to be looked at.
 */
export function EditorPreview({
  content,
  title,
  short_description,
  references,
  delay = 250,
  className,
}: EditorPreviewProps) {
  const [deferred, setDeferred] = useState(content);

  useEffect(() => {
    const timer = setTimeout(() => setDeferred(content), delay);
    return () => clearTimeout(timer);
  }, [content, delay]);

  /**
   * Red links in the preview, from the same resolver the article uses.
   *
   * Passing `undefined` takes the `GET /api/wanted/` branch — one cached
   * request for the whole session, covering every red-link target in the
   * corpus rather than one article's link rows. That is exactly what a preview
   * needs, because the page being written has no link rows yet. A title the
   * endpoint does not know about resolves as UNKNOWN and renders blue, so the
   * failure mode is a missing red link, never an invented one.
   */
  const resolveLink = useArticleLinkResolver(undefined);

  const scope = useMemo(
    () =>
      buildFootnoteScope(toReferences(references), [
        { id: SOURCE_ID, text: deferred },
      ]),
    [references, deferred],
  );

  const heading = title.trim();
  const gloss = short_description.trim();

  return (
    <div
      aria-live="off"
      className={cn(
        "overflow-auto rounded-chrome border border-rule bg-page px-4 py-4",
        className,
      )}
    >
      <div className="font-serif text-h1 leading-[1.25] font-normal text-ink">
        {heading || <span className="text-ink-3">Untitled</span>}
      </div>
      {gloss && <p className="mt-1 text-ui text-ink-2">{gloss}</p>}
      <hr className="mt-1.5 mb-4 border-0 border-t border-rule" />

      {deferred.trim() ? (
        <LinkResolutionContext.Provider value={resolveLink}>
          <FootnoteContext.Provider value={scope}>
            <Markdown content={deferred} sourceId={SOURCE_ID} lead />
          </FootnoteContext.Provider>
        </LinkResolutionContext.Provider>
      ) : (
        <p className="text-base text-ink-3">
          The rendered article appears here as you write.
        </p>
      )}
    </div>
  );
}
