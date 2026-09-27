/**
 * The article module's non-component layer.
 *
 * Everything here is deliberately free of JSX so the file exports no
 * components: `react-refresh/only-export-components` warns on a non-component
 * export from a file that also exports a component, and the lint gate runs with
 * `--max-warnings=0` (DECISIONS §18 — the same reason `buttonVariants` lives in
 * its own module).
 *
 * What lives here:
 *   1. Slugs — `wikiSlug` mirrors the backend's `wiki_slug`, so `[[Title]]`
 *      resolves to the same `/wiki/<slug>` the server assigned.
 *   2. Headings — extraction, stable ids, and the numbered tree the TOC renders.
 *   3. Footnotes — citation numbers and per-source marker allocation.
 *   4. Link resolution — the context that decides blue vs RED.
 *   5. `remarkWikiverse` — the one transform that turns `[[wikilinks]]` and
 *      `[^refkey]` markers into elements BEFORE react-markdown sees them.
 *   6. Citation identifier sniffing (`doi:` / `ISBN` / `arXiv:`).
 *   7. Programmatic anchor jumps (there is no `scroll-behavior: smooth`).
 *   8. The Page-Previews hover state machine.
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";

import { usePreviewCard, useWantedPages } from "@/api/articles";
import type { ArticleExtras, ArticleLinkTarget } from "@/api/articles";
import type { PreviewCard, Reference } from "@/lib/types";
import { scrollBehavior } from "@/lib/utils";

/* =====================================================================
   1. Slugs
   =====================================================================
   `wikiSlug` is the TypeScript twin of `apps/common/utils.py: wiki_slug`.
   If the two ever disagree, every `[[wikilink]]` in the corpus resolves to a
   red link, so the mapping is reproduced literally rather than approximated:
   symbol map first, then Django's `slugify(allow_unicode=True)`, then the
   220-character cap.
   ===================================================================== */

/** `apps/common/utils.py: SYMBOL_MAP`, character for character. */
const SYMBOL_MAP: ReadonlyArray<readonly [string, string]> = [
  ["+", "-plus"],
  ["#", "-sharp"],
  ["&", "-and"],
  ["/", "-"],
  ["@", "-at"],
  ["%", "-percent"],
  ["°", "-degrees"],
  ["½", "one-half"],
  ["π", "pi"],
  ["Ω", "omega"],
  ["Σ", "sigma"],
  ["∞", "infinity"],
  ["√", "sqrt"],
];

const MAX_SLUG_LENGTH = 220;

/**
 * Slugify a wiki title exactly as the backend does.
 *
 * Django's `slugify(value, allow_unicode=True)` is
 * `NFKC` → lowercase → drop everything that is not `\w`, whitespace or `-`
 * → collapse `[-\s]+` to one `-` → strip `-_` from both ends. Python's `\w`
 * under Unicode is letters, digits, marks and `_`, which is what the character
 * class below spells out.
 */
export function wikiSlug(title: string): string {
  let text = (title ?? "").trim();
  for (const [symbol, replacement] of SYMBOL_MAP) {
    if (text.includes(symbol)) text = text.split(symbol).join(replacement);
  }
  text = text
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\p{M}_\s-]/gu, "");
  const slug = text
    .replace(/[-\s]+/g, "-")
    .replace(/^[-_]+/, "")
    .replace(/[-_]+$/, "");
  return slug.slice(0, MAX_SLUG_LENGTH).replace(/^-+/, "").replace(/-+$/, "");
}

/**
 * The id a heading gets, and therefore the id the TOC and every `#section`
 * link target. Plain ASCII-ish and lowercase, because these end up in URLs
 * that people paste into chat.
 */
export function slugifyHeading(text: string): string {
  const slug = (text ?? "")
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-{2,}/g, "-")
    .replace(/^-+/, "")
    .replace(/-+$/, "");
  return slug || "section";
}

/**
 * A slugger that never repeats itself: the second "History" on a page becomes
 * `history-2`.
 *
 * The renderer and the table of contents each create a fresh slugger and walk
 * the same headings in the same order, so they arrive at the same ids without
 * sharing state — which is what lets the TOC be rendered in a different column,
 * at a different time, from a different component.
 */
export function createSlugger(): (text: string) => string {
  const seen = new Map<string, number>();
  return (text: string) => {
    const base = slugifyHeading(text);
    const used = seen.get(base);
    if (used === undefined) {
      seen.set(base, 1);
      return base;
    }
    let n = used + 1;
    while (seen.has(`${base}-${n}`)) n += 1;
    seen.set(base, n);
    seen.set(`${base}-${n}`, 1);
    return `${base}-${n}`;
  };
}

/* =====================================================================
   2. Headings
   ===================================================================== */

export type HeadingLevel = 2 | 3 | 4;

export interface Heading {
  id: string;
  text: string;
  level: HeadingLevel;
  /** `"1"`, `"1.2"`, `"1.2.3"` — the numbers Vector prints in its TOC. */
  number: string;
}

/** A heading plus its subsections, which is what the rail actually renders. */
export interface HeadingNode extends Heading {
  children: HeadingNode[];
}

/** Vector's own threshold: above this, subsections start collapsed. */
export const TOC_AUTO_COLLAPSE_ABOVE = 28;

/**
 * Turn inline Markdown into the plain text a heading id is derived from.
 *
 * It must agree with `mdastToText` below, because one runs on raw lines (here)
 * and the other on the parsed tree (in the renderer), and the ids they produce
 * have to match character for character.
 */
export function inlineToPlainText(markdown: string): string {
  return (markdown ?? "")
    .replace(/\[\[([^\]|]+)\|([^\]]*)\]\]/g, (_m, target: string, display: string) =>
      display.trim() || target.split("#")[0],
    )
    .replace(/\[\[([^\]|]+)\]\]/g, (_m, target: string) => target.split("#")[0])
    .replace(/\[\^[A-Za-z0-9][\w.:-]*\]/g, "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]*)\]\[[^\]]*\]/g, "$1")
    .replace(/`+/g, "")
    .replace(/\*\*|__/g, "")
    .replace(/[*_]/g, "")
    .replace(/~~/g, "")
    .replace(/\\([\\`*_{}[\]()#+\-.!>|~^])/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * Extract `##`–`####` headings from a Markdown body, ignoring fenced code.
 *
 * `#` is not extracted on purpose: a body H1 would duplicate the page title,
 * which is why DECISIONS §19 forbids it in the corpus. If one appears anyway it
 * is simply not in the contents — the renderer still gives it an id.
 */
export function extractHeadings(markdown: string): Heading[] {
  const slug = createSlugger();
  const headings: Heading[] = [];
  const counters = [0, 0, 0];
  let fence: string | null = null;

  for (const rawLine of (markdown ?? "").split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    const fenceMatch = /^[ \t]{0,3}(`{3,}|~{3,})/.exec(line);
    if (fenceMatch) {
      const marker = fenceMatch[1];
      if (fence === null) {
        fence = marker[0];
        continue;
      }
      if (marker[0] === fence && line.trim().split("").every((c) => c === fence)) {
        fence = null;
        continue;
      }
      continue;
    }
    if (fence !== null) continue;

    const match = /^[ \t]{0,3}(#{2,4})[ \t]+(.+?)[ \t]*#*[ \t]*$/.exec(line);
    if (!match) continue;

    const level = match[1].length as HeadingLevel;
    const text = inlineToPlainText(match[2]);
    if (!text) continue;

    const depth = level - 2;
    counters[depth] += 1;
    for (let deeper = depth + 1; deeper < counters.length; deeper += 1) counters[deeper] = 0;

    headings.push({
      id: slug(text),
      text,
      level,
      number: counters.slice(0, depth + 1).join("."),
    });
  }

  return headings;
}

/**
 * Split a body into the LEAD and everything after it.
 *
 * The lead is the unsectioned summary between the title block and the first
 * `h2` (MOS: it has no heading of its own and opens by restating the title in
 * bold). Splitting is what lets the mobile contents disclosure sit between the
 * lead and the first section — in the reading order, which is where Wikipedia
 * puts it — without a second prose container: both halves render as direct
 * children of the same `.article-prose`, so every `>` selector still matches.
 */
export function splitLead(markdown: string): { lead: string; body: string } {
  const lines = (markdown ?? "").split("\n");
  let fence: string | null = null;

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index].replace(/\r$/, "");
    const fenceMatch = /^[ \t]{0,3}(`{3,}|~{3,})/.exec(line);
    if (fenceMatch) {
      const marker = fenceMatch[1][0];
      if (fence === null) fence = marker;
      else if (marker === fence) fence = null;
      continue;
    }
    if (fence !== null) continue;
    if (/^[ \t]{0,3}#{1,6}[ \t]+/.test(line)) {
      return {
        lead: lines.slice(0, index).join("\n").trim(),
        body: lines.slice(index).join("\n"),
      };
    }
  }

  return { lead: (markdown ?? "").trim(), body: "" };
}

/** Nest a flat heading list by level. A skipped level is simply not nested. */
export function buildHeadingTree(headings: Heading[]): HeadingNode[] {
  const roots: HeadingNode[] = [];
  const stack: HeadingNode[] = [];

  for (const heading of headings) {
    const node: HeadingNode = { ...heading, children: [] };
    while (stack.length > 0 && stack[stack.length - 1].level >= node.level) stack.pop();
    if (stack.length === 0) roots.push(node);
    else stack[stack.length - 1].children.push(node);
    stack.push(node);
  }

  return roots;
}

/* =====================================================================
   3. Footnotes
   =====================================================================
   Two numbers per marker, and they are not the same number:

     * the CITATION NUMBER, printed in the brackets, is the reference's
       1-based position in `references` — every `[^curie1903]` on the page
       prints the same one;
     * the OCCURRENCE INDEX `n` in `cite_ref-{key}-{n}` (DECISIONS §14) counts
       markers, so the reference list can back-link to each of them as
       `^ a b c`.

   `n` is allocated ahead of render, per source string, by
   `buildFootnoteScope`. It is deliberately NOT a counter incremented during
   render: React renders a tree twice in StrictMode, and a render-time counter
   would silently double every id.
   ===================================================================== */

/** `{key: number of in-text markers}`, in first-appearance order. */
export function countFootnoteMarkers(markdown: string): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const run of textRuns(markdown ?? "")) {
    for (const match of run.matchAll(FOOTNOTE_RE)) {
      const key = match[1];
      counts[key] = (counts[key] ?? 0) + 1;
    }
  }
  return counts;
}

/** One Markdown string that may contain footnote markers. */
export interface FootnoteSource {
  /** Stable identity for the string, e.g. `"content"` or `"infobox.row.3"`. */
  id: string;
  text: string;
}

export interface FootnoteScope {
  /** `key` → 1-based citation number. Absent means "no such reference". */
  numbers: Readonly<Record<string, number>>;
  /** `key` → how many markers cite it across the whole article. */
  totals: Readonly<Record<string, number>>;
  /** `sourceId` → `key` → the `n` the first marker in that source takes. */
  offsets: Readonly<Record<string, Readonly<Record<string, number>>>>;
}

const EMPTY_FOOTNOTE_SCOPE: FootnoteScope = { numbers: {}, totals: {}, offsets: {} };

/**
 * Allocate citation numbers and marker indices for one article.
 *
 * `sources` must be listed in DOM order — infobox values first, then the lead
 * image caption, then the body — because that is the order a reader meets the
 * markers and therefore the order the `^ a b c` backlinks have to follow.
 */
export function buildFootnoteScope(
  references: readonly Reference[],
  sources: readonly FootnoteSource[],
): FootnoteScope {
  const numbers: Record<string, number> = {};
  const ordered = [...references].sort((a, b) => a.order - b.order);
  ordered.forEach((reference, index) => {
    numbers[reference.key] = index + 1;
  });

  const totals: Record<string, number> = {};
  const offsets: Record<string, Record<string, number>> = {};

  for (const source of sources) {
    const counts = countFootnoteMarkers(source.text);
    const offset: Record<string, number> = {};
    for (const [key, count] of Object.entries(counts)) {
      offset[key] = totals[key] ?? 0;
      totals[key] = (totals[key] ?? 0) + count;
    }
    offsets[source.id] = offset;
  }

  return { numbers, totals, offsets };
}

export const FootnoteContext = createContext<FootnoteScope>(EMPTY_FOOTNOTE_SCOPE);

/** The article's footnote allocation. Empty outside an article. */
export function useFootnoteScope(): FootnoteScope {
  return useContext(FootnoteContext);
}

/** `cite_note-{key}` (DECISIONS §14). */
export function citeNoteId(key: string): string {
  return `cite_note-${key}`;
}

/** `cite_ref-{key}-{n}` (DECISIONS §14). `n` is 0-based. */
export function citeRefId(key: string, n: number): string {
  return `cite_ref-${key}-${n}`;
}

/** `a`, `b`, … `z`, `aa` — the letters on a multi-cited reference's backlinks. */
export function backlinkLetter(n: number): string {
  let index = n;
  let out = "";
  do {
    out = String.fromCharCode(97 + (index % 26)) + out;
    index = Math.floor(index / 26) - 1;
  } while (index >= 0);
  return out;
}

/* =====================================================================
   4. Link resolution — blue or RED
   =====================================================================
   RED LINKS are a product decision, not a defect (DECISIONS §19): the corpus
   ships 63 of 120 planned articles, so a large minority of `[[links]]` point at
   titles nobody has written yet. They must render red, carry a "page does not
   exist" title and point at `/new?title=<Title>`.

   Resolution is a page-level lookup, never a request per link. See
   `useArticleLinkResolver` in `@/api/articles` for where the data comes from.
   ===================================================================== */

export interface ResolvedLink {
  /** The slug the target would have, whether or not it exists. */
  slug: string;
  /**
   * `true` the article exists, `false` it is a red link, `undefined` unknown —
   * and unknown renders BLUE, because inventing a red link is worse than
   * missing one.
   */
  exists: boolean | undefined;
}

export type LinkResolver = (title: string) => ResolvedLink;

/** The fallback resolver: slug only, existence unknown. */
export const optimisticResolver: LinkResolver = (title) => ({
  slug: wikiSlug(title),
  exists: undefined,
});

export const LinkResolutionContext = createContext<LinkResolver>(optimisticResolver);

export function useLinkResolution(): LinkResolver {
  return useContext(LinkResolutionContext);
}

/**
 * Build the resolver for one article.
 *
 * TWO SOURCES, in priority order, and both are page-level:
 *
 *  1. `article.links` — the `ArticleLink` rows for this body, resolved
 *     server-side in the same query as the article. Authoritative: it knows
 *     exactly which of THIS page's links are red. The serializer does not emit
 *     it yet; the moment it does, this branch takes over with no other change.
 *
 *  2. `GET /api/wanted/` — every red-link target in the corpus, ranked by
 *     inbound count, one cached request for the whole session. A target in that
 *     set is definitively red, because the endpoint is literally
 *     `ArticleLink.objects.filter(to_article__isnull=True)`. A target absent
 *     from it is reported as UNKNOWN, not as existing, and unknown renders
 *     blue — so the failure mode is a missing red link, never a false one.
 *
 * Neither branch ever issues a request per link.
 */
export function useArticleLinkResolver(article: ArticleExtras | undefined): LinkResolver {
  const links = article?.links;
  const { data: wanted } = useWantedPages(links === undefined);

  return useMemo<LinkResolver>(() => {
    if (links !== undefined) {
      const byTitle = new Map<string, ArticleLinkTarget>();
      const bySlug = new Map<string, ArticleLinkTarget>();
      for (const link of links) {
        byTitle.set(link.to_title.toLowerCase(), link);
        bySlug.set(link.to_slug, link);
      }
      return (title) => {
        const slug = wikiSlug(title);
        const hit = byTitle.get(title.toLowerCase()) ?? bySlug.get(slug);
        return { slug: hit?.to_slug || slug, exists: hit?.exists };
      };
    }

    if (wanted) {
      const red = new Set(wanted.results.map((row) => row.slug));
      return (title) => {
        const slug = wikiSlug(title);
        return { slug, exists: red.has(slug) ? false : undefined };
      };
    }

    return optimisticResolver;
  }, [links, wanted]);
}

/** `/new?title=<Title>` (DECISIONS §14). The title, not the slug. */
export function createPageHref(title: string): string {
  return `/new?title=${encodeURIComponent(title)}`;
}

/** The `title` attribute a red link carries, so a hover explains the colour. */
export function redLinkTitle(title: string): string {
  return `${title} (page does not exist)`;
}

/** `[[Target#Anchor|display]]` split into its three parts. */
export interface WikiTarget {
  title: string;
  anchor: string;
  display: string;
}

export function parseWikiTarget(raw: string): WikiTarget | null {
  const [targetPart, displayPart] = splitOnce(raw, "|");
  const target = collapse(targetPart);
  if (!target) return null;

  const [titlePart, anchorPart] = splitOnce(target, "#");
  const title = collapse(titlePart);
  if (!title) return null;

  const anchor = collapse(anchorPart ?? "");
  const display = collapse(displayPart ?? "") || (anchor ? target : title);

  return { title, anchor, display };
}

/** `/wiki/<slug>` plus the section anchor, if the link carried one. */
export function wikiHref(slug: string, anchor?: string): string {
  return anchor ? `/wiki/${slug}#${slugifyHeading(anchor)}` : `/wiki/${slug}`;
}

function splitOnce(value: string, separator: string): [string, string | undefined] {
  const at = value.indexOf(separator);
  if (at === -1) return [value, undefined];
  return [value.slice(0, at), value.slice(at + separator.length)];
}

function collapse(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

/* =====================================================================
   5. remarkWikiverse
   =====================================================================
   HOW CODE IS KEPT SAFE, which is the whole reason this is a remark plugin
   rather than a string pre-pass:

   The transform runs on the parsed mdast tree and only ever reads nodes whose
   `type` is exactly `"text"`. A fenced block is a `code` node and an inline
   span is an `inlineCode` node; both carry their contents in `value`, and
   NEITHER IS EVER OF TYPE `"text"`. So a `[[wikilink]]` or a `[^ref]` inside
   backticks is not merely skipped by a rule that could be got wrong — it is
   structurally invisible to the visitor. No regex ever touches code.

   Two further guards:
     * `SKIP_PARENTS` stops the visitor descending into link labels, image alt
       text and definitions, so no anchor is ever nested inside another.
     * consecutive `text` siblings are merged before matching, so a marker that
       the parser happened to split across two text nodes is still seen.

   Escapes: where the merged run's length matches its source span exactly, the
   original Markdown is consulted so `\[[not a link]]` stays literal — the same
   rule the backend's `markup.py` applies.
   ===================================================================== */

/** The minimal mdast surface this plugin needs. Structural, so no `mdast` import. */
interface MdNode {
  type: string;
  value?: string;
  children?: MdNode[];
  depth?: number;
  data?: MdData;
  position?: { start?: { offset?: number }; end?: { offset?: number } };
}

interface MdData {
  hName?: string;
  hProperties?: Record<string, unknown>;
}

const WIKILINK_RE = /\[\[([^[\]|\n]{1,200}?)(?:\|([^[\]\n]{0,200}?))?\]\]/g;
const FOOTNOTE_RE = /\[\^([A-Za-z0-9][A-Za-z0-9_.:-]{0,60})\]/g;

/** Never descend into these: their text is a label, not prose. */
const SKIP_PARENTS = new Set([
  "code",
  "inlineCode",
  "html",
  "link",
  "linkReference",
  "image",
  "imageReference",
  "definition",
  "footnoteDefinition",
  "footnoteReference",
  "yaml",
  "toml",
  // Nodes this plugin produced: their children are already final.
  "wikilink",
  "footnoteMarker",
]);

export interface RemarkWikiverseOptions {
  /** `key` → the `n` the first marker in THIS source takes. */
  footnoteOffsets?: Readonly<Record<string, number>>;
  /** Give `##`–`####` stable ids. Off for infobox values and talk messages. */
  headingIds?: boolean;
  /** Mark the first top-level paragraph `.lead`. */
  lead?: boolean;
}

/**
 * The single Markdown transform: wikilinks, footnote markers, heading ids and
 * the lead paragraph.
 *
 * Emitted nodes reuse real tag names (`a` and `sup`) with `data-` attributes
 * rather than inventing element names, because react-markdown's `components`
 * map is typed over `JSX.IntrinsicElements` and a custom key would need a cast.
 */
export function remarkWikiverse(options: RemarkWikiverseOptions = {}) {
  const { footnoteOffsets = {}, headingIds = true, lead = false } = options;

  return function transform(tree: MdNode, file: unknown): void {
    const source = typeof file === "undefined" || file === null ? "" : String(file);
    const used: Record<string, number> = {};
    const slug = createSlugger();
    let leadDone = !lead;

    function nextFootnoteIndex(key: string): number {
      const local = used[key] ?? 0;
      used[key] = local + 1;
      return (footnoteOffsets[key] ?? 0) + local;
    }

    function walk(node: MdNode, isTopLevel: boolean, root: MdNode): void {
      if (headingIds && node.type === "heading" && typeof node.depth === "number") {
        const id = slug(mdastToText(node));
        node.data = node.data ?? {};
        node.data.hProperties = { ...(node.data.hProperties ?? {}), id };
      }

      if (!leadDone && isTopLevel && node.type === "paragraph") {
        node.data = node.data ?? {};
        node.data.hProperties = { ...(node.data.hProperties ?? {}), className: ["lead"] };
        leadDone = true;
      }

      const children = node.children;
      if (!children || children.length === 0) return;
      if (SKIP_PARENTS.has(node.type)) return;

      node.children = expandTextRuns(children, source, nextFootnoteIndex);
      // Children of the root are the top level: that is where `.lead` may land.
      for (const child of node.children) walk(child, node === root, root);
    }

    // ONE traversal. Walking the tree twice would re-slug every heading (giving
    // `history-2` where `history` was expected) and desynchronise the ids from
    // the ones `extractHeadings` hands the table of contents.
    walk(tree, false, tree);
  };
}

/**
 * Replace runs of consecutive `text` siblings with the same text plus any
 * wikilink / footnote elements they contained.
 */
function expandTextRuns(
  children: MdNode[],
  source: string,
  nextFootnoteIndex: (key: string) => number,
): MdNode[] {
  if (!children.some((child) => child.type === "text")) return children;

  const out: MdNode[] = [];
  let run: MdNode[] = [];

  const flush = () => {
    if (run.length === 0) return;
    const value = run.map((node) => node.value ?? "").join("");
    const start = run[0].position?.start?.offset;
    const end = run[run.length - 1].position?.end?.offset;
    const escaped =
      typeof start === "number" && typeof end === "number"
        ? escapedPositions(source.slice(start, end), value)
        : EMPTY_POSITIONS;
    out.push(...transformText(value, escaped, nextFootnoteIndex));
    run = [];
  };

  for (const child of children) {
    if (child.type === "text") {
      run.push(child);
      continue;
    }
    flush();
    out.push(child);
  }
  flush();

  return out;
}

/** Split one text value into text / wikilink / footnote nodes. */
function transformText(
  value: string,
  escaped: ReadonlySet<number>,
  nextFootnoteIndex: (key: string) => number,
): MdNode[] {
  const marks: { start: number; end: number; node: MdNode }[] = [];

  WIKILINK_RE.lastIndex = 0;
  for (let m = WIKILINK_RE.exec(value); m !== null; m = WIKILINK_RE.exec(value)) {
    if (escaped.has(m.index)) continue;
    const raw = m[2] === undefined ? m[1] : `${m[1]}|${m[2]}`;
    const target = parseWikiTarget(raw);
    if (!target) continue;
    marks.push({ start: m.index, end: m.index + m[0].length, node: wikilinkNode(target) });
  }

  FOOTNOTE_RE.lastIndex = 0;
  for (let m = FOOTNOTE_RE.exec(value); m !== null; m = FOOTNOTE_RE.exec(value)) {
    if (escaped.has(m.index)) continue;
    if (value[m.index + m[0].length] === ":") continue; // a definition, not a citation
    if (marks.some((mark) => m.index < mark.end && mark.start < m.index + m[0].length)) continue;
    marks.push({ start: m.index, end: m.index + m[0].length, node: footnoteNode(m[1], 0) });
  }

  if (marks.length === 0) return [{ type: "text", value }];

  marks.sort((a, b) => a.start - b.start);

  const out: MdNode[] = [];
  let cursor = 0;
  for (const mark of marks) {
    if (mark.start < cursor) continue;
    if (mark.start > cursor) out.push({ type: "text", value: value.slice(cursor, mark.start) });
    // Footnote indices are claimed here, in document order, not at match time:
    // the two regex passes above run out of order.
    const key = mark.node.data?.hProperties?.["dataFootnote"];
    if (typeof key === "string") {
      mark.node.data!.hProperties!["dataFootnoteIndex"] = String(nextFootnoteIndex(key));
    }
    out.push(mark.node);
    cursor = mark.end;
  }
  if (cursor < value.length) out.push({ type: "text", value: value.slice(cursor) });

  return out;
}

function wikilinkNode(target: WikiTarget): MdNode {
  return {
    type: "wikilink",
    data: {
      hName: "a",
      hProperties: {
        dataWikilink: target.title,
        dataWikiAnchor: target.anchor || undefined,
      },
    },
    children: [{ type: "text", value: target.display }],
  };
}

function footnoteNode(key: string, index: number): MdNode {
  return {
    type: "footnoteMarker",
    data: {
      hName: "sup",
      hProperties: { dataFootnote: key, dataFootnoteIndex: String(index) },
    },
    children: [],
  };
}

const EMPTY_POSITIONS: ReadonlySet<number> = new Set<number>();

/**
 * Which offsets in a text node's VALUE were backslash-escaped in the SOURCE.
 *
 * `\[[not a link]]` must stay literal — the same rule the backend's `markup.py`
 * applies — but by the time micromark hands over a text node the backslash is
 * gone, so the value no longer says which `[` was escaped. The two strings
 * differ only by those dropped backslashes, so a two-pointer walk recovers the
 * positions exactly: wherever the source has `\x` and the value has `x`, that
 * position in the value was escaped.
 *
 * Anything else that could make the two diverge (a character reference, say)
 * makes the walk fail to consume both strings, and the function gives up and
 * reports no escapes — honouring the match, which is what the backend does with
 * an ambiguous case too.
 */
function escapedPositions(sourceSlice: string, value: string): ReadonlySet<number> {
  if (!sourceSlice.includes("\\")) return EMPTY_POSITIONS;

  const positions = new Set<number>();
  let source = 0;
  let target = 0;

  while (source < sourceSlice.length && target < value.length) {
    if (
      sourceSlice[source] === "\\" &&
      source + 1 < sourceSlice.length &&
      sourceSlice[source + 1] === value[target]
    ) {
      positions.add(target);
      source += 2;
      target += 1;
      continue;
    }
    if (sourceSlice[source] !== value[target]) return EMPTY_POSITIONS;
    source += 1;
    target += 1;
  }

  if (source !== sourceSlice.length || target !== value.length) return EMPTY_POSITIONS;
  return positions;
}

/** The plain text of an mdast subtree, wikilink display text included. */
function mdastToText(node: MdNode): string {
  if (typeof node.value === "string") return node.value;
  if (!node.children) return "";
  return node.children.map(mdastToText).join("");
}

/**
 * The text of a Markdown string with fenced blocks and inline code blanked.
 *
 * Used only by `countFootnoteMarkers`, which counts markers before anything is
 * parsed. It exists so the count and the render agree about what is code.
 */
function textRuns(markdown: string): string[] {
  const lines = markdown.split("\n");
  const runs: string[] = [];
  let fence: string | null = null;

  for (const rawLine of lines) {
    const line = rawLine.replace(/\r$/, "");
    const fenceMatch = /^[ \t]{0,3}(`{3,}|~{3,})/.exec(line);
    if (fenceMatch) {
      const marker = fenceMatch[1][0];
      if (fence === null) fence = marker;
      else if (marker === fence) fence = null;
      continue;
    }
    if (fence !== null) continue;
    runs.push(stripInlineCode(line));
  }

  return runs;
}

function stripInlineCode(line: string): string {
  let out = "";
  let index = 0;
  while (index < line.length) {
    if (line[index] !== "`") {
      out += line[index];
      index += 1;
      continue;
    }
    const open = /^`+/.exec(line.slice(index))![0];
    const closeAt = line.indexOf(open, index + open.length);
    if (closeAt === -1) {
      out += line.slice(index);
      break;
    }
    out += " ".repeat(closeAt + open.length - index);
    index = closeAt + open.length;
  }
  return out;
}

/* =====================================================================
   6. Citation identifiers
   =====================================================================
   `Reference.identifier` is ONE free-text field holding an ISBN, a DOI or an
   arXiv id (DECISIONS §11), so the label is sniffed from the prefix.
   ===================================================================== */

export type IdentifierKind = "doi" | "isbn" | "arxiv" | "other";

export interface CitationIdentifier {
  kind: IdentifierKind;
  /** `"doi:"`, `"ISBN"`, `"arXiv:"`, or `""`. */
  label: string;
  /** The identifier without its prefix. */
  value: string;
  /** A resolver URL, where one exists. */
  href: string | null;
}

export function parseIdentifier(identifier: string): CitationIdentifier | null {
  const raw = (identifier ?? "").trim();
  if (!raw) return null;

  const doi = /^doi:\s*(\S+)$/i.exec(raw);
  if (doi) {
    return {
      kind: "doi",
      label: "doi:",
      value: doi[1],
      href: `https://doi.org/${encodeURI(doi[1])}`,
    };
  }

  const isbn = /^isbn[:\s]*([\dXx\- ]+)$/i.exec(raw);
  if (isbn) {
    const value = isbn[1].trim();
    return { kind: "isbn", label: "ISBN", value, href: null };
  }

  const arxiv = /^arxiv:\s*(\S+)$/i.exec(raw);
  if (arxiv) {
    return {
      kind: "arxiv",
      label: "arXiv:",
      value: arxiv[1],
      href: `https://arxiv.org/abs/${encodeURI(arxiv[1])}`,
    };
  }

  return { kind: "other", label: "", value: raw, href: null };
}

/* =====================================================================
   7. Anchor jumps
   =====================================================================
   `scroll-behavior: smooth` is deliberately absent from the stylesheet
   (DECISIONS §18) because it fights focus management. Every in-page jump is
   therefore programmatic, offsets itself past the sticky sub-header, and asks
   `scrollBehavior()` which behaviour the reader's motion preference allows.
   ===================================================================== */

/** The sticky sub-header's height plus a 16px breathing gap, in pixels. */
export function anchorOffset(): number {
  if (typeof window === "undefined") return 0;
  const raw = getComputedStyle(document.documentElement).getPropertyValue("--subheader-h");
  const rem = Number.parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
  const value = raw.trim();
  if (value.endsWith("rem")) return Number.parseFloat(value) * rem + 16;
  if (value.endsWith("px")) return Number.parseFloat(value) + 16;
  return 68;
}

/**
 * Scroll an element into the reading band and give it focus.
 *
 * The URL fragment is deliberately NOT written: a `pushState` behind the data
 * router's back desynchronises it, and `:target` does not reliably re-evaluate
 * on `pushState` anyway. The flash class below is what confirms the landing,
 * and it restarts on a second click, which `:target` cannot.
 */
export function jumpToAnchor(id: string, flashClass?: string): void {
  if (typeof document === "undefined") return;
  const el = document.getElementById(id);
  if (!el) return;

  const top = el.getBoundingClientRect().top + window.scrollY - anchorOffset();
  window.scrollTo({ top: Math.max(0, top), behavior: scrollBehavior() });

  if (flashClass) {
    el.classList.remove(flashClass);
    // Force a style recalculation so the animation restarts on a repeat click.
    void el.offsetWidth;
    el.classList.add(flashClass);
  }

  if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
  el.focus({ preventScroll: true });
}

/* =====================================================================
   8. Hover previews — the 150 / 500 / 300 state machine
   =====================================================================
   Values are the Popups extension's own constants (survey-wikipedia.md Part 5):

     150ms dwell  before the request is allowed to fire
     500ms floor  before the card may paint, even if the data arrived at 180ms
     300ms grace  after the pointer leaves, so crossing the gap into the card
                  does not dismiss it

   The 500ms floor is the part that makes it feel right and the part almost
   every clone omits: without it, a reader dragging the pointer across a
   paragraph of six wikilinks gets six flashes.
   ===================================================================== */

const FETCH_START_DELAY = 150;
const SHOW_FLOOR = 500;
const ABANDON_GRACE = 300;

const CARD_WIDTH = 320;
const FLIP_MARGIN = 220;
const VIEWPORT_INSET = 8;

export interface PreviewPosition {
  left: number;
  top: number;
  /** The card was flipped above the trigger; it animates from below instead. */
  flipped: boolean;
}

export interface HoverPreviewState {
  /** Spread onto the trigger element. */
  trigger: {
    ref: (el: HTMLElement | null) => void;
    onPointerEnter: () => void;
    onPointerLeave: () => void;
    onFocus: () => void;
    onBlur: () => void;
    "aria-describedby"?: string;
  };
  /** Spread onto the card, so moving into it keeps it open. */
  card: {
    onPointerEnter: () => void;
    onPointerLeave: () => void;
  };
  id: string;
  open: boolean;
  position: PreviewPosition | null;
  data: PreviewCard | undefined;
}

/**
 * The hover-preview state machine for one wikilink.
 *
 * Suppressed entirely when `enabled` is false — which is every red link (there
 * is nothing to preview) and every touch pointer (a tap goes straight to the
 * article, so a card would be a second thing to dismiss).
 */
export function useHoverPreview(slug: string, enabled: boolean): HoverPreviewState {
  const [armed, setArmed] = useState(false);
  const [floorPassed, setFloorPassed] = useState(false);
  const [position, setPosition] = useState<PreviewPosition | null>(null);

  const triggerRef = useRef<HTMLElement | null>(null);
  const fetchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const floorTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const { data } = usePreviewCard(slug, enabled && armed);

  const clearTimers = useCallback(() => {
    for (const timer of [fetchTimer, floorTimer, hideTimer]) {
      if (timer.current !== null) {
        clearTimeout(timer.current);
        timer.current = null;
      }
    }
  }, []);

  const close = useCallback(() => {
    clearTimers();
    setArmed(false);
    setFloorPassed(false);
    setPosition(null);
  }, [clearTimers]);

  const measure = useCallback(() => {
    const el = triggerRef.current;
    if (!el || typeof window === "undefined") return;
    const rect = el.getBoundingClientRect();
    const flipped = rect.bottom > window.innerHeight - FLIP_MARGIN;
    const maxLeft = Math.max(VIEWPORT_INSET, window.innerWidth - CARD_WIDTH - VIEWPORT_INSET);
    setPosition({
      left: Math.min(Math.max(VIEWPORT_INSET, rect.left), maxLeft),
      top: flipped ? rect.top + window.scrollY : rect.bottom + window.scrollY + 4,
      flipped,
    });
  }, []);

  const begin = useCallback(() => {
    if (!enabled) return;
    if (hideTimer.current !== null) {
      clearTimeout(hideTimer.current);
      hideTimer.current = null;
    }
    if (fetchTimer.current !== null || armed) return;
    fetchTimer.current = setTimeout(() => {
      fetchTimer.current = null;
      setArmed(true);
    }, FETCH_START_DELAY);
    floorTimer.current = setTimeout(() => {
      floorTimer.current = null;
      measure();
      setFloorPassed(true);
    }, SHOW_FLOOR);
  }, [armed, enabled, measure]);

  const abandon = useCallback(() => {
    if (hideTimer.current !== null) clearTimeout(hideTimer.current);
    hideTimer.current = setTimeout(() => {
      hideTimer.current = null;
      close();
    }, ABANDON_GRACE);
  }, [close]);

  // Escape dismisses, and so does any scroll: a card anchored to a rectangle
  // that has moved is worse than no card.
  const open = enabled && floorPassed && Boolean(data);
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
    };
    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("scroll", close, { passive: true });
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("scroll", close);
    };
  }, [close, open]);

  useEffect(() => clearTimers, [clearTimers]);

  const id = `preview-${slug}`;

  return {
    trigger: {
      ref: (el) => {
        triggerRef.current = el;
      },
      onPointerEnter: begin,
      onPointerLeave: abandon,
      onFocus: begin,
      onBlur: close,
      "aria-describedby": open ? id : undefined,
    },
    card: {
      onPointerEnter: () => {
        if (hideTimer.current !== null) {
          clearTimeout(hideTimer.current);
          hideTimer.current = null;
        }
      },
      onPointerLeave: abandon,
    },
    id,
    open,
    position,
    data,
  };
}
