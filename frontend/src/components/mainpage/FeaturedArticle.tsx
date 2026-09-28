import { Link } from "react-router-dom";

import type { ArticleStub, MainPageFeatured } from "@/lib/types";

interface FeaturedArticleProps {
  featured: MainPageFeatured | null | undefined;
  /** The blocks behind the current one, newest first. */
  recentlyFeatured: ArticleStub[];
}

/** The extract arrives as plain text (`plain_extract`), paragraph-separated. */
function paragraphs(extract: string, limit = 3): string[] {
  return extract
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .filter(Boolean)
    .slice(0, limit);
}

/**
 * The Featured article panel: a floated thumbnail, the article's real opening
 * in serif, then `Full article →` and the `Recently featured:` line.
 *
 * The thumbnail is the main page's LCP element, so it declares
 * `fetchPriority="high"`, `loading="eager"` and an explicit box (a fixed
 * aspect ratio rather than raw pixel attributes, because the seed's Wikimedia
 * images have no fixed proportion and stretching one to fit is worse than
 * cropping it). Nothing here animates and nothing has a shadow.
 */
export function FeaturedArticle({
  featured,
  recentlyFeatured,
}: FeaturedArticleProps) {
  if (!featured) {
    return (
      <p className="text-ui text-ink-2">
        No article has been featured yet.{" "}
        <Link to="/browse" className="text-link hover:underline">
          Browse all articles
        </Link>{" "}
        instead.
      </p>
    );
  }

  const body = paragraphs(featured.extract || featured.short_description || "");

  return (
    <div>
      {/* The float narrows on a phone so the extract keeps a readable measure
          beside it, and widens once the panel has room. */}
      {featured.lead_image_url && (
        <figure className="float-right mb-2 ml-3 w-[7.5rem] sm:w-[9rem] md:w-[11rem]">
          <img
            src={featured.lead_image_url}
            alt={featured.lead_image_alt ?? ""}
            width={176}
            height={220}
            fetchPriority="high"
            loading="eager"
            decoding="async"
            className="aspect-[4/5] w-full rounded-chrome border border-rule-hair object-cover"
          />
          {featured.lead_image_caption && (
            <figcaption className="mt-1 text-2xs leading-snug text-ink-2">
              {featured.lead_image_caption}
            </figcaption>
          )}
        </figure>
      )}

      <h3 className="font-serif text-[1.125rem] leading-snug font-normal">
        <Link
          to={`/wiki/${featured.slug}`}
          className="text-link visited:text-link-visited hover:underline"
        >
          {featured.title}
        </Link>
      </h3>

      <div className="mt-1 font-serif text-read leading-[1.6] text-ink">
        {body.length > 0 ? (
          body.map((block, index) => (
            <p key={index} className={index > 0 ? "mt-2" : undefined}>
              {block}
            </p>
          ))
        ) : (
          <p>{featured.title} is featured on the main page.</p>
        )}
      </div>

      <p className="mt-2 text-ui">
        <Link
          to={`/wiki/${featured.slug}`}
          className="text-link hover:underline"
        >
          Full article →
        </Link>
      </p>

      {recentlyFeatured.length > 0 && (
        <p className="mt-1.5 border-t border-rule-hair pt-1.5 text-ui text-ink-2">
          Recently featured:{" "}
          {recentlyFeatured.map((stub, index) => (
            <span key={stub.slug}>
              {index > 0 && <span aria-hidden="true"> · </span>}
              <Link
                to={`/wiki/${stub.slug}`}
                className="text-link visited:text-link-visited hover:underline"
              >
                {stub.title}
              </Link>
            </span>
          ))}
        </p>
      )}

      {/* The float is cleared so the panel's border cannot be crossed by a
          tall thumbnail on a narrow column. */}
      <div className="clear-both" />
    </div>
  );
}
