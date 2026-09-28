import { screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { renderWithProviders } from "@/test/render";
import type { Reference } from "@/lib/types";
import { buildFootnoteScope, FootnoteContext } from "./markdownUtils";
import { References } from "./References";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

function ref(key: string, order: number, patch: Partial<Reference> = {}): Reference {
  return {
    key,
    order,
    title: `Title ${key}`,
    url: "",
    authors: "",
    publisher: "",
    published_on: "",
    accessed_on: null,
    identifier: "",
    quote: "",
    ...patch,
  };
}

const references = [
  ref("watson1953", 1, {
    title: "Molecular structure of nucleic acids",
    authors: "Watson, J. D.; Crick, F. H. C.",
    published_on: "1953",
    publisher: "Nature",
    identifier: "doi:10.1038/171737a0",
    url: "https://www.nature.com/articles/171737a0",
    accessed_on: "2026-09-26",
  }),
  ref("curie1903", 0, { identifier: "ISBN 978-0-19-852663-6", quote: "Radium" }),
  ref("vaswani2017", 2, { identifier: "arXiv:1706.03762" }),
  ref("uncited", 3, { identifier: "OCLC 12345" }),
];

function renderReferences(body: string) {
  const scope = buildFootnoteScope(references, [{ id: "content", text: body }]);
  return renderWithProviders(
    <FootnoteContext.Provider value={scope}>
      <References references={references} />
    </FootnoteContext.Provider>,
  );
}

describe("References (DECISIONS §11, §14)", () => {
  const body = "a[^curie1903] b[^watson1953] c[^watson1953] d[^watson1953] e[^vaswani2017]";

  it("gives every entry the id cite_note-{key}, in `order`", () => {
    const { container } = renderReferences(body);
    expect([...container.querySelectorAll("ol.reflist > li")].map((li) => li.id)).toEqual([
      "cite_note-curie1903",
      "cite_note-watson1953",
      "cite_note-vaswani2017",
      "cite_note-uncited",
    ]);
    expect(screen.getByRole("heading", { level: 2, name: "References" })).toHaveAttribute(
      "id",
      "references",
    );
  });

  it("back-links a single citation with ^ to cite_ref-{key}-0", () => {
    const { container } = renderReferences(body);
    const links = container.querySelectorAll("#cite_note-curie1903 .mw-cite-backlink a");
    expect(links).toHaveLength(1);
    expect(links[0]).toHaveTextContent("^");
    expect(links[0]).toHaveAttribute("href", "#cite_ref-curie1903-0");
  });

  it("back-links a multiply cited source as ^ a b c", () => {
    const { container } = renderReferences(body);
    const letters = [...container.querySelectorAll("#cite_note-watson1953 a.backlink-letter")];
    expect(letters.map((a) => a.textContent?.trim())).toEqual(["a", "b", "c"]);
    expect(letters.map((a) => a.getAttribute("href"))).toEqual([
      "#cite_ref-watson1953-0",
      "#cite_ref-watson1953-1",
      "#cite_ref-watson1953-2",
    ]);
  });

  it("offers no backlink anchor for a source cited nowhere", () => {
    const { container } = renderReferences(body);
    expect(container.querySelectorAll("#cite_note-uncited .mw-cite-backlink a")).toHaveLength(0);
  });

  it("labels a DOI and links it to doi.org", () => {
    const { container } = renderReferences(body);
    const doi = container.querySelector("#cite_note-watson1953 .cite-doi");
    expect(doi).toHaveTextContent("doi:10.1038/171737a0");
    expect(doi?.querySelector("a")).toHaveAttribute("href", "https://doi.org/10.1038/171737a0");
  });

  it("labels an ISBN, unlinked, with a space after the prefix", () => {
    const { container } = renderReferences(body);
    const isbn = container.querySelector("#cite_note-curie1903 .cite-isbn");
    expect(isbn?.textContent).toBe("ISBN 978-0-19-852663-6");
    expect(isbn?.querySelector("a")).toBeNull();
  });

  it("labels an arXiv id and links it to arxiv.org", () => {
    const { container } = renderReferences(body);
    const arxiv = container.querySelector("#cite_note-vaswani2017 .cite-arxiv");
    expect(arxiv).toHaveTextContent("arXiv:1706.03762");
    expect(arxiv?.querySelector("a")).toHaveAttribute("href", "https://arxiv.org/abs/1706.03762");
  });

  it("prints an unrecognised identifier verbatim", () => {
    const { container } = renderReferences(body);
    expect(container.querySelector("#cite_note-uncited .cite-other")?.textContent).toBe(
      "OCLC 12345",
    );
  });

  it("renders the full citation, and 'Retrieved' on the stored calendar day", () => {
    const { container } = renderReferences(body);
    const cite = container.querySelector("#cite_note-watson1953 cite");
    expect(cite).toHaveTextContent("Watson, J. D.; Crick, F. H. C. (1953).");
    expect(cite).toHaveTextContent("Nature");
    // Tests run in UTC−4: a naive `new Date("2026-09-26")` would print the 25th.
    expect(cite).toHaveTextContent("Retrieved 26 September 2026");
    const title = screen.getByRole("link", { name: /Molecular structure of nucleic acids/ });
    expect(title).toHaveAttribute("href", "https://www.nature.com/articles/171737a0");
    expect(title).toHaveAttribute("target", "_blank");
  });

  it("shows a quote, and never nests a link inside the title link", () => {
    renderWithProviders(
      <References
        references={[
          ref("x", 0, {
            url: "https://example.org",
            title: "See [[Physics]] and [elsewhere](https://evil.example)",
            quote: "Radium",
          }),
        ]}
      />,
    );
    const title = screen.getByRole("link", { name: /See Physics and elsewhere/ });
    expect(title.querySelector("a")).toBeNull();
    expect(screen.getByText(/Radium/)).toBeInTheDocument();
  });

  it("renders nothing for an empty list", () => {
    const { container } = renderWithProviders(<References references={[]} />);
    expect(container).toBeEmptyDOMElement();
  });
});
