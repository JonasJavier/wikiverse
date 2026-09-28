import { screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { renderWithProviders } from "@/test/render";
import type { Infobox as InfoboxData } from "@/lib/types";
import { Infobox } from "./Infobox";
import { LeadImage } from "./LeadImage";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

const curie: InfoboxData = {
  subtitle: "Physicist and chemist",
  rows: [
    { kind: "header", value: "Personal details" },
    { kind: "row", label: "Born", value: "7 November 1867, *Warsaw*" },
    { kind: "row", label: "Field", value: "[[Physics]] and [[Chemistry|chemistry]]" },
    { kind: "full", value: "Nobel laureate <script>alert(1)</script>" },
  ],
};

function leadImage(credit: string, extra: Partial<Parameters<typeof LeadImage>[0]> = {}) {
  return (
    <LeadImage
      url="https://upload.wikimedia.org/curie.jpg"
      alt="Marie Curie in her laboratory"
      caption="Curie in 1903"
      credit={credit}
      license="Public domain"
      sourceUrl="https://commons.wikimedia.org/wiki/File:Curie.jpg"
      {...extra}
    />
  );
}

describe("Infobox (DECISIONS §1)", () => {
  it("renders nothing without rows or an image", () => {
    const { container } = renderWithProviders(<Infobox infobox={null} title="Marie Curie" />);
    expect(container).toBeEmptyDOMElement();
    const empty = renderWithProviders(<Infobox infobox={{}} title="Marie Curie" />);
    expect(empty.container).toBeEmptyDOMElement();
  });

  it("falls back to the article title and shows the subtitle", () => {
    const { container } = renderWithProviders(<Infobox infobox={curie} title="Marie Curie" />);
    const caption = container.querySelector("caption");
    expect(caption).toHaveTextContent("Marie Curie");
    expect(caption).toHaveTextContent("Physicist and chemist");
  });

  it("prefers infobox.title over the article title", () => {
    const { container } = renderWithProviders(
      <Infobox infobox={{ ...curie, title: "Maria Skłodowska-Curie" }} title="Marie Curie" />,
    );
    expect(container.querySelector("caption")).toHaveTextContent("Maria Skłodowska-Curie");
  });

  it("renders the three row kinds", () => {
    const { container } = renderWithProviders(<Infobox infobox={curie} title="Marie Curie" />);

    const header = container.querySelector("th.infobox-header");
    expect(header).toHaveTextContent("Personal details");
    expect(header).toHaveAttribute("colspan", "2");

    const labels = [...container.querySelectorAll("th.infobox-label")];
    expect(labels.map((th) => th.textContent)).toEqual(["Born", "Field"]);
    expect(labels[0]).toHaveAttribute("scope", "row");
    expect(container.querySelectorAll("td.infobox-data")).toHaveLength(2);

    const full = container.querySelector("td.infobox-full-data");
    expect(full).toHaveAttribute("colspan", "2");
    expect(full).toHaveTextContent("Nobel laureate");
  });

  it("resolves wikilinks and emphasis in values, and strips raw HTML", () => {
    const { container } = renderWithProviders(<Infobox infobox={curie} title="Marie Curie" />);
    expect(screen.getByRole("link", { name: "Physics" })).toHaveAttribute("href", "/wiki/physics");
    expect(screen.getByRole("link", { name: "chemistry" })).toHaveAttribute(
      "href",
      "/wiki/chemistry",
    );
    expect(container.querySelector("em")).toHaveTextContent("Warsaw");
    expect(container.querySelector("script")).toBeNull();
    // Values are table-cell content, never paragraphs.
    expect(container.querySelector("td p")).toBeNull();
  });

  it("renders an infobox with only an image", () => {
    const { container } = renderWithProviders(
      <Infobox infobox={null} title="Marie Curie" image={leadImage("Henri Manuel")} />,
    );
    expect(within(container).getByRole("img")).toHaveAttribute(
      "alt",
      "Marie Curie in her laboratory",
    );
  });
});

describe("LeadImage credit line (DECISIONS §1 attribution)", () => {
  it("renders the credit, linked to the source, with the licence", () => {
    const { container } = renderWithProviders(
      <Infobox infobox={curie} title="Marie Curie" image={leadImage("Henri Manuel")} />,
    );
    const credit = screen.getByRole("link", { name: "Henri Manuel" });
    expect(credit).toHaveAttribute("href", "https://commons.wikimedia.org/wiki/File:Curie.jpg");
    expect(credit).toHaveAttribute("rel", expect.stringContaining("noopener"));
    expect(container).toHaveTextContent("Public domain");
    expect(container).toHaveTextContent("Curie in 1903");
  });

  it("renders an unlinked credit when there is no source URL", () => {
    renderWithProviders(leadImage("Henri Manuel", { sourceUrl: "" }));
    expect(screen.getByText("Henri Manuel", { exact: false })).toBeInTheDocument();
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("renders no credit line when the credit is empty", () => {
    const { container } = renderWithProviders(leadImage(""));
    expect(container).not.toHaveTextContent("Public domain");
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("renders the figure variant with the credit in the figcaption", () => {
    const { container } = renderWithProviders(leadImage("Henri Manuel", { variant: "figure" }));
    expect(container.querySelector("figure figcaption")).toHaveTextContent("Henri Manuel");
  });

  it("renders nothing without a URL", () => {
    const { container } = renderWithProviders(leadImage("Henri Manuel", { url: "" }));
    expect(container).toBeEmptyDOMElement();
  });
});
