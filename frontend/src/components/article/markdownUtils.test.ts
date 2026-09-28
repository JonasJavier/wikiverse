import { describe, expect, it, vi } from "vitest";

import type { Reference } from "@/lib/types";
import {
  backlinkLetter,
  buildFootnoteScope,
  buildHeadingTree,
  citeNoteId,
  citeRefId,
  countFootnoteMarkers,
  createPageHref,
  createSlugger,
  extractHeadings,
  inlineToPlainText,
  optimisticResolver,
  parseIdentifier,
  parseWikiTarget,
  redLinkTitle,
  slugifyHeading,
  splitLead,
  wikiHref,
  wikiSlug,
} from "./markdownUtils";

// markdownUtils imports the article query hooks; nothing here may reach the network.
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

describe("wikiSlug (twin of the backend's wiki_slug)", () => {
  it.each([
    ["Photosynthesis", "photosynthesis"],
    ["Mercury (planet)", "mercury-planet"],
    ["Gödel's incompleteness theorems", "gödels-incompleteness-theorems"],
    ["Ελλάδα", "ελλάδα"],
    ["Erdős number", "erdős-number"],
    ["C++", "c-plus-plus"],
    ["C#", "c-sharp"],
    ["AT&T", "at-andt"],
    ["TCP/IP", "tcp-ip"],
    ["π", "pi"],
    ["  Leading and trailing  ", "leading-and-trailing"],
    ["-_Edge_-", "edge"],
  ])("%j → %j", (title, slug) => {
    expect(wikiSlug(title)).toBe(slug);
  });

  it("applies NFKC before lowercasing, so compatibility ligatures fold", () => {
    expect(wikiSlug("ﬁnance")).toBe("finance");
  });

  it("caps the slug at 220 characters without leaving a trailing hyphen", () => {
    const slug = wikiSlug(`${"a".repeat(219)} b`);
    expect(slug.length).toBeLessThanOrEqual(220);
    expect(slug.endsWith("-")).toBe(false);
  });
});

describe("slugifyHeading", () => {
  it.each([
    ["History", "history"],
    ["Gödel's theorem", "godels-theorem"],
    ["Ελλάδα", "ελλαδα"],
    ["  Early   life  ", "early-life"],
    ["C++ & you", "c-you"],
    ["Rise -- and fall", "rise-and-fall"],
  ])("%j → %j", (text, id) => {
    expect(slugifyHeading(text)).toBe(id);
  });

  it('falls back to "section" when nothing sluggable is left', () => {
    expect(slugifyHeading("!!!")).toBe("section");
    expect(slugifyHeading("")).toBe("section");
  });
});

describe("createSlugger", () => {
  it("de-duplicates repeated headings as -2, -3", () => {
    const slug = createSlugger();
    expect([slug("History"), slug("History"), slug("History")]).toEqual([
      "history",
      "history-2",
      "history-3",
    ]);
  });

  it("never collides with a heading that already carries the suffix", () => {
    const slug = createSlugger();
    const ids = [slug("History"), slug("History 2"), slug("History"), slug("History 2")];
    expect(ids).toEqual(["history", "history-2", "history-3", "history-2-2"]);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("keeps separate state per slugger", () => {
    const a = createSlugger();
    const b = createSlugger();
    a("Overview");
    expect(b("Overview")).toBe("overview");
  });
});

describe("inlineToPlainText", () => {
  it("uses a wikilink's display text, or its title", () => {
    expect(inlineToPlainText("The [[Pythagorean theorem|theorem]] today")).toBe(
      "The theorem today",
    );
    expect(inlineToPlainText("On [[Euclid]]")).toBe("On Euclid");
  });

  it("drops footnote markers and inline Markdown syntax", () => {
    expect(inlineToPlainText("*Early* **life**[^bio1] and `code`")).toBe("Early life and code");
    expect(inlineToPlainText("See [the paper](https://example.org)")).toBe("See the paper");
  });
});

describe("extractHeadings", () => {
  const body = [
    "Lead paragraph.",
    "",
    "## History",
    "### Early period",
    "#### Sources",
    "### Late period",
    "## History",
    "## Legacy ##",
    "# Not in the contents",
    "##### Too deep",
    "```",
    "## Inside a fence",
    "```",
  ].join("\n");

  it("numbers ##–#### headings the way the TOC prints them", () => {
    expect(extractHeadings(body).map((h) => [h.number, h.level, h.text])).toEqual([
      ["1", 2, "History"],
      ["1.1", 3, "Early period"],
      ["1.1.1", 4, "Sources"],
      ["1.2", 3, "Late period"],
      ["2", 2, "History"],
      ["3", 2, "Legacy"],
    ]);
  });

  it("gives duplicate headings distinct ids", () => {
    expect(extractHeadings(body).map((h) => h.id)).toEqual([
      "history",
      "early-period",
      "sources",
      "late-period",
      "history-2",
      "legacy",
    ]);
  });

  it("derives the id of a heading with a wikilink from its display text", () => {
    const [heading] = extractHeadings("## The [[Pythagorean theorem|theorem]] in [[Greece]]");
    expect(heading.text).toBe("The theorem in Greece");
    expect(heading.id).toBe("the-theorem-in-greece");
  });

  it("ignores footnote markers when deriving an id", () => {
    expect(extractHeadings("## Early life[^bio]")[0].id).toBe("early-life");
  });

  it("handles CRLF line endings", () => {
    expect(extractHeadings("## One\r\n## Two\r\n").map((h) => h.id)).toEqual(["one", "two"]);
  });
});

describe("splitLead", () => {
  it("splits at the first heading", () => {
    expect(splitLead("**Title** is a thing.\n\n## History\nText")).toEqual({
      lead: "**Title** is a thing.",
      body: "## History\nText",
    });
  });

  it("treats a body with no heading as all lead", () => {
    expect(splitLead("Only a lead.\n")).toEqual({ lead: "Only a lead.", body: "" });
  });

  it("does not split on a heading inside fenced code", () => {
    const text = "Lead\n```\n## not a heading\n```\nStill lead";
    expect(splitLead(text).body).toBe("");
  });
});

describe("buildHeadingTree", () => {
  it("nests by level and tolerates a skipped level", () => {
    const tree = buildHeadingTree(extractHeadings("## A\n### A1\n#### A1a\n## B\n#### B-deep"));
    expect(tree.map((n) => n.id)).toEqual(["a", "b"]);
    expect(tree[0].children[0].children[0].id).toBe("a1a");
    expect(tree[1].children.map((n) => n.id)).toEqual(["b-deep"]);
  });
});

describe("footnotes", () => {
  it("counts [^key] markers in first-appearance order, outside code", () => {
    const counts = countFootnoteMarkers(
      "A[^b] B[^a] C[^b] `[^a]`\n```\n[^a]\n```\nD[^c]",
    );
    expect(counts).toEqual({ b: 2, a: 1, c: 1 });
    expect(Object.keys(counts)).toEqual(["b", "a", "c"]);
  });

  it("numbers references by `order`, not array position", () => {
    const scope = buildFootnoteScope([reference("second", 1), reference("first", 0)], []);
    expect(scope.numbers).toEqual({ first: 1, second: 2 });
  });

  it("allocates marker indices across sources in DOM order", () => {
    const scope = buildFootnoteScope(
      [reference("a", 0), reference("b", 1)],
      [
        { id: "infobox.0", text: "Born 1867[^a]" },
        { id: "content", text: "Text[^a] more[^a] other[^b]" },
      ],
    );
    expect(scope.totals).toEqual({ a: 3, b: 1 });
    expect(scope.offsets).toEqual({ "infobox.0": { a: 0 }, content: { a: 1, b: 0 } });
  });

  it("uses the exact DECISIONS §14 id formats", () => {
    expect(citeNoteId("curie1903")).toBe("cite_note-curie1903");
    expect(citeRefId("curie1903", 0)).toBe("cite_ref-curie1903-0");
    expect(citeRefId("curie1903", 2)).toBe("cite_ref-curie1903-2");
  });

  it.each([
    [0, "a"],
    [1, "b"],
    [25, "z"],
    [26, "aa"],
    [27, "ab"],
  ])("backlink letter %i → %s", (n, letter) => {
    expect(backlinkLetter(n)).toBe(letter);
  });
});

describe("red links", () => {
  it("targets /new?title=<Title> with the title, not the slug", () => {
    expect(createPageHref("Erdős number")).toBe("/new?title=Erd%C5%91s%20number");
    const url = new URL(createPageHref("AT&T"), "http://x");
    expect(url.pathname).toBe("/new");
    expect(url.searchParams.get("title")).toBe("AT&T");
  });

  it("explains itself in the title attribute", () => {
    expect(redLinkTitle("Erdős number")).toBe("Erdős number (page does not exist)");
  });

  it("the fallback resolver reports existence as unknown", () => {
    expect(optimisticResolver("Mercury (planet)")).toEqual({
      slug: "mercury-planet",
      exists: undefined,
    });
  });
});

describe("parseWikiTarget", () => {
  it("parses [[Title]]", () => {
    expect(parseWikiTarget("Photosynthesis")).toEqual({
      title: "Photosynthesis",
      anchor: "",
      display: "Photosynthesis",
    });
  });

  it("parses [[Title|text]]", () => {
    expect(parseWikiTarget("Photosynthesis|the process")).toEqual({
      title: "Photosynthesis",
      anchor: "",
      display: "the process",
    });
  });

  it("parses [[Title#Section]] and [[Title#Section|text]]", () => {
    expect(parseWikiTarget("Euclid#Elements")).toEqual({
      title: "Euclid",
      anchor: "Elements",
      display: "Euclid#Elements",
    });
    expect(parseWikiTarget("Euclid#Elements|his book")?.display).toBe("his book");
  });

  it("collapses whitespace and falls back to the title for an empty display", () => {
    expect(parseWikiTarget("  Isaac   Newton |  ")).toEqual({
      title: "Isaac Newton",
      anchor: "",
      display: "Isaac Newton",
    });
  });

  it.each(["", "   ", "|text", "#Section"])("rejects %j", (raw) => {
    expect(parseWikiTarget(raw)).toBeNull();
  });

  it("builds /wiki/<slug> hrefs with a slugged anchor", () => {
    expect(wikiHref("euclid")).toBe("/wiki/euclid");
    expect(wikiHref("euclid", "Early life")).toBe("/wiki/euclid#early-life");
  });
});

describe("parseIdentifier (DECISIONS §11 prefix sniffing)", () => {
  it("recognises a DOI", () => {
    expect(parseIdentifier("doi:10.1038/nature12373")).toEqual({
      kind: "doi",
      label: "doi:",
      value: "10.1038/nature12373",
      href: "https://doi.org/10.1038/nature12373",
    });
  });

  it("recognises an ISBN, with or without a colon", () => {
    expect(parseIdentifier("ISBN 978-0-19-852663-6")).toMatchObject({
      kind: "isbn",
      label: "ISBN",
      value: "978-0-19-852663-6",
      href: null,
    });
    expect(parseIdentifier("isbn:0-19-852663-X")?.value).toBe("0-19-852663-X");
  });

  it("recognises an arXiv id", () => {
    expect(parseIdentifier("arXiv:1706.03762")).toEqual({
      kind: "arxiv",
      label: "arXiv:",
      value: "1706.03762",
      href: "https://arxiv.org/abs/1706.03762",
    });
  });

  it("passes anything else through unlabelled, and ignores blanks", () => {
    expect(parseIdentifier("OCLC 12345")).toEqual({
      kind: "other",
      label: "",
      value: "OCLC 12345",
      href: null,
    });
    expect(parseIdentifier("   ")).toBeNull();
  });
});
