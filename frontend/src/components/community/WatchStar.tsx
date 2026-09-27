import { Star } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

import { useToggleWatch } from "@/api/community";
import { apiErrorMessage } from "@/lib/api";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import { toast } from "@/store/toast";

export interface WatchStarProps {
  slug: string;
  /** The article title. It goes in the accessible name, so it is required. */
  title: string;
  /** `Article.is_watched`. Always `false` for an anonymous reader. */
  watched: boolean;
  className?: string;
}

/**
 * Add or remove this article from the reader's watchlist.
 *
 * `aria-pressed`, not `aria-checked`: this is a toggle button, not a
 * checkbox, and the accessible NAME changes with the state ("Watch Marie
 * Curie" / "Unwatch Marie Curie") so the control is unambiguous the moment it
 * receives focus rather than only after the reader inspects its state.
 *
 * Two channels carry the state — fill AND colour — so it is legible in
 * greyscale: filled in `--ok` when watched, outline in `--ink-2` when not.
 *
 * The mutation is optimistic against the article detail cache (see
 * `useToggleWatch`), so the star flips on the click. On failure it reverts
 * AND raises a toast naming the article: a star that silently springs back
 * is worse than one that never moved, because the reader walks away
 * believing the page is watched.
 *
 * For an anonymous reader this renders a LINK to sign in, not a dead button.
 * `POST /watch/` requires authentication, and the honest answer to "why did
 * nothing happen?" is a sign-in page.
 */
export function WatchStar({ slug, title, watched, className }: WatchStarProps) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const location = useLocation();
  const toggle = useToggleWatch(slug);

  const shell =
    "grid size-8 shrink-0 place-items-center rounded-chrome hover:bg-panel";

  if (!isAuthenticated) {
    return (
      <Link
        to={`/login?next=${encodeURIComponent(location.pathname)}`}
        aria-label={`Sign in to watch ${title}`}
        title="Sign in to watch pages"
        className={cn(shell, "text-ink-3 hover:text-ink-2", className)}
      >
        <Star aria-hidden="true" className="size-4" />
      </Link>
    );
  }

  return (
    <button
      type="button"
      aria-pressed={watched}
      aria-label={watched ? `Unwatch ${title}` : `Watch ${title}`}
      disabled={toggle.isPending}
      onClick={() =>
        toggle.mutate(!watched, {
          onError: (error) =>
            toast.error(
              watched
                ? `Could not stop watching “${title}”.`
                : `Could not watch “${title}”.`,
              { detail: apiErrorMessage(error, "The change was not saved.") },
            ),
        })
      }
      className={cn(
        shell,
        "cursor-pointer transition-colors duration-100 disabled:opacity-60",
        watched ? "text-ok" : "text-ink-2 hover:text-ink",
        className,
      )}
    >
      <Star
        aria-hidden="true"
        className={cn("size-4", watched && "fill-current")}
      />
    </button>
  );
}
