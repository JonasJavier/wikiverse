import { screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { wikiSlug, type LinkResolver } from "@/components/article/markdownUtils";
import { renderWithProviders } from "@/test/render";
import { WikiText } from "./WikiText";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

function redFor(...titles: string[]): LinkResolver {
  return (title) => ({ slug: wikiSlug(title), exists: titles.includes(title) ? false : true });
}

describe("WikiText (main-page hooks)", () => {
  it("renders [[Title]] and [[Title|text]] as internal links", () => {
    renderWithProviders(
      <WikiText>{"… that [[Marie Curie]] won two [[Nobel Prize|Nobel Prizes]]?"}</WikiText>,
    );
    const curie = screen.getByRole("link", { name: "Marie Curie" });
    expect(curie).toHaveAttribute("href", "/wiki/marie-curie");
    expect(curie).toHaveAttribute("title", "Marie Curie");
    expect(screen.getByRole("link", { name: "Nobel Prizes" })).toHaveAttribute(
      "href",
      "/wiki/nobel-prize",
    );
  });

  it("renders a red link to /new?title=<Title> with .is-redlink", () => {
    renderWithProviders(
      <WikiText resolve={redFor("Erdős number")}>{"… that [[Erdős number|Erdős]] is small?"}</WikiText>,
    );
    const link = screen.getByRole("link", { name: "Erdős" });
    expect(link).toHaveAttribute("href", "/new?title=Erd%C5%91s%20number");
    expect(link).toHaveClass("is-redlink");
    expect(link).toHaveAttribute("title", "Erdős number (page does not exist)");
  });

  it("keeps a red-link title with parentheses intact", () => {
    renderWithProviders(
      <WikiText resolve={redFor("Mercury (planet)")}>{"[[Mercury (planet)]] is closest."}</WikiText>,
    );
    const link = screen.getByRole("link", { name: "Mercury (planet)" });
    expect(new URL(link.getAttribute("href") ?? "", "http://x").searchParams.get("title")).toBe(
      "Mercury (planet)",
    );
  });

  it("carries an anchor onto a blue link", () => {
    renderWithProviders(<WikiText>{"[[Euclid#Elements|the Elements]]"}</WikiText>);
    expect(screen.getByRole("link", { name: "the Elements" })).toHaveAttribute(
      "href",
      "/wiki/euclid#elements",
    );
  });

  it("strips raw HTML (skipHtml) and blocks javascript: links", () => {
    const { container } = renderWithProviders(
      <WikiText>{'<img src=x onerror="alert(1)"><script>alert(2)</script> [x](javascript:alert(3)) **ok**'}</WikiText>,
    );
    expect(container.querySelector("img")).toBeNull();
    expect(container.querySelector("script")).toBeNull();
    expect(container.querySelector('a[href^="javascript"]')).toBeNull();
    expect(container.querySelector("strong")).toHaveTextContent("ok");
  });

  it("renders inline — no <p> inside the list item it sits in", () => {
    const { container } = renderWithProviders(<WikiText>{"One sentence."}</WikiText>);
    expect(container.querySelector("p")).toBeNull();
    expect(container).toHaveTextContent("One sentence.");
  });

  it("opens an external link in a new tab, safely", () => {
    renderWithProviders(<WikiText>{"[source](https://example.org)"}</WikiText>);
    const link = screen.getByRole("link", { name: "source" });
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", expect.stringContaining("noopener"));
  });
});
