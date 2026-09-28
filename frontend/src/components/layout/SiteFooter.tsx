import { Link } from "react-router-dom";

import { CHANGES_FEED_URL } from "@/api/community";
import { API_BASE_URL } from "@/lib/api";

const REPOSITORY_URL = "https://github.com/JonasJavier/wikiverse";

/**
 * The site footer: licence lines and a single row of links, in the shell
 * colour, under a rule. It replaces the old marketing footer, whose "API docs"
 * link pointed at `http://localhost:8000` on the live site.
 */
export function SiteFooter() {
  return (
    <footer className="mt-12 border-t border-rule bg-shell print:hidden">
      <div className="mx-auto max-w-[81.5rem] space-y-3 px-4 py-8 text-2xs text-ink-2 sm:px-6 tools:px-8">
        <p className="max-w-[48rem] leading-relaxed">
          Article text is available under the{" "}
          <a
            href="https://creativecommons.org/licenses/by/4.0/"
            rel="license noreferrer"
            target="_blank"
            className="text-link hover:text-link-hover"
          >
            Creative Commons Attribution 4.0
          </a>{" "}
          licence; images carry the licence stated in their credit line. The
          software is released under the MIT licence. Wikiverse is an
          independent portfolio project and is not affiliated with Wikipedia or
          the Wikimedia Foundation.
        </p>
        <nav aria-label="Footer">
          <ul className="flex flex-wrap gap-x-5 gap-y-1">
            <FooterLink to="/about">About Wikiverse</FooterLink>
            <FooterLink to="/changes">Recent changes</FooterLink>
            <FooterLink to="/categories">Categories</FooterLink>
            <FooterAnchor href={`${API_BASE_URL}/docs/`}>API documentation</FooterAnchor>
            <FooterAnchor href={CHANGES_FEED_URL}>RSS feed</FooterAnchor>
            <FooterAnchor href={REPOSITORY_URL} external>
              Source code
            </FooterAnchor>
          </ul>
        </nav>
      </div>
    </footer>
  );
}

function FooterLink({ to, children }: { to: string; children: string }) {
  return (
    <li>
      <Link to={to} className="text-link hover:text-link-hover">
        {children}
      </Link>
    </li>
  );
}

function FooterAnchor({
  href,
  external,
  children,
}: {
  href: string;
  external?: boolean;
  children: string;
}) {
  return (
    <li>
      <a
        href={href}
        className="text-link hover:text-link-hover"
        {...(external ? { target: "_blank", rel: "noreferrer" } : {})}
      >
        {children}
      </a>
    </li>
  );
}
