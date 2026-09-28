import axios from "axios";
import { Printer, Star } from "lucide-react";
import { type ReactNode, useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";

import {
  useArticle,
  useDeleteArticle,
  usePageInfo,
  useWatchArticle,
  type ArticleDetail,
} from "@/api/articles";
import { ArticleMeta } from "@/components/article/ArticleMeta";
import { CategoryFooterBar } from "@/components/article/CategoryFooterBar";
import { Infobox } from "@/components/article/Infobox";
import { LeadImage } from "@/components/article/LeadImage";
import { MarkdownFlow } from "@/components/article/Markdown";
import {
  buildFootnoteScope,
  FootnoteContext,
  LinkResolutionContext,
  splitLead,
  useArticleLinkResolver,
  type FootnoteSource,
} from "@/components/article/markdownUtils";
import { References } from "@/components/article/References";
import { SeeAlso } from "@/components/article/SeeAlso";
import { StubNotice } from "@/components/article/StubNotice";
import {
  TableOfContents,
  TableOfContentsDisclosure,
  type ExtraSection,
} from "@/components/article/TableOfContents";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useIsShelf } from "@/hooks/useMediaQuery";
import type { CategoryRef } from "@/lib/types";
import { cn, formatNumber } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import { toast } from "@/store/toast";

/**
 * THE ARTICLE PAGE.
 *
 * Element order is fixed by MOS:LAYOUT and enforced HERE, by the component,
 * rather than by whoever wrote the Markdown (design-ui §5.2):
 *
 *   tab row → title block → hatnotes → infobox → lead → mobile contents →
 *   body → See also → References → category bar → stub notice → tools
 *
 * Hatnotes come before the infobox because that is the screen-reader order MOS
 * requires, and it is exactly the thing a right float makes look correct while
 * being wrong.
 *
 * There is NO duplicate `h1`: the page renders the title, and the body starts at
 * `h2` (DECISIONS §19 forbids a body `h1`; the renderer demotes one if it slips
 * through).
 */
export function ArticlePage() {
  const { slug = "" } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const isShelf = useIsShelf();

  const user = useAuthStore((state) => state.user);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const { data: article, isLoading, isError, error } = useArticle(slug);

  const resolveLink = useArticleLinkResolver(article);
  const footnoteSources = useFootnoteSources(article);
  const footnotes = useMemo(
    () => buildFootnoteScope(article?.references ?? [], footnoteSources),
    [article?.references, footnoteSources],
  );

  const { lead, body } = useMemo(() => splitLead(article?.content ?? ""), [article?.content]);
  const seeAlso = article?.see_also ?? EMPTY_TITLES;
  const extraSections = useMemo<ExtraSection[]>(() => {
    const sections: ExtraSection[] = [];
    if (seeAlso.length > 0) sections.push({ id: "see-also", text: "See also" });
    if ((article?.references.length ?? 0) > 0) {
      sections.push({ id: "references", text: "References" });
    }
    return sections;
  }, [article?.references.length, seeAlso.length]);

  const del = useDeleteArticle();
  const watch = useWatchArticle(slug);
  const [confirmOpen, setConfirmOpen] = useState(false);

  const notFound = isError && axios.isAxiosError(error) && error.response?.status === 404;

  useDocumentMeta({
    title: article?.title ?? (notFound ? decodeURIComponent(slug) : undefined),
    description: article?.short_description || article?.summary,
    canonical: `/wiki/${slug}`,
    robots: notFound ? "noindex" : undefined,
    image: article?.lead_image_url || undefined,
    imageAlt: article?.lead_image_alt || undefined,
    type: "article",
  });

  if (isLoading) return <ArticleSkeleton slug={slug} />;
  if (notFound) return <MissingArticle slug={slug} />;
  // A 500 is not a missing page, and telling a reader the article does not exist
  // when the server merely failed is the kind of wrong that costs trust.
  if (!article) return <LoadFailure slug={slug} />;

  const categories = articleCategories(article);
  const canDelete = Boolean(
    user && (user.is_staff || (article.author && user.id === article.author.id)),
  );
  const redirectedFrom = searchParams.get("redirect") === "no" ? null : article.redirected_from;

  async function handleDelete() {
    try {
      await del.mutateAsync(slug);
      toast.success(`“${article?.title ?? slug}” was deleted.`);
      setConfirmOpen(false);
      navigate("/browse");
    } catch {
      toast.error("The article could not be deleted.", {
        detail: "You may not have permission, or the server rejected the request.",
      });
      setConfirmOpen(false);
    }
  }

  async function handleWatch() {
    const next = !article?.is_watched;
    try {
      await watch.mutateAsync(next);
    } catch {
      toast.error(next ? "Could not add this page to your watchlist." : "Could not unwatch this page.");
    }
  }

  const leadImage =
    article.lead_image_url ? (
      <LeadImage
        url={article.lead_image_url}
        alt={article.lead_image_alt}
        caption={article.lead_image_caption}
        credit={article.lead_image_credit}
        license={article.lead_image_license}
        sourceUrl={article.lead_image_source_url}
        variant="infobox"
        priority
        sourceId="leadImage"
      />
    ) : null;

  const hasInfobox = (article.infobox?.rows?.length ?? 0) > 0 || Boolean(leadImage);
  const isDisambiguation = article.is_disambiguation || article.page_type === "disambiguation";

  return (
    <LinkResolutionContext.Provider value={resolveLink}>
      <FootnoteContext.Provider value={footnotes}>
        <WikiFrame
          rail={
            isDisambiguation ? null : (
              <TableOfContents content={article.content} extraSections={extraSections} />
            )
          }
          tools={
            <ArticleTools
              slug={slug}
              wordCount={article.word_count}
              viewCount={article.view_count}
              revisionCount={article.revision_count}
              backlinkCount={article.backlink_count}
            />
          }
        >
          <ArticleTabs slug={slug} talkCount={article.talk_thread_count} />

          <TitleBlock
            title={article.title}
            tagline={
              isDisambiguation
                ? "Wikiverse disambiguation page: one title, several articles."
                : "From Wikiverse, the open encyclopedia."
            }
            redirectedFrom={redirectedFrom}
            actions={
              <div className="flex shrink-0 items-center gap-1">
                {isAuthenticated ? (
                  <button
                    type="button"
                    onClick={handleWatch}
                    disabled={watch.isPending}
                    aria-pressed={article.is_watched}
                    aria-label={
                      article.is_watched ? `Unwatch ${article.title}` : `Watch ${article.title}`
                    }
                    className="grid size-8 cursor-pointer place-items-center rounded-chrome text-ink-2 hover:bg-panel aria-pressed:text-ok"
                  >
                    <Star
                      className={cn("size-4", article.is_watched && "fill-current")}
                      aria-hidden="true"
                    />
                  </button>
                ) : null}
                {canDelete ? (
                  <Button variant="danger" size="sm" onClick={() => setConfirmOpen(true)}>
                    Delete
                  </Button>
                ) : null}
              </div>
            }
          />

          <div className="article-prose">
            {/*
              Hatnotes render FIRST and before the infobox, which is the
              screen-reader order MOS requires. `Hatnote` is built and exported;
              the article payload carries no hatnote data yet, so nothing is
              fabricated here — see the report.
            */}
            {isDisambiguation ? null : (
              <Infobox
                infobox={article.infobox}
                title={article.title}
                image={leadImage}
                sourceId="infobox"
              />
            )}

            {/* The lead image has nowhere to live when there is no infobox. */}
            {!hasInfobox && article.lead_image_url ? (
              <LeadImage
                url={article.lead_image_url}
                alt={article.lead_image_alt}
                caption={article.lead_image_caption}
                credit={article.lead_image_credit}
                license={article.lead_image_license}
                sourceUrl={article.lead_image_source_url}
                variant="figure"
                priority
                sourceId="leadImage"
              />
            ) : null}

            <MarkdownFlow content={lead} sourceId="content.lead" lead headings={false} />

            {/* The contents live in ONE place at a time: the rail above `shelf`,
                this disclosure below it. Never both — duplicating it would
                duplicate every id inside it. */}
            {!isShelf && !isDisambiguation ? (
              <TableOfContentsDisclosure
                content={article.content}
                extraSections={extraSections}
                defaultOpen={false}
              />
            ) : null}

            {body ? <MarkdownFlow content={body} sourceId="content" /> : null}

            <SeeAlso entries={seeAlso} />
            {isDisambiguation ? null : <References references={article.references} />}

            {isDisambiguation ? <DisambiguationNote title={article.title} /> : null}

            <CategoryFooterBar categories={categories} />
            {article.is_stub ? (
              <StubNotice slug={slug} categoryName={article.category?.name} />
            ) : null}
          </div>

          <ArticleMeta
            slug={slug}
            updatedAt={article.updated_at}
            createdAt={article.created_at}
            lastEditor={article.last_editor}
            latestRevision={article.latest_revision}
          />
        </WikiFrame>

        <ConfirmDialog
          open={confirmOpen}
          title={`Delete “${article.title}”?`}
          body={
            <>
              Its {formatNumber(article.revision_count)} revision
              {article.revision_count === 1 ? "" : "s"} and{" "}
              {formatNumber(article.talk_thread_count)} talk thread
              {article.talk_thread_count === 1 ? "" : "s"} go with it.
            </>
          }
          confirmLabel="Delete"
          tone="danger"
          busy={del.isPending}
          onConfirm={handleDelete}
          onCancel={() => setConfirmOpen(false)}
        />
      </FootnoteContext.Provider>
    </LinkResolutionContext.Provider>
  );
}

/* =====================================================================
   Pieces this page owns until the shared layout components land
   =====================================================================
   `TabRow`, `StickySubHeader` and `ToolsRail` are layout components (design-ui
   §3.7, §3.5, §3.10) owned elsewhere in the redesign and not yet in the tree.
   The three below are deliberately LOCAL and unexported, so that when the real
   ones land there is nothing to migrate off and no duplicate export to collide
   with — this file just imports them and deletes these.
   ===================================================================== */

const EMPTY_TITLES: readonly string[] = [];

function ArticleTabs({ slug, talkCount }: { slug: string; talkCount: number }) {
  return (
    <div className="tab-row mb-4 flex flex-wrap items-end justify-between gap-y-1 border-b border-rule print:hidden">
      <nav aria-label="Namespace" className="flex">
        <Tab active>Article</Tab>
        <Tab to={`/wiki/${slug}/talk`} count={talkCount}>
          Talk
        </Tab>
      </nav>
      <nav aria-label="Page actions" className="flex">
        <Tab active>Read</Tab>
        <Tab to={`/wiki/${slug}/edit`}>Edit</Tab>
        <Tab to={`/wiki/${slug}/history`}>View history</Tab>
      </nav>
    </div>
  );
}

function Tab({
  to,
  active = false,
  count,
  children,
}: {
  to?: string;
  active?: boolean;
  count?: number;
  children: ReactNode;
}) {
  const base =
    "relative -mb-px inline-flex items-center gap-1.5 border-b-2 px-3 py-2 text-ui whitespace-nowrap transition-colors duration-100 motion-reduce:transition-none";

  // A link to the page you are already on is a screen-reader dead end, so the
  // active tab is a span with aria-current, not an anchor.
  if (active || to === undefined) {
    return (
      <span aria-current="page" className={cn(base, "cursor-default border-ink font-semibold text-ink")}>
        {children}
      </span>
    );
  }

  return (
    <Link
      to={to}
      className={cn(base, "border-transparent text-link hover:border-rule hover:text-link-hover")}
    >
      {children}
      {count !== undefined && count > 0 ? (
        <sup className="text-2xs text-ink-3 tabular-nums">{formatNumber(count)}</sup>
      ) : null}
    </Link>
  );
}

function TitleBlock({
  title,
  tagline,
  redirectedFrom,
  actions,
}: {
  title: string;
  tagline: string;
  redirectedFrom?: string | { slug: string; title: string } | null;
  actions?: ReactNode;
}) {
  const redirect =
    typeof redirectedFrom === "string"
      ? { slug: redirectedFrom, title: redirectedFrom }
      : redirectedFrom ?? null;

  return (
    <div className="pt-4 pb-3">
      <div className="flex items-start justify-between gap-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">{title}</h1>
        {actions}
      </div>
      <hr className="mt-1.5 border-0 border-t border-rule" />
      <p className="mt-1.5 font-sans text-ui text-ink-2">{tagline}</p>
      {redirect ? (
        <p className="mw-redirectedfrom mt-0.5 font-sans text-ui text-ink-2">
          (Redirected from{" "}
          <Link to={`/wiki/${redirect.slug}?redirect=no`}>{redirect.title}</Link>)
        </p>
      ) : null}
    </div>
  );
}

function ArticleTools({
  slug,
  wordCount,
  viewCount,
  revisionCount,
  backlinkCount,
}: {
  slug: string;
  wordCount: number;
  viewCount: number;
  revisionCount: number;
  backlinkCount: number;
}) {
  const { data: info } = usePageInfo(slug);

  return (
    <aside aria-label="Tools" className="sticky top-[calc(var(--subheader-h)+1rem)] font-sans text-ui print:hidden">
      <RailGroup label="Tools">
        <li>
          <Link to={`/wiki/${slug}/links-here`}>What links here ({formatNumber(backlinkCount)})</Link>
        </li>
        <li>
          <Link to={`/wiki/${slug}/history`}>Permanent link</Link>
        </li>
        <li>
          <Link to={`/wiki/${slug}/info`}>Page information</Link>
        </li>
        <li>
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex cursor-pointer items-center gap-1.5 text-link hover:underline"
          >
            <Printer className="size-3.5" aria-hidden="true" />
            Printable version
          </button>
        </li>
      </RailGroup>

      {/*
        The "This page" block is where the home page's deleted KPI strip actually
        belongs: numbers about THIS document, beside THIS document, at 14px in a
        definition list — not four icon tiles on a reader's front page.
      */}
      <RailGroup label="This page" as="div">
        <dl className="grid grid-cols-[auto_1fr] gap-x-2 gap-y-1 text-ink-2">
          <dt>Revisions</dt>
          <dd className="text-ink tabular-nums">{formatNumber(revisionCount)}</dd>
          <dt>Words</dt>
          <dd className="text-ink tabular-nums">{formatNumber(wordCount)}</dd>
          <dt>Views</dt>
          <dd className="text-ink tabular-nums">{formatNumber(viewCount)}</dd>
          {info ? (
            <>
              <dt>Contributors</dt>
              <dd className="text-ink tabular-nums">{formatNumber(info.contributor_count)}</dd>
              <dt>Watchers</dt>
              <dd className="text-ink tabular-nums">{formatNumber(info.watcher_count)}</dd>
            </>
          ) : null}
        </dl>
      </RailGroup>
    </aside>
  );
}

function RailGroup({
  label,
  as = "ul",
  children,
}: {
  label: string;
  as?: "ul" | "div";
  children: ReactNode;
}) {
  return (
    <div className="mt-4 first:mt-0">
      <p className="border-b border-rule-hair pb-1 text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
        {label}
      </p>
      {as === "ul" ? (
        <ul className="mt-1 space-y-1 [&_a]:text-link [&_a:hover]:underline">{children}</ul>
      ) : (
        <div className="mt-1">{children}</div>
      )}
    </div>
  );
}

/** §5.14's footer note. A `.ambox` in the protection (grey) variant. */
function DisambiguationNote({ title }: { title: string }) {
  return (
    <div
      role="note"
      className="ambox ambox-protection mt-6 grid grid-cols-1 rounded-chrome border border-rule border-l-[10px] border-l-[var(--banner-protect)] bg-panel px-3 py-2 font-sans text-[0.824em] leading-normal"
    >
      This disambiguation page lists articles associated with the title <b>{title}</b>. If an
      internal link brought you here, you may wish to change it to point directly to the intended
      article.
    </div>
  );
}

/* =====================================================================
   Loading and missing
   ===================================================================== */

/**
 * A skeleton with the final layout's GEOMETRY, statically tinted.
 *
 * No shimmer: an infinite animation on a reader-facing page is the single worst
 * accessibility item a stylesheet can carry (design-ui §5.0.5, §6.2). The `h1`
 * is rendered from the route param, so the page is never without a heading.
 */
function ArticleSkeleton({ slug }: { slug: string }) {
  const title = decodeURIComponent(slug).replace(/-/g, " ");

  return (
    <WikiFrame>
      <div aria-busy="true" aria-live="polite">
        <div className="pt-4 pb-3">
          <h1 className="font-serif text-h1 font-normal text-ink first-letter:uppercase">{title}</h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <p className="mt-1.5 font-sans text-ui text-ink-2">Loading…</p>
        </div>
        <div className="mt-4 space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-11/12" />
          <Skeleton className="h-4 w-4/5" />
        </div>
        <Skeleton className="mt-6 h-6 w-1/3" />
        <div className="mt-3 space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-10/12" />
        </div>
      </div>
    </WikiFrame>
  );
}

/**
 * The missing page, in the wiki idiom rather than as an apology: the title you
 * asked for, and three things you can do about it.
 *
 * An SPA cannot set an HTTP status, so `noindex` is what tells a crawler.
 */
function MissingArticle({ slug }: { slug: string }) {
  const title = decodeURIComponent(slug).replace(/-/g, " ");

  return (
    <WikiFrame>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-ink first-letter:uppercase">{title}</h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 font-sans text-ui text-ink-2">
          Wikiverse does not have an article with this exact title.
        </p>
      </div>
      <div className="article-prose mt-4 max-w-[34rem]">
        <p>
          You can <Link to={`/new?title=${encodeURIComponent(title)}`}>create this page</Link>,
          search for <Link to={`/search?q=${encodeURIComponent(title)}`}>“{title}”</Link> in other
          pages, or look through <Link to="/changes">recent changes</Link>.
        </p>
      </div>
    </WikiFrame>
  );
}

/** The article exists as far as we know; the request itself failed. */
function LoadFailure({ slug }: { slug: string }) {
  const title = decodeURIComponent(slug).replace(/-/g, " ");

  return (
    <WikiFrame>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-ink first-letter:uppercase">{title}</h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 font-sans text-ui text-ink-2">
          This page could not be loaded. The server did not answer.
        </p>
      </div>
      <div className="article-prose mt-4 max-w-[34rem]">
        <p>
          Reloading may be enough. If it is not, <Link to="/changes">recent changes</Link> will show
          whether the site is responding at all.
        </p>
      </div>
    </WikiFrame>
  );
}

/* =====================================================================
   Helpers
   ===================================================================== */

/**
 * Every Markdown string on the page that may hold a `[^refkey]`, in DOM order.
 *
 * Order matters: it decides which marker is `a` and which is `b` in the
 * reference list's `^ a b c` backlinks, and the infobox is read before the lead.
 */
function useFootnoteSources(article: ArticleDetail | undefined): FootnoteSource[] {
  const infoboxRows = article?.infobox?.rows;
  const caption = article?.lead_image_caption;
  const content = article?.content;

  return useMemo(() => {
    const sources: FootnoteSource[] = [];
    (infoboxRows ?? []).forEach((row, index) => {
      if (row.kind === "row") sources.push({ id: `infobox.${index}.label`, text: row.label });
      sources.push({ id: `infobox.${index}`, text: row.value });
    });
    if (caption) sources.push({ id: "leadImage", text: caption });
    const { lead, body } = splitLead(content ?? "");
    sources.push({ id: "content.lead", text: lead });
    sources.push({ id: "content", text: body });
    return sources;
  }, [caption, content, infoboxRows]);
}

/** Primary category first, then the extras (DECISIONS §13). */
function articleCategories(article: ArticleDetail): CategoryRef[] {
  if (article.categories && article.categories.length > 0) return article.categories;
  if (!article.category) return [];
  return [
    {
      slug: article.category.slug,
      name: article.category.name,
      color: article.category.color,
    },
  ];
}
