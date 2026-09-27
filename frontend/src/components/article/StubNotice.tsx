import { Link } from "react-router-dom";

export interface StubNoticeProps {
  /** The article's slug, for the "expanding it" link. */
  slug: string;
  /** The primary category name, lowercased into the sentence. */
  categoryName?: string | null;
}

/**
 * The stub notice: a hairline rule, then one small italic line, at the VERY
 * bottom of the page — after the category bar, which is where MediaWiki puts it
 * and the last thing a reader meets.
 *
 * "This mathematics-related article is a stub. You can help by expanding it."
 * The phrasing is fixed; only the category varies.
 */
export function StubNotice({ slug, categoryName }: StubNoticeProps) {
  const topic = categoryName?.trim();

  return (
    <>
      <hr className="stub-rule mt-6 border-0 border-t border-rule-hair" />
      <div
        role="note"
        className="stub flex items-baseline gap-2 pt-[0.6em] font-sans text-[0.824em] italic text-ink-2"
      >
        <span aria-hidden="true" className="not-italic text-warn">
          {/* A glyph rather than an icon component: it sits on the text baseline
              and costs no bundle. */}
          &#9671;
        </span>
        <span>
          This {topic ? `${topic.toLowerCase()}-related ` : ""}article is a stub. You can help by{" "}
          <Link to={`/wiki/${slug}/edit`}>expanding it</Link>.
        </span>
      </div>
    </>
  );
}
