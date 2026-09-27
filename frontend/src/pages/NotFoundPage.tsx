import type { FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useSuggest } from "@/api/search";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Field";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";

export interface NotFoundPageProps {
  /**
   * The exact title, when the caller knows it — `ArticlePage` does, for a slug
   * that resolved to a 404 after a redirect lookup.
   */
  title?: string;
  /** The slug that was not found. Defaults to the last segment of the URL. */
  slug?: string;
}

/**
 * Words a title keeps in lower case unless they open it. Without this,
 * `on-the-origin-of-species` reads `On The Origin Of Species`, which is not how
 * a reference work sets a title.
 */
const MINOR_WORDS = new Set([
  "a",
  "an",
  "and",
  "as",
  "at",
  "but",
  "by",
  "for",
  "from",
  "in",
  "nor",
  "of",
  "on",
  "or",
  "the",
  "to",
  "vs",
  "with",
]);

/** `"marie-curie"` -> `"Marie Curie"`. A guess, and the best one available. */
function titleFromSlug(slug: string): string {
  const words = slug.replace(/[-_]+/g, " ").trim().split(/\s+/).filter(Boolean);
  if (words.length === 0) return "";

  return words
    .map((word, index) => {
      const lower = word.toLocaleLowerCase();
      if (index > 0 && MINOR_WORDS.has(lower)) return lower;
      return lower.charAt(0).toLocaleUpperCase() + lower.slice(1);
    })
    .join(" ");
}

/**
 * 404 / missing page — ONE component with two entry points: an unmatched route,
 * and `/wiki/:slug` answering 404.
 *
 * The giant accent-coloured `404` numeral is gone. A wiki does not apologise
 * for a page that has not been written; it tells you the title is free and
 * hands you the pen. The three ways out are the wiki idiom, in order: create
 * it, search for it, or pick one of the titles that nearly matched.
 *
 * "Similar titles" comes from `GET /api/search/suggest/` — the typeahead
 * endpoint, which on PostgreSQL answers a misspelling through `pg_trgm`.
 * DECISIONS §2 is explicit that no separate similar-titles endpoint exists.
 *
 * An SPA cannot set an HTTP status, so `noindex` is how the 404 is signalled to
 * a crawler. That is a documented limitation, not an oversight.
 */
export function NotFoundPage({ title, slug }: NotFoundPageProps = {}) {
  const location = useLocation();
  const navigate = useNavigate();

  const segments = location.pathname.split("/").filter(Boolean);
  const resolvedSlug = slug ?? segments[segments.length - 1] ?? "";
  const displayTitle = title ?? titleFromSlug(resolvedSlug);
  const heading = displayTitle || "Page not found";
  // The suggest endpoint wants words, not a slug: "marie curie", not
  // "marie-curie", or the trigram match has one long token to work with.
  const term = displayTitle || resolvedSlug.replace(/[-_]+/g, " ");

  const { data: suggestions, isLoading } = useSuggest(term);
  const similar = suggestions?.filter((s) => s.title !== displayTitle) ?? [];

  useDocumentMeta({
    title: heading,
    description: `Wikiverse does not have an article titled “${heading}”. Create it, or search for it.`,
    robots: "noindex",
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const submitted = String(
      new FormData(event.currentTarget).get("q") ?? "",
    ).trim();
    if (submitted) navigate(`/search?q=${encodeURIComponent(submitted)}`);
  }

  return (
    <WikiFrame>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          {heading}
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          Wikiverse does not have an article with this exact title.
        </p>
      </div>

      <div className="mt-4 max-w-[34rem] text-read">
        <p>
          You can{" "}
          {displayTitle ? (
            <Link
              to={`/new?title=${encodeURIComponent(displayTitle)}`}
              title={`${displayTitle} (page does not exist)`}
              className="font-semibold text-link-red hover:underline"
            >
              create this page
            </Link>
          ) : (
            <Link to="/new" className="text-link hover:underline">
              create a page
            </Link>
          )}
          , search the full text of every article for{" "}
          <Link
            to={`/search?q=${encodeURIComponent(term)}`}
            className="text-link hover:underline"
          >
            “{term}”
          </Link>
          , or{" "}
          <Link to="/browse" className="text-link hover:underline">
            browse the whole encyclopedia
          </Link>
          .
        </p>

        <form role="search" onSubmit={handleSubmit} className="mt-4 flex gap-2">
          <label htmlFor="notfound-q" className="sr-only">
            Search Wikiverse
          </label>
          <Input
            id="notfound-q"
            name="q"
            type="search"
            defaultValue={term}
            placeholder="Search Wikiverse…"
            autoComplete="off"
            className="h-9"
          />
          <Button
            type="submit"
            variant="secondary"
            size="lg"
            className="h-9 shrink-0"
          >
            Search
          </Button>
        </form>

        <h2 className="mt-6 font-serif text-h2 font-normal text-ink">
          Similar titles
        </h2>
        <hr className="mt-1 border-0 border-t border-rule-hair" />

        <div aria-busy={isLoading} className="mt-2">
          {isLoading ? (
            <ul>
              {Array.from({ length: 4 }, (_, index) => (
                <li key={index} className="py-1.5">
                  <Skeleton className="h-5 w-1/2" />
                </li>
              ))}
            </ul>
          ) : similar.length === 0 ? (
            <p className="text-ui text-ink-2">
              No existing title is close to this one.
            </p>
          ) : (
            <ul className="text-read">
              {similar.map((suggestion) => (
                <li key={suggestion.slug} className="py-1">
                  <Link
                    to={`/wiki/${suggestion.slug}`}
                    className="text-link visited:text-link-visited hover:underline"
                  >
                    {suggestion.title}
                  </Link>
                  {suggestion.short_description && (
                    <span className="text-ink-2">
                      , {suggestion.short_description}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </WikiFrame>
  );
}
