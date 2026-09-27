import { type ReactNode, useMemo } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import { Link } from "react-router-dom";
import rehypeHighlight from "rehype-highlight";
import type { PluggableList } from "unified";
import remarkGfm from "remark-gfm";

import { cn } from "@/lib/utils";
import { FootnoteMarker } from "./Footnote";
import { WikiLink } from "./WikiLink";
import { remarkWikiverse, useFootnoteScope, type RemarkWikiverseOptions } from "./markdownUtils";

/* =====================================================================
   THE ONE RULE OF THIS FILE
   =====================================================================
   `react-markdown` runs WITHOUT `rehype-raw` and WITH `skipHtml` — for article
   bodies, talk messages, infobox values and reference titles alike (DECISIONS
   §0.5). Raw HTML in a body is dropped, not rendered.

   `dangerouslySetInnerHTML` appears nowhere in this app, and there is no
   exception (DECISIONS §0.4). Search highlighting is built from React elements
   by splitting on literal `<mark>` tokens; citations, infobox values and talk
   posts all come back through here.
   ===================================================================== */

export interface MarkdownProps {
  content: string;
  /**
   * Identifies this string inside the article's footnote allocation, so a
   * `[^ref]` in an infobox row and one in the body get different marker ids.
   * Omit it outside an article.
   */
  sourceId?: string;
  /** Give `##`–`####` stable ids and a hover `#` permalink. On by default. */
  headings?: boolean;
  /** Mark the first top-level paragraph `.lead`. */
  lead?: boolean;
  /** The wrapper's classes. `null` renders no wrapper at all. */
  className?: string | null;
}

/**
 * Markdown inside a `.article-prose` wrapper.
 *
 * This is the shape every non-article surface wants — talk messages, the editor
 * preview, main-page blocks — because the `em`-based type cascade in `index.css`
 * only applies to descendants of `.article-prose`.
 */
export function Markdown({ className = "article-prose", ...rest }: MarkdownProps) {
  if (className === null) return <MarkdownFlow {...rest} />;
  return (
    <div className={cn(className)}>
      <MarkdownFlow {...rest} />
    </div>
  );
}

/**
 * Markdown with NO wrapper element.
 *
 * The article page owns its own `.article-prose` container so that the infobox,
 * hatnotes, the reference list and the category bar are DIRECT children of it
 * alongside the body — which is what `index.css`'s `.article-prose > .infobox`,
 * `> .hatnote`, `> .reflist` and `> .catbar` selectors require, and what lets
 * the floated infobox interleave with the prose instead of sitting above it.
 */
export function MarkdownFlow({
  content,
  sourceId,
  headings = true,
  lead = false,
}: Omit<MarkdownProps, "className">) {
  const { offsets } = useFootnoteScope();
  const footnoteOffsets = sourceId === undefined ? undefined : offsets[sourceId];

  const remarkPlugins = useMarkdownPlugins({ footnoteOffsets, headingIds: headings, lead });

  return (
    <ReactMarkdown
      skipHtml
      remarkPlugins={remarkPlugins}
      rehypePlugins={REHYPE_PLUGINS}
      components={BLOCK_COMPONENTS}
    >
      {content}
    </ReactMarkdown>
  );
}

export interface MarkdownInlineProps {
  content: string;
  sourceId?: string;
  /**
   * Render link text without the link. Used for reference titles, which are
   * already wrapped in an anchor — an anchor inside an anchor is invalid HTML
   * and unreachable by keyboard.
   */
  plainLinks?: boolean;
}

/**
 * Markdown with the block level removed: no `<p>`, no headings, no lists.
 *
 * This is what an infobox value and a reference title are — a string that may
 * carry `[[wikilinks]]`, `*emphasis*` and `[^refkey]` markers (DECISIONS §1),
 * and must not become a paragraph inside a table cell.
 */
export function MarkdownInline({ content, sourceId, plainLinks = false }: MarkdownInlineProps) {
  const { offsets } = useFootnoteScope();
  const footnoteOffsets = sourceId === undefined ? undefined : offsets[sourceId];

  const remarkPlugins = useMarkdownPlugins({ footnoteOffsets, headingIds: false, lead: false });
  const components = plainLinks ? INLINE_PLAIN_COMPONENTS : INLINE_COMPONENTS;

  return (
    <ReactMarkdown skipHtml remarkPlugins={remarkPlugins} components={components}>
      {content}
    </ReactMarkdown>
  );
}

/* =====================================================================
   Plugins
   ===================================================================== */

const REHYPE_PLUGINS = [rehypeHighlight];

/**
 * `remarkWikiverse` is passed as a tuple so unified calls it as an attacher.
 * Memoised because react-markdown rebuilds its whole pipeline whenever the
 * plugin list is a new array — which, for a 40KB article body, is a real cost.
 */
function useMarkdownPlugins(options: RemarkWikiverseOptions): PluggableList {
  const { footnoteOffsets, headingIds, lead } = options;
  return useMemo<PluggableList>(
    () => [remarkGfm, [remarkWikiverse, { footnoteOffsets, headingIds, lead }]],
    [footnoteOffsets, headingIds, lead],
  );
}

/* =====================================================================
   Components
   =====================================================================
   `node.properties` is the HAST element, before React prop conversion, so the
   `data-` attributes `remarkWikiverse` stamped on are read back verbatim.
   Real tag names (`a`, `sup`) are reused rather than invented ones, because
   `Components` is keyed on `ElementType` and a custom key would need a cast.
   ===================================================================== */

function stringProp(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

/**
 * Anchors, in five kinds — and four of them are not router navigations.
 *
 * A `#fragment` href must stay a plain `<a>`: routing it pushes a history entry
 * instead of jumping, which is the defect this replaces. So must a
 * protocol-relative `//host` href, which is external however much it looks like
 * a path.
 */
const Anchor: NonNullable<Components["a"]> = ({ node, href, children, className, ...rest }) => {
  const properties = node?.properties ?? {};

  const wikiTitle = stringProp(properties.dataWikilink);
  if (wikiTitle !== undefined) {
    return (
      <WikiLink
        title={wikiTitle}
        anchor={stringProp(properties.dataWikiAnchor)}
        className={className}
      >
        {children}
      </WikiLink>
    );
  }

  if (href === undefined || href === "") {
    return <span className={className}>{children}</span>;
  }

  // In-page jump: the browser's own, offset by `scroll-padding-top`.
  if (href.startsWith("#")) {
    return (
      <a href={href} className={className} {...rest}>
        {children}
      </a>
    );
  }

  if (href.startsWith("/") && !href.startsWith("//")) {
    return (
      <Link to={href} className={className} {...rest}>
        {children}
      </Link>
    );
  }

  return (
    <a
      href={href}
      className={cn("external", className)}
      target="_blank"
      rel="noreferrer noopener"
      {...rest}
    >
      {children}
    </a>
  );
};

/** `<sup>` is either a footnote marker or ordinary superscript. */
const Superscript: NonNullable<Components["sup"]> = ({ node, children, ...rest }) => {
  const properties = node?.properties ?? {};
  const refKey = stringProp(properties.dataFootnote);
  if (refKey !== undefined) {
    const index = Number.parseInt(String(properties.dataFootnoteIndex ?? "0"), 10);
    return <FootnoteMarker refKey={refKey} index={Number.isNaN(index) ? 0 : index} />;
  }
  return <sup {...rest}>{children}</sup>;
};

/**
 * The hover `#` permalink beside a heading — our addition over Vector, hidden
 * below `shelf` by `index.css` and revealed on hover or keyboard focus.
 */
function headingAnchor(id: string | undefined, children: ReactNode) {
  if (id === undefined) return children;
  return (
    <>
      {children}
      <a className="heading-anchor" href={`#${id}`} aria-label="Permanent link to this section">
        #
      </a>
    </>
  );
}

const BLOCK_COMPONENTS: Components = {
  a: Anchor,
  sup: Superscript,
  // `h1` in a body would duplicate the page title (DECISIONS §19 forbids it in
  // the corpus); if one slips in it is demoted to an `h2` so heading order in
  // the document stays legal.
  h1: ({ children, id }) => <h2 id={id}>{headingAnchor(id, children)}</h2>,
  h2: ({ children, id }) => <h2 id={id}>{headingAnchor(id, children)}</h2>,
  h3: ({ children, id }) => <h3 id={id}>{headingAnchor(id, children)}</h3>,
  h4: ({ children, id }) => <h4 id={id}>{headingAnchor(id, children)}</h4>,
  img: ({ src, alt, title }) => (
    <img src={typeof src === "string" ? src : undefined} alt={alt ?? ""} title={title} loading="lazy" decoding="async" />
  ),
};

const INLINE_COMPONENTS: Components = {
  ...BLOCK_COMPONENTS,
  // An infobox value is a table cell's content, not a paragraph.
  p: ({ children }) => <>{children}</>,
};

const INLINE_PLAIN_COMPONENTS: Components = {
  ...INLINE_COMPONENTS,
  a: ({ children }) => <>{children}</>,
};
