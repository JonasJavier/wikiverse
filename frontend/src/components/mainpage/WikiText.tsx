import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import remarkGfm from "remark-gfm";

import {
  createPageHref,
  optimisticResolver,
  parseWikiTarget,
  redLinkTitle,
  wikiHref,
  type LinkResolver,
} from "@/components/article/markdownUtils";
import { cn } from "@/lib/utils";

/**
 * One line of editorial wiki markup — a Did you know… hook or an On this day
 * event — rendered as React elements.
 *
 * Constraints, all of them hard:
 *  - `react-markdown` WITHOUT `rehype-raw` and WITH `skipHtml`, exactly as for
 *    article bodies, talk messages, infobox values and reference titles
 *    (DECISIONS §0.5). Editorial blocks are database content authored through
 *    the admin, so they are treated as no more trusted than an article body.
 *  - No `dangerouslySetInnerHTML`, here or anywhere (DECISIONS §0.4).
 *  - `[[Target]]` / `[[Target|display]]` resolve to internal links, and a
 *    target the resolver reports as missing renders as a RED link pointing at
 *    `/new?title=<Title>` (DECISIONS §14, §19).
 *
 * Slugging, the red-link href and the red-link title all come from
 * `components/article/markdownUtils`, the same module the article body's
 * `WikiLink` uses, so a hook on the front page and a link inside an article
 * can never disagree about where `[[Erdős number]]` points or about whether it
 * is red.
 *
 * `WikiLink` itself is deliberately NOT used here: it carries a hover preview
 * card and reads its resolver from a context an article page provides. A
 * one-line hook wants the link and nothing else.
 *
 * The wikilink pre-pass rewrites `[[…]]` into an ordinary markdown link whose
 * href is already the final ROOT-RELATIVE route, so the parser does the
 * escaping, the emphasis and the entities, react-markdown's default
 * `urlTransform` still blocks every dangerous scheme (a custom scheme would
 * have had to disable it), and this file only decides what an anchor becomes.
 * A raw `[[Target]]` left in the text would otherwise render as literal
 * brackets.
 */

const WIKILINK = /\[\[([^[\]]+)\]\]/g;
const RED_PREFIX = "/new?title=";

/** The title carried by a red-link href, for its `title` attribute. */
function titleFromRedHref(href: string): string {
  const raw = href.slice(RED_PREFIX.length);
  try {
    return decodeURIComponent(raw);
  } catch {
    return raw;
  }
}

/** Markdown link text may not contain an unescaped bracket. */
function escapeLinkText(text: string): string {
  return text.replace(/([[\]])/g, "\\$1");
}

function toMarkdown(source: string, resolve: LinkResolver): string {
  return source.replace(WIKILINK, (match, raw: string) => {
    const parsed = parseWikiTarget(raw);
    if (!parsed) return match;
    const { slug, exists } = resolve(parsed.title);
    const href =
      exists === false
        ? createPageHref(parsed.title)
        : wikiHref(slug, parsed.anchor || undefined);
    const hint = parsed.title.replace(/"/g, "");
    return `[${escapeLinkText(parsed.display)}](${href} "${hint}")`;
  });
}

interface WikiTextProps {
  /** Markdown, possibly containing `[[wikilinks]]`. */
  children: string;
  /**
   * Existence oracle, from `useArticleLinkResolver`. Absent, every target is
   * unknown and therefore renders blue: a missing red link is a small loss, an
   * invented one is a lie about the corpus.
   */
  resolve?: LinkResolver;
  className?: string;
}

const LINK = "text-link visited:text-link-visited hover:underline";
/** `.is-redlink` is the class DECISIONS §19 names; the token class carries the
 *  colour outside `.article-prose`, where the stylesheet's rule does not reach. */
const RED_LINK = "is-redlink text-link-red hover:underline";

export function WikiText({ children, resolve, className }: WikiTextProps) {
  return (
    <span className={cn("[&_p]:inline", className)}>
      <ReactMarkdown
        skipHtml
        remarkPlugins={[remarkGfm]}
        components={{
          /* A hook is one sentence inside an existing `li`; a block `p` would
             break the bullet's baseline. */
          p: ({ children: content }) => <>{content}</>,
          a: ({ href, children: content, title }) => {
            if (href?.startsWith(RED_PREFIX)) {
              return (
                <Link
                  to={href}
                  title={redLinkTitle(titleFromRedHref(href))}
                  className={RED_LINK}
                >
                  {content}
                </Link>
              );
            }
            if (href?.startsWith("/")) {
              return (
                <Link to={href} title={title} className={LINK}>
                  {content}
                </Link>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noreferrer noopener"
                className={LINK}
              >
                {content}
              </a>
            );
          },
        }}
      >
        {toMarkdown(children, resolve ?? optimisticResolver)}
      </ReactMarkdown>
    </span>
  );
}
