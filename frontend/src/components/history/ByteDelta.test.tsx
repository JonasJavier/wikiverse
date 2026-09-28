import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { BOLD_THRESHOLD, ByteDelta } from "./ByteDelta";

function visible(container: HTMLElement): string {
  return container.querySelector('[aria-hidden="true"]')?.textContent ?? "";
}

describe("ByteDelta", () => {
  it("prints an addition with an explicit + and the positive tone", () => {
    const { container } = render(<ByteDelta value={1423} />);
    const root = container.firstElementChild;
    expect(visible(container)).toBe("+1,423");
    expect(root).toHaveClass("text-delta-pos");
    expect(root).toHaveClass("font-bold");
    expect(root).toHaveAttribute("title", "1,423 bytes added");
  });

  it("prints a removal with U+2212, not a hyphen", () => {
    const { container } = render(<ByteDelta value={-96} />);
    expect(visible(container)).toBe("−96");
    expect(container.firstElementChild).toHaveClass("text-delta-neg");
    expect(container.firstElementChild).not.toHaveClass("font-bold");
    expect(container).toHaveTextContent("96 bytes removed");
  });

  it("prints zero as 0 in the null tone", () => {
    const { container } = render(<ByteDelta value={0} />);
    expect(visible(container)).toBe("0");
    expect(container.firstElementChild).toHaveClass("text-delta-null");
    expect(container).toHaveTextContent("no change in size");
  });

  it("prints an em dash when there is no byte information (talk rows)", () => {
    const { container } = render(<ByteDelta value={null} />);
    expect(visible(container)).toBe("—");
    expect(container.firstElementChild).toHaveClass("text-delta-null");
    expect(container).toHaveTextContent("no size information");
  });

  it("goes bold at ±500 bytes, in both directions", () => {
    expect(BOLD_THRESHOLD).toBe(500);
    const at = render(<ByteDelta value={-500} />);
    expect(at.container.firstElementChild).toHaveClass("font-bold");
    at.unmount();
    const below = render(<ByteDelta value={499} />);
    expect(below.container.firstElementChild).not.toHaveClass("font-bold");
  });

  it("gives screen readers a sentence instead of the glyphs", () => {
    const { container } = render(<ByteDelta value={-12345} />);
    expect(container.querySelector(".sr-only")).toHaveTextContent("12,345 bytes removed");
  });
});
