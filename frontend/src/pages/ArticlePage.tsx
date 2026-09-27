import {
  Clock,
  Eye,
  History,
  Pencil,
  Trash2,
  TriangleAlert,
} from "lucide-react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { useArticle, useDeleteArticle } from "@/api/articles";
import { Markdown } from "@/components/article/Markdown";
import { CategoryChip } from "@/components/article/CategoryChip";
import { TableOfContents } from "@/components/article/TableOfContents";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { formatCount, formatDate, formatRelativeTime } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";

const CONTAINER = "mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-10";

export function ArticlePage() {
  const { slug = "" } = useParams();
  const { data: article, isLoading, isError } = useArticle(slug);
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const del = useDeleteArticle();
  const navigate = useNavigate();

  if (isLoading) return <ArticleSkeleton />;

  if (isError || !article) {
    return (
      <div className={CONTAINER}>
        <EmptyState
          icon={TriangleAlert}
          title="Article not found"
          description="This page doesn't exist or may have been removed."
          action={
            <Link to="/browse" className={buttonVariants()}>
              Browse articles
            </Link>
          }
        />
      </div>
    );
  }

  const canDelete = user && article.author && user.id === article.author.id;

  async function handleDelete() {
    if (!article) return;
    if (!window.confirm(`Delete “${article.title}”? This cannot be undone.`)) return;
    await del.mutateAsync(article.slug);
    navigate("/browse");
  }

  return (
    <div className={CONTAINER}>
      <div className="grid grid-cols-1 gap-10 xl:grid-cols-[1fr_15rem]">
        <article className="min-w-0">
          <div className="mx-auto max-w-3xl">
            {/* Header */}
            <header className="mb-8">
              {article.category && <CategoryChip category={article.category} />}
              <h1 className="mt-3 font-serif text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl">
                {article.title}
              </h1>
              {article.summary && (
                <p className="mt-4 text-lg leading-relaxed text-muted">
                  {article.summary}
                </p>
              )}

              <div className="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2 border-y border-border py-3 text-sm text-muted">
                {article.author && (
                  <Link
                    to={`/u/${article.author.username}`}
                    className="flex items-center gap-2 hover:text-foreground"
                  >
                    <Avatar name={article.author.username} src={article.author.avatar} className="size-7" />
                    <span className="font-medium text-foreground">
                      {article.author.username}
                    </span>
                  </Link>
                )}
                <span className="flex items-center gap-1.5">
                  <Clock className="size-4" />
                  {article.read_time} min read
                </span>
                <span className="flex items-center gap-1.5">
                  <Eye className="size-4" />
                  {formatCount(article.view_count)} views
                </span>
                <Link
                  to={`/wiki/${article.slug}/history`}
                  className="flex items-center gap-1.5 hover:text-foreground"
                >
                  <History className="size-4" />
                  {article.revision_count} revision{article.revision_count === 1 ? "" : "s"}
                </Link>
              </div>

              {/* Actions */}
              <div className="mt-4 flex flex-wrap items-center gap-2">
                {isAuthenticated && (
                  <Link
                    to={`/wiki/${article.slug}/edit`}
                    className={buttonVariants({ variant: "outline", size: "sm" })}
                  >
                    <Pencil className="size-4" />
                    Edit
                  </Link>
                )}
                <Link
                  to={`/wiki/${article.slug}/history`}
                  className={buttonVariants({ variant: "ghost", size: "sm" })}
                >
                  <History className="size-4" />
                  History
                </Link>
                {canDelete && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleDelete}
                    disabled={del.isPending}
                    className="text-danger hover:bg-danger/10"
                  >
                    <Trash2 className="size-4" />
                    Delete
                  </Button>
                )}
              </div>
            </header>

            {/* Body */}
            <Markdown content={article.content} />

            {/* Footer meta */}
            <footer className="mt-12 border-t border-border pt-6 text-sm text-muted">
              Last edited {formatRelativeTime(article.updated_at)}
              {article.last_editor && (
                <> by <span className="font-medium text-foreground">{article.last_editor.username}</span></>
              )}{" "}
              · Created {formatDate(article.created_at)}
            </footer>
          </div>
        </article>

        {/* TOC sidebar */}
        <aside className="hidden xl:block">
          <div className="sticky top-24">
            <TableOfContents content={article.content} />
          </div>
        </aside>
      </div>
    </div>
  );
}

function ArticleSkeleton() {
  return (
    <div className={CONTAINER}>
      <div className="mx-auto max-w-3xl">
        <Skeleton className="h-5 w-24 rounded-full" />
        <Skeleton className="mt-4 h-12 w-3/4" />
        <Skeleton className="mt-4 h-6 w-full" />
        <Skeleton className="mt-8 h-4 w-full" />
        <Skeleton className="mt-3 h-4 w-full" />
        <Skeleton className="mt-3 h-4 w-5/6" />
        <Skeleton className="mt-8 h-40 w-full rounded-xl" />
      </div>
    </div>
  );
}
