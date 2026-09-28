import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link, Navigate } from "react-router-dom";

import { fetchRandomArticle } from "@/api/articles";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";

/**
 * `/random` — a route rather than only a button, so it can be linked and
 * bookmarked (design-ui §5.13). One quiet line while the request is in flight,
 * announced politely, then a replace-navigation so Back skips this page.
 *
 * `gcTime: 0` and a key per mount: every visit must draw a new article, never a
 * cached one.
 */
export function RandomPage() {
  useDocumentMeta({ title: "Random article", robots: "noindex" });
  // Stable for the life of this mount; a fresh value on the next visit.
  const [draw] = useState(() => Math.random());

  const { data, isError } = useQuery({
    queryKey: ["articles", "random", draw],
    queryFn: fetchRandomArticle,
    gcTime: 0,
    staleTime: 0,
    retry: 1,
  });

  if (data) return <Navigate to={`/wiki/${data.slug}`} replace />;

  return (
    <WikiFrame>
      <p className="pt-10 text-ui text-ink-2" aria-live="polite">
        {isError ? (
          <>
            No article could be drawn at random.{" "}
            <Link to="/browse" className="text-link hover:text-link-hover">
              Browse every article
            </Link>{" "}
            instead.
          </>
        ) : (
          "Taking you to a random article…"
        )}
      </p>
    </WikiFrame>
  );
}
