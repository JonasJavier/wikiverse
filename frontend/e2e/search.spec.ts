import { expect, test } from "@playwright/test";

test.describe("search", () => {
  test("the masthead typeahead suggests titles and opens one", async ({ page }) => {
    await page.goto("/");

    const box = page.getByRole("combobox", { name: "Search Wikiverse" });
    await box.fill("E2E talk");
    const listbox = page.getByRole("listbox", { name: "Search suggestions" });
    await expect(listbox.getByRole("option", { name: /E2E talk me/ })).toBeVisible();

    await box.press("ArrowDown");
    await box.press("Enter");
    await expect(page).toHaveURL(/\/wiki\/e2e-talk-me$/);
    await expect(page.getByRole("heading", { level: 1, name: "E2E talk me" })).toBeVisible();
  });

  test("the last suggestion runs a full-text search", async ({ page }) => {
    await page.goto("/");

    const box = page.getByRole("combobox", { name: "Search Wikiverse" });
    await box.fill("fixture");
    await page.getByRole("option", { name: /Search for pages containing/ }).click();

    await expect(page).toHaveURL(/\/search\?q=fixture/);
    await expect(page.getByText(/Results 1–3 of 3/)).toBeVisible();
    for (const title of ["E2E read me", "E2E edit me", "E2E talk me"]) {
      await expect(page.getByRole("link", { name: title }).first()).toBeVisible();
    }
  });

  test("a search with no hits says so", async ({ page }) => {
    await page.goto("/search?q=zzqxv-no-such-term");
    await expect(page.getByText("No pages matched.")).toBeVisible();
    // …and offers to start the page, as a wiki does.
    await expect(page.getByRole("link", { name: /zzqxv-no-such-term/ })).toHaveAttribute(
      "href",
      /\/new\?title=/,
    );
  });
});
