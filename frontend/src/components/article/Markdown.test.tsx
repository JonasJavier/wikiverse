import { screen } from "@testing-library/react";
import type { ReactElement } from "react";
import { describe, expect, it, vi } from "vitest";

import { renderWithProviders } from "@/test/render";
import type { Reference } from "@/lib/types";
import { Markdown, MarkdownInline } from "./Markdown";
import {
  buildFootnoteScope,
  extractHeadings,
  FootnoteContext,
  LinkResolutionContext,
  wikiSlug,
  type FootnoteSource,
  type LinkResolver,
} from "./markdownUtils";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

function reference(key: string, order: number): Reference {
  return {
    key,
    order,
    title: key,
    url: "",
    authors: "",
    publisher: "",
    published_on: "",
    accessed_on: null,
    identifier: "",
    quote: "",
  };
}

/** Every title in `red` is an unwritten article; everything else exists. */
function resolverWithRedLinks(...red: string[]): LinkResolver {
  return (title) => ({ slug: wikiSlug(title), exists: !red.includes(title) });
}

function withFootnotes(ui: ReactElement, references: Reference[], sources: FootnoteSource[]) {
  return (
    <FootnoteContext.Provider value={buildFootnoteScope(references, sources)}>
      {ui}
    </FootnoteContext.Provider>
  );
}

describe("Markdown — raw HTML is never rendered (DECISIONS §0.5, skipHtml)", () => {
  it("drops inline <script> and <img onerror>", () => {
    const { container } = renderWithProviders(
      <Markdown content={'Hello <script>alert(1)</script> and <img src="x" onerror="alert(2)"> world'} />,
    );
    expect(container.querySelector("script")).toBeNull();
    expect(container.querySelector("img")).toBeNull();
    expect(container.innerHTML).not.toContain("onerror");
    expect(container).toHaveTextContent("Hello");
    expect(container).toHaveTextContent("world");
  });

  it("drops block-level HTML entirely", () => {
    const { container } = renderWithProviders(
      <Markdown content={'<div onclick="steal()">boxed</div>\n\nAfter.'} />,
    );
    expect(container.querySelector("[onclick]")).toBeNull();
    expect(container.innerHTML).not.toContain("steal");
    expect(screen.getByText("After.")).toBeInTheDocument();
  });

  it("neutralises javascript: links", () => {
    const { container } = renderWithProviders(<Markdown content="[click](javascript:alert(1))" />);
    expect(container.querySelector('a[href^="javascript"]')).toBeNull();
    expect(screen.getByText("click")).toBeInTheDocument();
  });

  it("renders inline values with no raw HTML either", () => {
    const { container } = renderWithProviders(
      <MarkdownInline content={'*1867* <b onmouseover="x()">Warsaw</b>'} />,
    );
    expect(container.querySelector("b")).toBeNull();
    expect(container.querySelector("em")).toHaveTextContent("1867");
    expect(container.querySelector("p")).toBeNull();
    expect(container).toHaveTextContent("Warsaw");
  });
});

describe("Markdown — wikilinks", () => {
  it("renders [[Title]] and [[Title|text]] as internal links", () => {
    renderWithProviders(
      <Markdown content="Light drives [[Photosynthesis]] in [[Chloroplast|chloroplasts]]." />,
    );
    expect(screen.getByRole("link", { name: "Photosynthesis" })).toHaveAttribute(
      "href",
      "/wiki/photosynthesis",
    );
    expect(screen.getByRole("link", { name: "chloroplasts" })).toHaveAttribute(
      "href",
      "/wiki/chloroplast",
    );
  });

  it("carries a section anchor through to the href", () => {
    renderWithProviders(<Markdown content="See [[Euclid#Early life|his youth]]." />);
    expect(screen.getByRole("link", { name: "his youth" })).toHaveAttribute(
      "href",
      "/wiki/euclid#early-life",
    );
  });

  it("renders a red link to /new?title=<Title> with .is-redlink", () => {
    renderWithProviders(
      <LinkResolutionContext.Provider value={resolverWithRedLinks("Erdős number")}>
        <Markdown content="Compare [[Erdős number]] with [[Graph theory]]." />
      </LinkResolutionContext.Provider>,
    );
    const red = screen.getByRole("link", { name: "Erdős number" });
    expect(red).toHaveAttribute("href", "/new?title=Erd%C5%91s%20number");
    expect(red).toHaveClass("is-redlink");
    expect(red).toHaveAttribute("title", "Erdős number (page does not exist)");

    const blue = screen.getByRole("link", { name: "Graph theory" });
    expect(blue).toHaveAttribute("href", "/wiki/graph-theory");
    expect(blue).not.toHaveClass("is-redlink");
  });

  it("leaves wikilinks inside code, and escaped ones, literal", () => {
    const { container } = renderWithProviders(
      <Markdown content={"Inline `[[Not a link]]`.\n\n```\n[[Also not]]\n```\n\n\\[[Escaped]]"} />,
    );
    expect(container.querySelectorAll("a")).toHaveLength(0);
    expect(container).toHaveTextContent("[[Not a link]]");
    expect(container).toHaveTextContent("[[Also not]]");
    expect(container).toHaveTextContent("[[Escaped]]");
  });

  it("marks external links as external and opens them safely", () => {
    renderWithProviders(<Markdown content="[Source](https://example.org/paper)" />);
    const link = screen.getByRole("link", { name: "Source" });
    expect(link).toHaveClass("external");
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", expect.stringContaining("noopener"));
  });
});

describe("Markdown — footnote markers", () => {
  const references = [reference("a", 0), reference("b", 1)];

  it("renders [^key] as cite_ref-{key}-{n} pointing at cite_note-{key}", () => {
    const content = "First[^a] again[^a] other[^b].";
    const { container } = renderWithProviders(
      withFootnotes(<Markdown content={content} sourceId="content" />, references, [
        { id: "content", text: content },
      ]),
    );
    const markers = [...container.querySelectorAll("sup.reference")];
    expect(markers.map((m) => m.id)).toEqual(["cite_ref-a-0", "cite_ref-a-1", "cite_ref-b-0"]);
    expect(markers.map((m) => m.textContent)).toEqual(["[1]", "[1]", "[2]"]);
    expect(markers[0].querySelector("a")).toHaveAttribute("href", "#cite_note-a");
    expect(markers[2].querySelector("a")).toHaveAttribute("href", "#cite_note-b");
  });

  it("continues the occurrence index after markers in an earlier source", () => {
    const content = "Body[^a].";
    const { container } = renderWithProviders(
      withFootnotes(<Markdown content={content} sourceId="content" />, references, [
        { id: "infobox.0", text: "Born[^a]" },
        { id: "content", text: content },
      ]),
    );
    expect(container.querySelector("sup.reference")?.id).toBe("cite_ref-a-1");
  });

  it("renders an unresolved marker visibly as [?]", () => {
    const { container } = renderWithProviders(
      withFootnotes(<Markdown content="Claim[^missing]." />, references, []),
    );
    const marker = container.querySelector("sup.reference");
    expect(marker).toHaveTextContent("[?]");
    expect(marker).toHaveAttribute("title", expect.stringContaining("missing"));
    expect(marker?.querySelector("a")).toBeNull();
  });
});

describe("Markdown — headings", () => {
  it("gives every heading the same id the table of contents computes", () => {
    const content = [
      "## History",
      "Text.",
      "## History",
      "### The [[Pythagorean theorem|theorem]] in [[Greece]]",
      "## Early life[^a]",
      "## Gödel's theorem",
      "## Links to [[Euclid#Elements]]",
    ].join("\n\n");

    const { container } = renderWithProviders(
      withFootnotes(<Markdown content={content} sourceId="content" />, [reference("a", 0)], [
        { id: "content", text: content },
      ]),
    );

    const rendered = [...container.querySelectorAll("h2, h3")].map((h) => h.id);
    expect(rendered).toEqual(extractHeadings(content).map((h) => h.id));
    expect(rendered).toEqual([
      "history",
      "history-2",
      "the-theorem-in-greece",
      "early-life",
      "godels-theorem",
      "links-to-euclidelements",
    ]);
  });

  it("demotes a body # H1 to an h2 and adds a permalink", () => {
    const { container } = renderWithProviders(<Markdown content="# Stray title" />);
    expect(container.querySelector("h1")).toBeNull();
    const heading = container.querySelector("h2");
    expect(heading).toHaveAttribute("id", "stray-title");
    expect(heading?.querySelector("a.heading-anchor")).toHaveAttribute("href", "#stray-title");
  });

  it("marks only the first top-level paragraph as the lead", () => {
    const { container } = renderWithProviders(
      <Markdown content={"**Photosynthesis** is a process.\n\nSecond paragraph."} lead />,
    );
    const paragraphs = container.querySelectorAll("p");
    expect(paragraphs[0]).toHaveClass("lead");
    expect(paragraphs[1]).not.toHaveClass("lead");
  });
});
