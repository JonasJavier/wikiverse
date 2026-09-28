import { expect, test } from "@playwright/test";

test.describe("reading", () => {
  test("an article renders with its title, contents and tabs", async ({ page }) => {
    await page.goto("/wiki/e2e-read-me");

    await expect(page).toHaveTitle("E2E read me — Wikiverse");
    await expect(page.getByRole("heading", { level: 1, name: "E2E read me" })).toBeVisible();
    await expect(page.getByText("is a fixture article. End-to-end tests read it")).toBeVisible();

    // The table of contents is built from the body's headings.
    const contents = page.getByRole("navigation", { name: /contents/i });
    await expect(contents.getByRole("link", { name: /Structure/ })).toBeVisible();
    await expect(contents.getByRole("link", { name: /Stability/ })).toBeVisible();

    // Namespace and action tabs.
    await expect(page.getByRole("link", { name: "Talk" }).first()).toBeVisible();
    await expect(page.getByRole("link", { name: "View history" }).first()).toBeVisible();
  });

  test("a wikilink shows a hover preview and navigates", async ({ page }) => {
    await page.goto("/wiki/e2e-read-me");

    const link = page.locator("main").getByRole("link", { name: "E2E edit me" }).first();
    await link.hover();
    await expect(page.getByText("A fixture article that end-to-end tests edit")).toBeVisible();

    await link.click();
    await expect(page).toHaveURL(/\/wiki\/e2e-edit-me$/);
    await expect(page.getByRole("heading", { level: 1, name: "E2E edit me" })).toBeVisible();
  });

  test("a missing article offers to create it", async ({ page }) => {
    await page.goto("/wiki/an-article-nobody-wrote");

    await expect(
      page.getByText("Wikiverse does not have an article with this exact title."),
    ).toBeVisible();
    const create = page.getByRole("link", { name: "create this page" });
    await expect(create).toHaveAttribute("href", /\/new\?title=/);
  });

  test("the skip link is the first stop for keyboard readers", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Tab");
    const skip = page.getByRole("link", { name: "Skip to content" });
    await expect(skip).toBeFocused();
    await skip.press("Enter");
    await expect(page.locator("main#content")).toBeFocused();
  });

  test("random article lands on an article", async ({ page }) => {
    await page.goto("/random");
    await expect(page).toHaveURL(/\/wiki\/e2e-/);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("E2E");
  });
});
