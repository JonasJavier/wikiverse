import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { ReactNode } from "react";
import { describe, expect, it } from "vitest";

import type { DiffHunk, DiffPayload, DiffRow } from "@/lib/types";
import { stubMatchMedia } from "@/test/render";
import { DiffOps, InlineRows, SplitRow } from "./DiffLine";
import { DiffViewer } from "./DiffViewer";

const MODE_KEY = "wikiverse.diff.mode";

function payload(patch: Partial<DiffPayload> = {}): DiffPayload {
  return {
    article: { slug: "photosynthesis", title: "Photosynthesis", page_type: "article", category: null },
    from_revision: { id: 1, editor: null, comment: "", byte_size: 100, is_minor: false, created_at: null },
    to_revision: { id: 2, editor: null, comment: "", byte_size: 120, is_minor: false, created_at: null },
    prev_id: null,
    next_id: null,
    created: false,
    title_changed: false,
    summary_changed: false,
    stats: { lines_added: 1, lines_removed: 1, lines_changed: 1, bytes_added: 1423, bytes_removed: 96 },
    truncated: false,
    hunks: [],
    ...patch,
  };
}

const changed: DiffRow = {
  t: "~",
  a: 3,
  b: 3,
  ops: [
    ["=", "Light is "],
    ["-", "absorbed"],
    ["+", "captured"],
    ["=", " by chlorophyll."],
  ],
};
const context: DiffRow = { t: "=", a: 2, b: 2, ops: [["=", "Context line."]] };
const added: DiffRow = { t: "+", a: null, b: 4, ops: [["+", "New line."]] };

function hunk(a_start: number, a_lines: number, rows: DiffRow[]): DiffHunk {
  return { a_start, a_lines, b_start: a_start, b_lines: a_lines, rows };
}

function renderRow(ui: ReactNode) {
  return render(
    <table>
      <tbody>{ui}</tbody>
    </table>,
  );
}

describe("DiffOps", () => {
  it("reconstructs the old line with <del> and the new line with <ins>", () => {
    const old = renderRow(
      <tr>
        <td>
          <DiffOps ops={changed.ops} side="old" />
        </td>
      </tr>,
    );
    expect(old.container.querySelector("td")?.textContent).toBe("Light is absorbed by chlorophyll.");
    expect(old.container.querySelector("del")).toHaveTextContent("absorbed");
    expect(old.container.querySelector("ins")).toBeNull();
    old.unmount();

    const next = renderRow(
      <tr>
        <td>
          <DiffOps ops={changed.ops} side="new" />
        </td>
      </tr>,
    );
    expect(next.container.querySelector("td")?.textContent).toBe("Light is captured by chlorophyll.");
    expect(next.container.querySelector("ins")).toHaveTextContent("captured");
  });

  it("keeps a blank line's height with a no-break space", () => {
    const { container } = renderRow(
      <tr>
        <td>
          <DiffOps ops={[]} side="old" />
        </td>
      </tr>,
    );
    expect(container.querySelector("td")?.textContent).toBe(" ");
  });
});

describe("SplitRow / InlineRows", () => {
  it("a changed row is one six-cell row side by side", () => {
    const { container } = renderRow(<SplitRow row={changed} />);
    expect(container.querySelectorAll("tr")).toHaveLength(1);
    expect(container.querySelectorAll("td")).toHaveLength(6);
    expect(container).toHaveTextContent("removed:");
    expect(container).toHaveTextContent("added:");
  });

  it("a changed row is two rows inline: removed above added", () => {
    const { container } = renderRow(<InlineRows row={changed} />);
    const rows = [...container.querySelectorAll("tr")];
    expect(rows).toHaveLength(2);
    expect(rows[0]).toHaveTextContent("removed:");
    expect(rows[0].querySelector("del")).toBeInTheDocument();
    expect(rows[1]).toHaveTextContent("added:");
    expect(rows[1].querySelector("ins")).toBeInTheDocument();
  });

  it("an added row has no old side", () => {
    const { container } = renderRow(<InlineRows row={added} />);
    expect(container.querySelectorAll("tr")).toHaveLength(1);
    expect(container).toHaveTextContent("added:");
    expect(container).not.toHaveTextContent("removed:");
  });

  it("a `~` row with no changed ops renders as unchanged context", () => {
    const { container } = renderRow(<InlineRows row={{ t: "~", a: 5, b: 5, ops: [] }} />);
    expect(container.querySelectorAll("tr")).toHaveLength(1);
    expect(container).not.toHaveTextContent("removed:");
    expect(container).not.toHaveTextContent("added:");
  });
});

describe("DiffViewer", () => {
  it("prints the stats with +, U+2212 and grouped numbers", () => {
    render(<DiffViewer diff={payload({ hunks: [hunk(2, 2, [context, changed])] })} />);
    expect(screen.getByText("+1,423")).toBeInTheDocument();
    expect(screen.getByText("−96")).toBeInTheDocument();
  });

  it("says so when nothing in the body changed", () => {
    render(
      <DiffViewer
        diff={payload({
          stats: { lines_added: 0, lines_removed: 0, lines_changed: 0, bytes_added: 0, bytes_removed: 0 },
        })}
      />,
    );
    expect(screen.getByText("No difference.")).toBeInTheDocument();
    expect(screen.getByText(/byte for byte identical/)).toBeInTheDocument();
    expect(screen.queryByRole("table")).toBeNull();
  });

  it("shows the created / title / summary / truncated notices", () => {
    render(
      <DiffViewer
        diff={payload({
          created: true,
          title_changed: true,
          summary_changed: true,
          truncated: true,
          hunks: [hunk(1, 1, [added])],
        })}
      />,
    );
    expect(screen.getByText(/created the page/)).toBeInTheDocument();
    expect(screen.getByText(/title changed/)).toBeInTheDocument();
    expect(screen.getByText(/summary changed/)).toBeInTheDocument();
    expect(screen.getByText(/comparison is incomplete/)).toBeInTheDocument();
  });

  it("is inline-only below the shelf breakpoint (no matchMedia in jsdom)", () => {
    const { container } = render(
      <DiffViewer diff={payload({ hunks: [hunk(2, 2, [context, changed])] })} />,
    );
    expect(screen.queryByRole("group", { name: "Diff display" })).toBeNull();
    expect(container.querySelectorAll("col")).toHaveLength(4);
    expect(screen.getByText(/Line 2 → 2:/)).toBeInTheDocument();
  });

  it("counts the unchanged lines skipped between hunks", () => {
    render(
      <DiffViewer
        diff={payload({ hunks: [hunk(2, 2, [context, changed]), hunk(10, 1, [added]), hunk(12, 1, [added])] })}
      />,
    );
    expect(screen.getByText("6 unchanged lines")).toBeInTheDocument();
    expect(screen.getByText("1 unchanged line")).toBeInTheDocument();
  });

  it("offers side by side at shelf width and persists the choice", async () => {
    stubMatchMedia((query) => query.includes("min-width: 60rem"));
    const user = userEvent.setup();
    const { container } = render(
      <DiffViewer diff={payload({ hunks: [hunk(2, 2, [context, changed])] })} />,
    );

    const split = screen.getByRole("button", { name: "Side by side" });
    const inline = screen.getByRole("button", { name: "Inline" });
    expect(split).toHaveAttribute("aria-pressed", "true");
    expect(container.querySelectorAll("col")).toHaveLength(6);

    await user.click(inline);
    expect(inline).toHaveAttribute("aria-pressed", "true");
    expect(container.querySelectorAll("col")).toHaveLength(4);
    expect(window.localStorage.getItem(MODE_KEY)).toBe("inline");
  });

  it("restores a stored inline preference", () => {
    stubMatchMedia((query) => query.includes("min-width: 60rem"));
    window.localStorage.setItem(MODE_KEY, "inline");
    render(<DiffViewer diff={payload({ hunks: [hunk(2, 2, [changed])] })} />);
    expect(screen.getByRole("button", { name: "Inline" })).toHaveAttribute("aria-pressed", "true");
  });
});
