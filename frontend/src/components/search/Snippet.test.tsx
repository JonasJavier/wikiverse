import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Snippet } from "./Snippet";

/** The highlighted runs, in order. The component highlights with `<b>`. */
function highlighted(container: HTMLElement): string[] {
  return [...container.querySelectorAll("b")].map((el) => el.textContent ?? "");
}

describe("Snippet (DECISIONS §3 — split on literal <mark> tokens)", () => {
  it("turns each <mark>…</mark> run into a highlight element", () => {
    const { container } = render(
      <Snippet text="The <mark>quick</mark> brown <mark>fox</mark> jumps" />,
    );
    expect(highlighted(container)).toEqual(["quick", "fox"]);
    expect(container).toHaveTextContent("The quick brown fox jumps");
    // The tokens themselves never reach the page, as text or as elements.
    expect(container.textContent).not.toContain("<mark>");
    expect(container.textContent).not.toContain("</mark>");
    expect(container.querySelector("mark")).toBeNull();
  });

  it("renders an escaped <script> as inert text", () => {
    const { container } = render(
      <Snippet text={"&lt;script&gt;alert(1)&lt;/script&gt; and <mark>more</mark>"} />,
    );
    expect(container.querySelector("script")).toBeNull();
    expect(container).toHaveTextContent("<script>alert(1)</script> and more");
  });

  it("renders a raw, unescaped <script> as inert text too", () => {
    const { container } = render(<Snippet text="<script>alert(1)</script>" />);
    expect(container.querySelector("script")).toBeNull();
    expect(container.textContent).toBe("<script>alert(1)</script>");
  });

  it("renders <img onerror> as text, never as an element", () => {
    const text = '<img src=x onerror="alert(1)"> <mark>hit</mark>';
    const { container } = render(<Snippet text={text} />);
    expect(container.querySelector("img")).toBeNull();
    expect(container.querySelector("[onerror]")).toBeNull();
    expect(container.textContent).toBe('<img src=x onerror="alert(1)"> hit');
  });

  it("does not honour any tag other than the two exact tokens", () => {
    const { container } = render(
      <Snippet text={'<b>bold?</b> <mark onclick="x()">no</mark> <MARK>upper</MARK>'} />,
    );
    // No element from the input survives: `<b>` stays literal text, and a
    // `<mark …>` with attributes, or in upper case, is not a token. (The exact
    // `</mark>` IS a token; unmatched, it is consumed and changes nothing.)
    expect(highlighted(container)).toEqual([]);
    expect(container.querySelector("[onclick]")).toBeNull();
    expect(container.textContent).toBe('<b>bold?</b> <mark onclick="x()">no <MARK>upper</MARK>');
  });

  it("decodes html.escape() entities exactly once", () => {
    const { container } = render(
      <Snippet text={"Amp&#x27;ère &amp; Ohm &quot;law&quot; &#39;x&#39; &amp;lt;b&amp;gt;"} />,
    );
    // `&amp;lt;` is the escaped form of the literal text `&lt;`, not of `<`.
    expect(container.textContent).toBe(`Amp'ère & Ohm "law" 'x' &lt;b&gt;`);
  });

  it("leaves entities outside the html.escape() table alone", () => {
    const { container } = render(<Snippet text={"&#60;not decoded&#62; &nbsp;"} />);
    expect(container.textContent).toBe("&#60;not decoded&#62; &nbsp;");
  });

  it("treats a stray </mark> as nothing and never goes negative", () => {
    const { container } = render(<Snippet text="plain</mark> text <mark>hit</mark> tail" />);
    expect(highlighted(container)).toEqual(["hit"]);
    expect(container).toHaveTextContent("plain text hit tail");
  });

  it("handles nested and unclosed tokens without leaking markup", () => {
    const nested = render(<Snippet text="<mark><mark>a</mark>b</mark>c" />);
    expect(highlighted(nested.container)).toEqual(["a", "b"]);
    expect(nested.container.textContent).toBe("abc");
    nested.unmount();

    const unclosed = render(<Snippet text="x <mark>rest" />);
    expect(highlighted(unclosed.container)).toEqual(["rest"]);
  });

  it("falls back when the snippet is blank, and renders nothing when both are", () => {
    const fallback = render(<Snippet text="" fallback="Plain title" />);
    expect(fallback.container.textContent).toBe("Plain title");
    fallback.unmount();

    const empty = render(<Snippet text="" />);
    expect(empty.container).toBeEmptyDOMElement();
  });

  it("wraps in a span only when given a className", () => {
    const { container } = render(<Snippet text="a <mark>b</mark>" className="snippet" />);
    expect(container.firstElementChild?.tagName).toBe("SPAN");
    expect(container.firstElementChild).toHaveClass("snippet");
  });
});
