import { MessageSquarePlus } from "lucide-react";
import { type ReactNode, useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";

import { useArticle } from "@/api/articles";
import { useCreateTalkThread, useTalkThreads } from "@/api/community";
import { TalkComposer } from "@/components/community/TalkComposer";
import { TalkThread } from "@/components/community/TalkThread";
import { WatchStar } from "@/components/community/WatchStar";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Button } from "@/components/ui/Button";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { apiErrorMessage } from "@/lib/api";
import { cn, formatNumber, scrollBehavior } from "@/lib/utils";
import { toast } from "@/store/toast";

/**
 * `/wiki/:slug/talk` — the discussion namespace for one article.
 *
 * Both tab groups render on both namespaces (design-ui §3.7: "the detail
 * clones get wrong"), so the Talk page keeps Read / Edit / View history
 * pointing at the article namespace rather than dropping them.
 *
 * The talk markdown path is the article markdown path — `TalkComposer` and
 * `TalkMessage` both mount `components/article/Markdown.tsx`. There is no
 * second renderer to get wrong, which is how DECISIONS §0.5 ("no
 * `rehype-raw`, `skipHtml` for talk messages exactly as for article bodies")
 * stays true without a second audit.
 *
 * There is no Subscribe control anywhere on this page: DECISIONS §12 cut it
 * because no subscription model exists behind it.
 */
export function TalkPage() {
  const { slug = "" } = useParams();
  const location = useLocation();
  const article = useArticle(slug);
  const threads = useTalkThreads(slug);
  const createThread = useCreateTalkThread(slug);
  const [composing, setComposing] = useState(false);

  const title = article.data?.title ?? slug;
  const rows = threads.data?.results ?? [];

  useDocumentMeta({
    title: `Talk: ${title}`,
    description: `Discussion about improving the ${title} article on Wikiverse.`,
    canonical: `/wiki/${slug}/talk`,
    robots: "noindex",
  });

  /**
   * A talk row in Recent changes links to `#c-123`, and a topic heading to
   * `#thread-4`. Neither target exists at first paint, because the threads and
   * then each thread's messages load after it — so the browser's own hash jump
   * fires against nothing. Re-running it once the threads have arrived is what
   * makes those links work at all.
   */
  const hash = location.hash;
  const threadsReady = !threads.isPending;
  useEffect(() => {
    if (!hash || !threadsReady) return;
    const target = document.getElementById(hash.slice(1));
    if (target) {
      target.scrollIntoView({ behavior: scrollBehavior(), block: "start" });
    }
  }, [hash, threadsReady, rows.length]);

  const addTopicButton = (
    <Button
      onClick={() => setComposing(true)}
      aria-expanded={composing}
      size="sm"
    >
      <MessageSquarePlus aria-hidden="true" className="size-4" />
      Add topic
    </Button>
  );

  return (
    <WikiFrame
      rail={
        <>
          <Sidebar />
          {rows.length > 0 && (
            <nav aria-label="Topics" className="mt-6 text-ui">
              <p className="mb-1 border-b border-rule-hair pb-1 text-2xs tracking-[0.04em] text-ink-2 uppercase">
                Topics
              </p>
              <ol className="space-y-1">
                {rows.map((thread, index) => (
                  <li key={thread.id} className="flex gap-1.5">
                    <span className="tabular-nums text-ink-3">{index + 1}</span>
                    <a
                      href={`#thread-${thread.id}`}
                      className="text-link hover:underline"
                    >
                      {thread.title}
                    </a>
                  </li>
                ))}
              </ol>
            </nav>
          )}
        </>
      }
    >
      <div className="mb-4 flex flex-wrap items-end justify-between gap-y-1 border-b border-rule">
        <nav aria-label="Namespace" className="flex">
          <Tab to={`/wiki/${slug}`}>Article</Tab>
          <Tab active>
            Talk
            {article.data && article.data.talk_thread_count > 0 && (
              <sup className="ml-0.5 text-2xs font-normal text-ink-2 tabular-nums">
                {formatNumber(article.data.talk_thread_count)}
              </sup>
            )}
          </Tab>
        </nav>
        <nav aria-label="Page actions" className="flex">
          <Tab to={`/wiki/${slug}`}>Read</Tab>
          <Tab to={`/wiki/${slug}/edit`}>Edit</Tab>
          <Tab to={`/wiki/${slug}/history`}>View history</Tab>
        </nav>
      </div>

      <div className="flex items-start justify-between gap-3 pt-1 pb-3">
        <div className="min-w-0 flex-1">
          <h1 className="font-serif text-h1 font-normal text-balance text-ink">
            Talk: {title}
          </h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <p className="mt-1.5 text-ui text-ink-2">
            Discussion about improving the{" "}
            <Link to={`/wiki/${slug}`} className="text-link hover:underline">
              {title}
            </Link>{" "}
            article.
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          {article.data && (
            <WatchStar
              slug={slug}
              title={article.data.title}
              watched={article.data.is_watched}
            />
          )}
          {addTopicButton}
        </div>
      </div>

      {composing && (
        <TalkComposer
          key={`new-topic-${rows.length}`}
          withTitle
          autoFocus
          submitLabel="Add topic"
          placeholder="Describe what should change and why. Markdown is supported; raw HTML is not."
          note="Opening a topic posts its first comment at the same time."
          busy={createThread.isPending}
          className="mb-4"
          onCancel={() => setComposing(false)}
          onSubmit={({ title: topic, body }) =>
            createThread.mutate(
              { title: topic ?? "", body },
              {
                onSuccess: () => {
                  setComposing(false);
                  toast.success("Topic added.");
                },
                onError: (error) =>
                  toast.error("Could not add that topic.", {
                    detail: apiErrorMessage(error),
                  }),
              },
            )
          }
        />
      )}

      <section aria-busy={threads.isPending}>
        {threads.isPending ? (
          <div className="space-y-4">
            {Array.from({ length: 2 }).map((_, index) => (
              <div key={index} className="space-y-2">
                <Skeleton className="h-7 w-2/3" />
                <Skeleton className="h-4 w-1/2" />
                <Skeleton className="h-4 w-full" />
              </div>
            ))}
          </div>
        ) : threads.isError ? (
          <EmptyState
            title="This talk page could not be loaded."
            hint="The article may have been removed. Try the article itself."
            action={
              <Link
                to={`/wiki/${slug}`}
                className={buttonVariants({ variant: "secondary" })}
              >
                Go to the article
              </Link>
            }
          />
        ) : rows.length === 0 ? (
          <EmptyState
            title="No discussion yet."
            hint="Start the first topic. Talk pages are for deciding what an article should say — not for the article text itself."
            action={addTopicButton}
          />
        ) : (
          <div className="space-y-6">
            {rows.map((thread) => (
              <TalkThread key={thread.id} slug={slug} thread={thread} />
            ))}
          </div>
        )}
      </section>

      {rows.length > 0 && (
        <div className="mt-8 border-t border-rule pt-3">{addTopicButton}</div>
      )}
    </WikiFrame>
  );
}

/**
 * design-ui §3.7's tab: ink weight plus a 2px ink underline breaking the row's
 * own rule via `-mb-px`. The active tab is a `<span>` with
 * `aria-current="page"`, because a link to the page you are on is a
 * screen-reader dead end.
 */
function Tab({
  to,
  active = false,
  children,
}: {
  to?: string;
  active?: boolean;
  children: ReactNode;
}) {
  const base =
    "relative -mb-px inline-flex items-baseline gap-1.5 border-b-2 px-3 py-2 text-ui " +
    "whitespace-nowrap transition-colors duration-100 motion-reduce:transition-none";

  if (active || !to) {
    return (
      <span
        aria-current="page"
        className={cn(base, "cursor-default border-ink font-semibold text-ink")}
      >
        {children}
      </span>
    );
  }
  return (
    <Link
      to={to}
      className={cn(
        base,
        "border-transparent text-link hover:border-rule hover:text-link-hover",
      )}
    >
      {children}
    </Link>
  );
}
