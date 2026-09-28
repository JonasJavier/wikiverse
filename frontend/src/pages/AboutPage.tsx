import type { ReactNode } from "react";
import { Link } from "react-router-dom";

import { useSiteStats } from "@/api/articles";
import { Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { API_BASE_URL } from "@/lib/api";
import { formatNumber } from "@/lib/utils";

const REPOSITORY_URL = "https://github.com/JonasJavier/wikiverse";

/**
 * `/about` — what the site is, how it is written and how it is built.
 *
 * Written in the encyclopedia's own register (serif prose, sections under
 * rules) rather than as a marketing page, and honest about scope: a portfolio
 * project with a partial corpus whose red links are deliberate.
 */
export function AboutPage() {
  const { data: stats } = useSiteStats();

  useDocumentMeta({
    title: "About Wikiverse",
    description:
      "Wikiverse is an open encyclopedia and a full-stack portfolio project: Django REST Framework, PostgreSQL full-text search, React and TypeScript.",
    canonical: "/about",
  });

  return (
    <WikiFrame rail={<Sidebar />}>
      <article className="pt-4">
        <h1 className="font-serif text-h1 font-normal text-balance text-ink">
          About Wikiverse
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">From Wikiverse, the open encyclopedia</p>

        <div className="article-prose mt-4">
          <p>
            <b>Wikiverse</b> is an open, general-interest encyclopedia that anyone
            with an account can edit. It is also a portfolio project: a working
            model of the machinery behind a wiki — revision history, diffs, talk
            pages, watchlists, red links, citations and full-text search — built
            from scratch rather than on top of MediaWiki.
          </p>
          {stats && (
            <p>
              The encyclopedia currently holds{" "}
              <b>{formatNumber(stats.articles)}</b> articles in{" "}
              {formatNumber(stats.categories)} categories, with{" "}
              {formatNumber(stats.revisions)} revisions by{" "}
              {formatNumber(stats.contributors)} contributors.
            </p>
          )}

          <h2>The corpus</h2>
          <p>
            The seed articles span mathematics, physics, astronomy, chemistry,
            the life sciences, medicine, the Earth sciences, geography and
            computing; the history, philosophy, language and arts categories are
            planned and still being written. Each article is in a neutral
            encyclopedic register, carries references to
            published sources, and was checked for factual accuracy before it
            was included. The article text is licensed under{" "}
            <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noreferrer" target="_blank">
              CC BY 4.0
            </a>
            ; images come from Wikimedia Commons under the licence named in
            their credit line.
          </p>
          <p>
            Links shown in red point to planned articles that have not been
            written yet. They are kept on purpose, exactly as on Wikipedia:
            following one opens the editor with the title already filled in.
          </p>

          <h2>Contributing</h2>
          <p>
            Reading needs no account. To write, <Link to="/register">create an
            account</Link>, then use <Link to="/new">Create an article</Link> or
            the <i>Edit</i> tab on any page. Every save becomes a revision that
            can be compared with any other on the page history, and discussion
            about an article belongs on its <i>Talk</i> page. The{" "}
            <Link to="/changes">recent changes</Link> feed shows every edit as it
            happens.
          </p>

          <h2>How it is built</h2>
          <ul>
            <Item label="API">
              Django and Django REST Framework, documented with OpenAPI (
              <a href={`${API_BASE_URL}/docs/`}>interactive reference</a>).
            </Item>
            <Item label="Search">
              PostgreSQL full-text search with weighted ranking, highlighted
              snippets and trigram typo tolerance, maintained by a database
              trigger.
            </Item>
            <Item label="Data">
              PostgreSQL for storage and Redis for caching and rate limiting.
            </Item>
            <Item label="Interface">
              React, TypeScript and Tailwind CSS, with self-hosted typefaces and a
              strict Content Security Policy.
            </Item>
            <Item label="Hosting">
              Docker images on Railway: nginx serves the interface and proxies
              the API, and search-engine crawlers receive server-rendered Open
              Graph pages.
            </Item>
          </ul>
          <p>
            The source code is on{" "}
            <a href={REPOSITORY_URL} target="_blank" rel="noreferrer">
              GitHub
            </a>{" "}
            under the MIT licence.
          </p>

          <h2>Disclaimer</h2>
          <p>
            Wikiverse is an independent project. It is not affiliated with,
            endorsed by or connected to Wikipedia or the Wikimedia Foundation.
          </p>
        </div>
      </article>
    </WikiFrame>
  );
}

function Item({ label, children }: { label: string; children: ReactNode }) {
  return (
    <li>
      <b>{label}.</b> {children}
    </li>
  );
}
