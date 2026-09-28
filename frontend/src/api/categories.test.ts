import { describe, expect, it, vi } from "vitest";

import {
  buildCategoryTree,
  CATEGORY_PAGE_SIZE,
  parentSlug,
  subcategoriesOf,
  type CategoryRow,
} from "./categories";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

let nextId = 1;

function category(
  slug: string,
  parent: CategoryRow["parent"] = null,
  { order = 0, count = 0, name }: { order?: number; count?: number; name?: string } = {},
): CategoryRow {
  return {
    id: nextId++,
    name: name ?? slug[0].toUpperCase() + slug.slice(1),
    slug,
    description: "",
    color: "#888888",
    icon: "",
    order,
    parent,
    article_count: count,
  };
}

const flat: CategoryRow[] = [
  category("science", null, { order: 1, count: 2 }),
  category("physics", "science", { order: 2, count: 5 }),
  category("biology", "science", { order: 1, count: 3 }),
  category("chemistry", { slug: "science", name: "Science", color: "#000" }, { order: 1, count: 1 }),
  category("arts", null, { order: 0, count: 1 }),
  category("music", "arts", { count: 20 }),
  category("history", null, { order: 1, count: 4 }),
];

describe("parentSlug — both wire shapes", () => {
  it.each([
    [null, null],
    ["", null],
    ["science", "science"],
    [{ slug: "science", name: "Science", color: "#000" }, "science"],
    [{ slug: "", name: "", color: "" }, null],
  ] as const)("%j → %j", (parent, expected) => {
    expect(parentSlug(parent)).toBe(expected);
  });
});

describe("buildCategoryTree", () => {
  it("returns nothing for no data", () => {
    expect(buildCategoryTree(undefined)).toEqual([]);
    expect(buildCategoryTree([])).toEqual([]);
  });

  it("groups children under their parent, from either parent shape", () => {
    const tree = buildCategoryTree(flat);
    const science = tree.find((b) => b.category.slug === "science");
    expect(science?.children.map((c) => c.slug)).toEqual(["biology", "chemistry", "physics"]);
  });

  it("sorts roots and children by order, then name", () => {
    const tree = buildCategoryTree(flat);
    expect(tree.map((b) => b.category.slug)).toEqual(["arts", "history", "science"]);
  });

  it("totals a branch as its own count plus its children's", () => {
    const totals = Object.fromEntries(
      buildCategoryTree(flat).map((b) => [b.category.slug, b.total]),
    );
    expect(totals).toEqual({ arts: 21, history: 4, science: 11 });
  });

  it("sorts by total, largest first, when asked for size", () => {
    expect(buildCategoryTree(flat, "size").map((b) => b.category.slug)).toEqual([
      "arts",
      "science",
      "history",
    ]);
  });

  it("breaks a size tie by name", () => {
    const tied = [category("zeta", null, { count: 3 }), category("alpha", null, { count: 3 })];
    expect(buildCategoryTree(tied, "size").map((b) => b.category.slug)).toEqual(["alpha", "zeta"]);
  });

  it("promotes an orphan (missing parent) and a self-parented row to the top level", () => {
    const tree = buildCategoryTree([
      category("orphan", "gone"),
      category("loop", "loop"),
    ]);
    expect(tree.map((b) => b.category.slug).sort()).toEqual(["loop", "orphan"]);
    expect(tree.every((b) => b.children.length === 0)).toBe(true);
  });

  it("does not mutate its input", () => {
    const copy = structuredClone(flat);
    buildCategoryTree(flat, "size");
    expect(flat).toEqual(copy);
  });
});

describe("subcategoriesOf", () => {
  it("lists a category's children sorted by order then name", () => {
    expect(subcategoriesOf(flat, "science").map((c) => c.slug)).toEqual([
      "biology",
      "chemistry",
      "physics",
    ]);
  });

  it("returns nothing for a leaf, an unknown slug, a blank slug or no data", () => {
    expect(subcategoriesOf(flat, "physics")).toEqual([]);
    expect(subcategoriesOf(flat, "nope")).toEqual([]);
    expect(subcategoriesOf(flat, "")).toEqual([]);
    expect(subcategoriesOf(undefined, "science")).toEqual([]);
  });

  it("pages category listings at 50 (DECISIONS §10)", () => {
    expect(CATEGORY_PAGE_SIZE).toBe(50);
  });
});
