import { ChevronRight } from "lucide-react";
import { type MouseEvent, type ReactNode, useEffect, useMemo, useState } from "react";

import { cn } from "@/lib/utils";
import {
  anchorOffset,
  buildHeadingTree,
  extractHeadings,
  jumpToAnchor,
  TOC_AUTO_COLLAPSE_ABOVE,
  type Heading,
  type HeadingNode,
} from "./markdownUtils";

/** A section the renderer adds after the body — See also, References. */
export interface ExtraSection {
  id: string;
  text: string;
}

const NO_SECTIONS: readonly ExtraSection[] = [];

export interface TableOfContentsProps {
  /** The article's Markdown body. Headings are derived from it, not from the DOM. */
  content: string;
  /** Sections the page appends itself, numbered after the body's own. */
  extraSections?: readonly ExtraSection[];
  /** The id `(Top)` scrolls to. */
  topId?: string;
  className?: string;
}

/**
 * The table of contents, in the left rail.
 *
 * Conventions taken from the measured Vector markup because they are what make
 * a TOC read as an encyclopedia's rather than as a docs site's:
 *   - the first entry is literally `(Top)`, in parentheses;
 *   - section numbers (`1`, `1.2`) sit in their own column and are QUIETER than
 *     the label, not louder;
 *   - level-3 children collapse behind a chevron, and auto-collapse entirely
 *     above 28 sections, which is Vector's own threshold;
 *   - a heading becomes active when it reaches the top reading band, not when it
 *     merely enters the viewport — hence the negative `rootMargin` top (the
 *     sticky sub-header's height) and the `-70%` bottom.
 *
 * Ids come from `extractHeadings`, which runs the same slugger the renderer
 * runs, so the two agree without sharing state — which is what lets this render
 * in a different column, at a different time, from the body.
 */
export function TableOfContents({
  content,
  extraSections = NO_SECTIONS,
  topId = "content",
  className,
}: TableOfContentsProps) {
  const { tree, ids, count } = useContents(content, extraSections);
  const active = useActiveHeading(ids);
  const [shown, setShown] = useState(true);

  if (count < 2) return null;

  return (
    <nav
      id="toc-rail"
      aria-label="Contents"
      className={cn(
        "sticky top-[calc(var(--subheader-h)+1rem)] max-h-[calc(100vh-var(--subheader-h)-2rem)]",
        "overflow-y-auto overscroll-contain font-sans text-ui print:hidden",
        className,
      )}
    >
      <div className="flex items-baseline justify-between border-b border-rule-hair pb-1">
        {/*
          A plain label, not a heading: the rail is the first column in DOM order,
          so an <h2> here would land before the page's <h1> and break heading
          order. The nav's accessible name carries the same information.
        */}
        <span className="text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
          Contents
        </span>
        <button
          type="button"
          onClick={() => setShown((value) => !value)}
          aria-expanded={shown}
          aria-controls="toc-list"
          className="cursor-pointer text-2xs text-link hover:underline"
        >
          {shown ? "hide" : "show"}
        </button>
      </div>

      {/* Kept mounted rather than unmounted, so `aria-controls` always resolves. */}
      <ol id="toc-list" hidden={!shown} className="mt-1">
        <li>
          <TocLink href={`#${topId}`} depth={1} active={active === null}>
            (Top)
          </TocLink>
        </li>
        {tree.map((node) => (
          <TocBranch key={node.id} node={node} active={active} autoCollapse={count > TOC_AUTO_COLLAPSE_ABOVE} />
        ))}
      </ol>
    </nav>
  );
}

export interface TableOfContentsDisclosureProps extends TableOfContentsProps {
  /** Open by default between 768px and `shelf`, closed below 768px. */
  defaultOpen?: boolean;
}

/**
 * The same contents as a `<details>`, for every width below `shelf`.
 *
 * A disclosure in the reading order, exactly where Wikipedia puts its mobile
 * TOC — never a floating overlay panel. That is what preserves document order
 * for a screen reader and for print, and the TOC never exists in two places at
 * once: the page mounts this OR the rail, not both.
 */
export function TableOfContentsDisclosure({
  defaultOpen = false,
  className,
  ...rest
}: TableOfContentsDisclosureProps) {
  const { count } = useContents(rest.content, rest.extraSections ?? NO_SECTIONS);
  if (count < 2) return null;

  return (
    <details
      open={defaultOpen}
      className={cn(
        "my-4 max-w-[var(--measure-prose)] rounded-chrome border border-rule bg-panel px-2.5 py-1.5 print:hidden",
        className,
      )}
    >
      <summary className="cursor-pointer list-none font-sans text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase [&::-webkit-details-marker]:hidden">
        Contents
      </summary>
      <TableOfContents {...rest} className="static max-h-none overflow-visible" />
    </details>
  );
}

/* =====================================================================
   Internals
   ===================================================================== */

function useContents(content: string, extraSections: readonly ExtraSection[]) {
  return useMemo(() => {
    const headings = extractHeadings(content);
    const topLevel = headings.filter((heading) => heading.level === 2).length;

    const appended: Heading[] = extraSections.map((section, index) => ({
      id: section.id,
      text: section.text,
      level: 2 as const,
      number: String(topLevel + index + 1),
    }));

    const all = [...headings, ...appended];
    return {
      tree: buildHeadingTree(all),
      ids: all.map((heading) => heading.id),
      count: all.length,
    };
  }, [content, extraSections]);
}

/**
 * Which heading the reader is currently in.
 *
 * `null` means "above the first heading", i.e. the lead — which is what makes
 * `(Top)` the active row on arrival instead of nothing being active.
 */
function useActiveHeading(ids: readonly string[]): string | null {
  const [active, setActive] = useState<string | null>(null);

  useEffect(() => {
    if (ids.length === 0 || typeof IntersectionObserver === "undefined") return;

    const elements = ids
      .map((id) => document.getElementById(id))
      .filter((el): el is HTMLElement => el !== null);
    if (elements.length === 0) return;

    const order = new Map(ids.map((id, index) => [id, index]));
    const visible = new Set<string>();

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) visible.add(entry.target.id);
          else visible.delete(entry.target.id);
        }
        if (visible.size === 0) return;
        let best: string | null = null;
        for (const id of visible) {
          if (best === null || (order.get(id) ?? 0) < (order.get(best) ?? 0)) best = id;
        }
        setActive(best);
      },
      {
        rootMargin: `-${Math.round(anchorOffset())}px 0px -70% 0px`,
        threshold: 0,
      },
    );

    for (const element of elements) observer.observe(element);
    return () => observer.disconnect();
  }, [ids]);

  return active;
}

function containsId(node: HeadingNode, id: string | null): boolean {
  if (id === null) return false;
  if (node.id === id) return true;
  return node.children.some((child) => containsId(child, id));
}

function TocBranch({
  node,
  active,
  autoCollapse,
}: {
  node: HeadingNode;
  active: string | null;
  autoCollapse: boolean;
}) {
  const hasActive = containsId(node, active);
  const [open, setOpen] = useState(!autoCollapse);
  const expanded = open || hasActive;

  return (
    <li>
      <div className="flex items-start">
        <TocLink
          href={`#${node.id}`}
          depth={node.level - 1}
          number={node.number}
          active={node.id === active}
          className="min-w-0 flex-1"
        >
          {node.text}
        </TocLink>
        {node.children.length > 0 ? (
          <button
            type="button"
            onClick={() => setOpen(!expanded)}
            aria-expanded={expanded}
            aria-label={`${expanded ? "Collapse" : "Expand"} subsections of ${node.text}`}
            className="mt-1.5 grid size-5 shrink-0 cursor-pointer place-items-center rounded-chrome text-ink-3 hover:bg-panel hover:text-ink"
          >
            <ChevronRight
              className={cn(
                "size-3.5 motion-safe:transition-transform motion-safe:duration-100",
                expanded && "rotate-90",
              )}
              aria-hidden="true"
            />
          </button>
        ) : null}
      </div>

      {node.children.length > 0 ? (
        <ol hidden={!expanded} className="ml-3">
          {node.children.map((child) => (
            <TocBranch key={child.id} node={child} active={active} autoCollapse={autoCollapse} />
          ))}
        </ol>
      ) : null}
    </li>
  );
}

function TocLink({
  href,
  depth,
  number,
  active = false,
  className,
  children,
}: {
  href: string;
  depth: number;
  number?: string;
  active?: boolean;
  className?: string;
  children: ReactNode;
}) {
  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const id = href.slice(1);
    if (id === "content") {
      window.scrollTo({ top: 0, behavior: "auto" });
      return;
    }
    jumpToAnchor(id);
  }

  return (
    <a
      href={href}
      onClick={handleClick}
      aria-current={active ? "location" : undefined}
      className={cn(
        // 6px of vertical padding per row: Vector's own measured `.vector-toc-text`.
        "group flex gap-2 rounded-chrome py-1.5 pr-1 pl-2 text-link hover:bg-panel hover:text-link-hover",
        active && "-ml-px border-l-2 border-ink bg-panel pl-[calc(0.5rem-1px)] font-semibold text-ink",
        depth > 1 && "text-[0.9375em]",
        className,
      )}
    >
      {number ? (
        <span className="shrink-0 text-ink-3 tabular-nums" aria-hidden="true">
          {number}
        </span>
      ) : null}
      <span className="min-w-0">{children}</span>
    </a>
  );
}
