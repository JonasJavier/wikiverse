import { Link } from "react-router-dom";

import type { Author, Revision } from "@/lib/types";
import { cn, formatDate, formatDateTime } from "@/lib/utils";

export interface ArticleMetaProps {
  slug: string;
  /** `Article.updated_at`. */
  updatedAt: string;
  /** `Article.created_at`. */
  createdAt: string;
  lastEditor: Author | null;
  latestRevision: Revision | null;
  className?: string;
}

/**
 * The last-edited footer, in the wiki's own words:
 * "This page was last edited on 26 September 2026, at 16:41, by Ada."
 *
 * A `<time>` carries the machine-readable instant and a `title` carries the
 * exact timestamp, because a relative time alone ("3 days ago") is not enough
 * for a document whose history is the point.
 *
 * `view_count` deliberately does not appear here. Per-document statistics live
 * in the Tools rail beside the document, not in the reading surface.
 */
export function ArticleMeta({
  slug,
  updatedAt,
  createdAt,
  lastEditor,
  latestRevision,
  className,
}: ArticleMetaProps) {
  const editor = latestRevision?.editor ?? lastEditor;

  return (
    <footer
      className={cn(
        "mt-6 border-t border-rule-hair pt-2 font-sans text-xs text-ink-2 print:hidden",
        className,
      )}
    >
      <p>
        This page was last edited on{" "}
        <time dateTime={updatedAt} title={formatDateTime(updatedAt)}>
          {formatDateTime(updatedAt)}
        </time>
        {editor ? (
          <>
            , by <Link to={`/u/${editor.username}`}>{editor.username}</Link>
          </>
        ) : null}
        .{" "}
        <Link to={`/wiki/${slug}/history`}>View history</Link>
      </p>
      <p className="mt-0.5">
        Created{" "}
        <time dateTime={createdAt} title={formatDateTime(createdAt)}>
          {formatDate(createdAt)}
        </time>
        . Text is available under a Creative Commons licence.
      </p>
    </footer>
  );
}
