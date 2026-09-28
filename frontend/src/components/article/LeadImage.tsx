import { cn } from "@/lib/utils";
import { MarkdownInline } from "./Markdown";

export interface LeadImageProps {
  /** `Article.lead_image_url`. Never `infobox.image` — there is no such field. */
  url: string;
  alt: string;
  caption: string;
  credit: string;
  license: string;
  sourceUrl: string;
  /**
   * `"infobox"` renders the image cell's contents; `"figure"` renders a
   * right-floated `<figure>` for an article with no infobox.
   */
  variant?: "infobox" | "figure";
  /**
   * The lead image of an article is the LCP element, so it loads eagerly at high
   * priority. Everything else is lazy.
   */
  priority?: boolean;
  /** Footnote source id, because a caption may carry `[^refkey]`. */
  sourceId?: string;
}

/**
 * The lead image, its caption, and its CREDIT LINE.
 *
 * The lead image lives on `Article` columns and never inside `infobox`
 * (DECISIONS §1). The credit line renders whenever `lead_image_credit` is
 * non-empty, and that is not a styling nicety — it is the attribution
 * requirement for CC-licensed media, which is why it is a hard condition in the
 * component rather than a prop a call site can forget.
 *
 * `alt` describes the subject and is never a copy of the caption: a screen
 * reader reads both, and hearing the same sentence twice is worse than hearing
 * nothing.
 */
export function LeadImage({
  url,
  alt,
  caption,
  credit,
  license,
  sourceUrl,
  variant = "infobox",
  priority = false,
  sourceId,
}: LeadImageProps) {
  if (!url) return null;

  const img = (
    <img
      src={url}
      alt={alt}
      className={cn(
        "mx-auto block h-auto max-w-full border border-rule-hair",
        variant === "infobox" && "w-[250px]",
      )}
      loading={priority ? "eager" : "lazy"}
      fetchPriority={priority ? "high" : undefined}
      decoding="async"
    />
  );

  const creditLine = credit ? (
    <div className="pt-[0.3em] text-[0.8em] leading-snug text-ink-3">
      {sourceUrl ? (
        <a className="external" href={sourceUrl} target="_blank" rel="noreferrer noopener">
          {credit}
        </a>
      ) : (
        credit
      )}
      {license ? <> &middot; {license}</> : null}
    </div>
  ) : null;

  if (variant === "figure") {
    return (
      <figure className="thumb-right">
        {img}
        {caption || creditLine ? (
          <figcaption>
            {caption ? <MarkdownInline content={caption} sourceId={sourceId} /> : null}
            {creditLine}
          </figcaption>
        ) : null}
      </figure>
    );
  }

  return (
    <>
      {img}
      {caption ? (
        <div className="infobox-caption pt-[0.35em] text-center text-[0.88em] leading-snug text-ink-2">
          <MarkdownInline content={caption} sourceId={sourceId} />
        </div>
      ) : null}
      {creditLine ? <div className="text-center">{creditLine}</div> : null}
    </>
  );
}
