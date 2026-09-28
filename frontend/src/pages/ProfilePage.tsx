import type { ReactNode } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";

import { useArticles } from "@/api/articles";
import { usePublicProfile } from "@/api/community";
import { Markdown } from "@/components/article/Markdown";
import { ContributionsList } from "@/components/community/ContributionsList";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Avatar } from "@/components/ui/Avatar";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { cn, formatDate, formatKb, formatNumber } from "@/lib/utils";

/** DECISIONS §10: `/api/articles/` pages at 20. */
const ARTICLE_PAGE_SIZE = 20;

type ProfileTab = "contributions" | "created";

/**
 * `/u/:username?tab=&page=` — a public profile and its contributions.
 *
 * **`email` is never rendered here, and cannot be.** The query reads
 * `PublicUser`, which by construction has no `email` field — the old page
 * read the full `User` shape off `/auth/users/{username}/`, which is exactly
 * how one reader's address ends up on another reader's screen. Keeping the
 * narrow type is the enforcement mechanism, not a note in a review.
 *
 * The avatar carries `alt=""` (the `Avatar` primitive hard-codes it): the name
 * is immediately beside it as text, so a real `alt` makes a screen reader
 * announce the same username twice.
 */
export function ProfilePage() {
  const { username = "" } = useParams();
  const [search] = useSearchParams();

  const tab: ProfileTab = search.get("tab") === "created" ? "created" : "contributions";
  const page = Math.max(1, Number.parseInt(search.get("page") ?? "1", 10) || 1);

  const profile = usePublicProfile(username);
  /**
   * Queried on both tabs rather than only on `?tab=created`. A hook cannot be
   * conditional, and the alternative — an `enabled` flag threaded through
   * `useArticles`, which another area owns — would be a cross-area edit for
   * one request that also happens to warm the other tab.
   */
  const created = useArticles({
    author: username,
    page,
    page_size: ARTICLE_PAGE_SIZE,
    ordering: "-created_at",
  });

  useDocumentMeta({
    title: username || "User",
    description: profile.data
      ? `${profile.data.username} has made ${profile.data.edit_count} edits and created ${profile.data.article_count} articles on Wikiverse.`
      : undefined,
    canonical: `/u/${username}`,
  });

  function hrefFor(next: { tab?: ProfileTab; page?: number }): string {
    const params = new URLSearchParams();
    const nextTab = next.tab ?? tab;
    const nextPage = next.page ?? 1;
    if (nextTab !== "contributions") params.set("tab", nextTab);
    if (nextPage > 1) params.set("page", String(nextPage));
    const query = params.toString();
    return query ? `?${query}` : "";
  }

  if (profile.isError) {
    return (
      <WikiFrame rail={<Sidebar />}>
        <div className="pt-4 pb-3">
          <h1 className="font-serif text-h1 font-normal text-ink">{username}</h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <p className="mt-1.5 text-ui text-ink-2">No such account.</p>
        </div>
        <EmptyState
          title="This user does not exist."
          hint={`No account is registered as “${username}”.`}
          action={
            <Link to="/browse" className={buttonVariants({ variant: "secondary" })}>
              Browse articles
            </Link>
          }
        />
      </WikiFrame>
    );
  }

  return (
    <WikiFrame rail={<Sidebar />}>
      <div className="flex items-start gap-3 pt-4 pb-3">
        {profile.isPending ? (
          <Skeleton className="size-12 rounded-full" />
        ) : (
          <Avatar
            name={profile.data.username}
            src={profile.data.avatar}
            className="size-12 text-base"
          />
        )}
        <div className="min-w-0 flex-1">
          <h1 className="font-serif text-h1 font-normal text-balance text-ink">
            {profile.data?.username ?? username}
          </h1>
          <hr className="mt-1.5 border-0 border-t border-rule" />
          <p className="mt-1.5 text-ui text-ink-2">
            {profile.isPending ? (
              <Skeleton className="inline-block h-4 w-64 align-middle" />
            ) : (
              <>
                Joined{" "}
                <time dateTime={profile.data.date_joined} className="tabular-nums">
                  {formatDate(profile.data.date_joined)}
                </time>
                {" · "}
                <span className="tabular-nums">
                  {formatNumber(profile.data.edit_count)}
                </span>{" "}
                {profile.data.edit_count === 1 ? "edit" : "edits"}
                {" · "}
                <span className="tabular-nums">
                  {formatNumber(profile.data.article_count)}
                </span>{" "}
                {profile.data.article_count === 1 ? "article" : "articles"}{" "}
                created
                {profile.data.is_bot && " · bot account"}
              </>
            )}
          </p>
        </div>
      </div>

      {profile.data?.bio && (
        <div className="mb-4">
          <Markdown content={profile.data.bio} headings={false} />
        </div>
      )}

      <div className="mb-4 flex flex-wrap items-end gap-y-1 border-b border-rule">
        <nav aria-label="Profile sections" className="flex">
          <Tab active={tab === "contributions"} to={hrefFor({ tab: "contributions" })}>
            Contributions
          </Tab>
          <Tab active={tab === "created"} to={hrefFor({ tab: "created" })}>
            Created articles
          </Tab>
        </nav>
      </div>

      {tab === "contributions" ? (
        <section>
          <h2 className="sr-only">Contributions</h2>
          <ContributionsList
            username={username}
            page={page}
            hrefForPage={(next) => hrefFor({ page: next })}
          />
        </section>
      ) : (
        <section>
          <h2 className="sr-only">Created articles</h2>
          {created.isPending ? (
            <div className="space-y-2" aria-busy="true">
              {Array.from({ length: 6 }).map((_, index) => (
                <Skeleton key={index} className="h-10 w-full" />
              ))}
            </div>
          ) : created.data && created.data.results.length > 0 ? (
            <>
              <ul className="divide-y divide-rule-hair border-t border-rule-hair">
                {created.data.results.map((article) => (
                  <li key={article.slug} className="py-2.5">
                    <Link
                      to={`/wiki/${article.slug}`}
                      className="text-base font-medium text-link hover:underline"
                    >
                      {article.title}
                    </Link>
                    {article.short_description && (
                      <p className="text-ui text-ink-2">
                        {article.short_description}
                      </p>
                    )}
                    <p className="text-2xs text-ink-3">
                      <span className="tabular-nums">
                        {formatKb(article.byte_size)}
                      </span>
                      {" · "}
                      <span className="tabular-nums">
                        {formatNumber(article.word_count)}
                      </span>{" "}
                      words · created{" "}
                      <time dateTime={article.created_at} className="tabular-nums">
                        {formatDate(article.created_at)}
                      </time>
                      {article.is_stub && " · stub"}
                    </p>
                  </li>
                ))}
              </ul>
              <Pagination
                page={page}
                count={created.data.count}
                pageSize={ARTICLE_PAGE_SIZE}
                hrefFor={(next) => hrefFor({ page: next })}
              />
            </>
          ) : (
            <EmptyState
              title="No articles created yet."
              hint={`${profile.data?.username ?? username} has edited pages but has not started one.`}
            />
          )}
        </section>
      )}
    </WikiFrame>
  );
}

/**
 * The namespace-tab shape from design-ui §3.7: ink weight plus a 2px ink
 * underline that breaks the row's own rule via `-mb-px`. Never an accent
 * fill — the accent means "link", and the inactive tabs are links.
 *
 * The active tab is a `<span>`, not a `<Link>`: a link to the view you are
 * already on is a screen-reader dead end.
 */
function Tab({
  active,
  to,
  children,
}: {
  active: boolean;
  to: string;
  children: ReactNode;
}) {
  const base =
    "relative -mb-px inline-flex items-center gap-1.5 border-b-2 px-3 py-2 text-ui " +
    "whitespace-nowrap transition-colors duration-100 motion-reduce:transition-none";

  if (active) {
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
