import { useEffect } from "react";

/**
 * The exact strings from DECISIONS §14. These are asserted by tests; do not
 * "improve" the dash. `—` is U+2014 EM DASH, not a hyphen and not an en dash.
 */
export const SITE_NAME = "Wikiverse";
export const DEFAULT_TITLE = "Wikiverse — the open encyclopedia";
export const TITLE_SUFFIX = " — Wikiverse";

export const DEFAULT_DESCRIPTION =
  "Wikiverse is an open encyclopedia. Read, cite, discuss and edit articles across every discipline.";

/**
 * Compose a document title.
 *
 * `null`/`undefined`/empty → the site default. Anything else →
 * `` `${page} — Wikiverse` ``. A page whose title already ends in the suffix is
 * passed through unchanged, so `useDocumentMeta({ title: DEFAULT_TITLE })`
 * cannot produce "Wikiverse — the open encyclopedia — Wikiverse".
 */
export function documentTitle(page?: string | null): string {
  const trimmed = page?.trim();
  if (!trimmed) return DEFAULT_TITLE;
  if (trimmed === DEFAULT_TITLE || trimmed.endsWith(TITLE_SUFFIX)) return trimmed;
  return `${trimmed}${TITLE_SUFFIX}`;
}

export interface DocumentMeta {
  /**
   * The page name, WITHOUT the site suffix — the hook adds it. Omit it (or pass
   * `null`) on the main page to get `Wikiverse — the open encyclopedia`.
   */
  title?: string | null;
  /** Meta description. Falls back to the site description, never to nothing. */
  description?: string | null;
  /**
   * Absolute or root-relative canonical URL. Defaults to the current path
   * WITHOUT its query string, resolved against `VITE_PUBLIC_BASE_URL` when that
   * is set (so a canonical emitted from a preview deploy still points at
   * production) and against the current origin otherwise.
   */
  canonical?: string | null;
  /** e.g. `"noindex"` on Search and Diff, which must not be indexed. */
  robots?: string | null;
  /** Open Graph / Twitter image. Absolute URL. */
  image?: string | null;
  imageAlt?: string | null;
  /** `"website"` on the main page, `"article"` on an article. */
  type?: "website" | "article";
}

function publicBase(): string {
  const configured = import.meta.env.VITE_PUBLIC_BASE_URL?.trim();
  if (configured) return configured.replace(/\/+$/, "");
  if (typeof window !== "undefined") return window.location.origin;
  return "";
}

function absolute(url: string): string {
  if (/^https?:\/\//i.test(url)) return url;
  return `${publicBase()}${url.startsWith("/") ? url : `/${url}`}`;
}

/**
 * Upsert a `<meta>` or `<link>` in `<head>`, keyed by an attribute selector.
 *
 * Elements this hook creates are stamped `data-dm=""` so they are
 * distinguishable from the static tags `index.html` ships. Nothing is ever
 * removed: every route sets all four values, so the last route to render wins
 * and there is no window in which a stale description survives. Removing on
 * unmount is what produces the classic bug where navigating A → B tears down
 * A's tags *after* B has installed its own.
 */
function upsert(
  tag: "meta" | "link",
  keyAttr: string,
  keyValue: string,
  valueAttr: string,
  value: string | null,
): void {
  const selector = `${tag}[${keyAttr}="${keyValue}"]`;
  let el = document.head.querySelector<HTMLElement>(selector);

  if (value === null) {
    // Only ever retract a tag this hook created; index.html's own stay.
    if (el?.dataset.dm !== undefined) el.remove();
    return;
  }

  if (!el) {
    el = document.createElement(tag);
    el.setAttribute(keyAttr, keyValue);
    el.dataset.dm = "";
    document.head.appendChild(el);
  }
  el.setAttribute(valueAttr, value);
}

function meta(name: string, value: string | null): void {
  upsert("meta", "name", name, "content", value);
}

function og(property: string, value: string | null): void {
  upsert("meta", "property", property, "content", value);
}

/**
 * Set `document.title`, the meta description and the canonical link for a page.
 *
 * Every route calls it — a route that does not is a bug, and it is the
 * highest-value SEO fix in the frontend after the footer. Dependency-free by
 * design: no react-helmet, no context, no provider. Roughly 40 lines of DOM.
 */
export function useDocumentMeta({
  title,
  description,
  canonical,
  robots,
  image,
  imageAlt,
  type = "website",
}: DocumentMeta = {}): void {
  const resolvedTitle = documentTitle(title);
  const resolvedDescription = description?.trim() || DEFAULT_DESCRIPTION;

  useEffect(() => {
    document.title = resolvedTitle;

    const url = absolute(
      canonical?.trim() ||
        (typeof window === "undefined" ? "/" : window.location.pathname),
    );

    meta("description", resolvedDescription);
    meta("robots", robots?.trim() || null);
    upsert("link", "rel", "canonical", "href", url);

    og("og:site_name", SITE_NAME);
    og("og:title", resolvedTitle);
    og("og:description", resolvedDescription);
    og("og:url", url);
    og("og:type", type);
    og("og:image", image ? absolute(image) : null);
    og("og:image:alt", image ? (imageAlt?.trim() || null) : null);

    meta("twitter:card", image ? "summary_large_image" : "summary");
    meta("twitter:title", resolvedTitle);
    meta("twitter:description", resolvedDescription);
  }, [
    resolvedTitle,
    resolvedDescription,
    canonical,
    robots,
    image,
    imageAlt,
    type,
  ]);
}
