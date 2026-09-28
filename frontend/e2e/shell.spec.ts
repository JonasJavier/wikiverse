import { expect, test } from "@playwright/test";

test.describe("site shell", () => {
  test("the main page shows its panels and the site navigation", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Wikiverse — the open encyclopedia");
    await expect(page.getByRole("heading", { level: 1, name: "Welcome to Wikiverse" })).toBeVisible();

    const site = page.getByRole("navigation", { name: "Site" });
    for (const name of ["Main page", "Recent changes", "Random article", "About"]) {
      await expect(site.getByRole("link", { name })).toBeVisible();
    }
  });

  test("recent changes lists the fixture edits and keeps filters in the URL", async ({ page }) => {
    await page.goto("/changes?days=90");
    await expect(page.getByRole("heading", { level: 1, name: "Recent changes" })).toBeVisible();

    await page.getByRole("link", { name: "Edits", exact: true }).click();
    await expect(page).toHaveURL(/type=edit/);
    await expect(page).toHaveURL(/days=90/);
  });

  test("on a phone the site navigation opens from the masthead", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/about");

    const toggle = page.getByRole("button", { name: "Site navigation" });
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await page.locator("#site-nav-panel").getByRole("link", { name: "Categories" }).click();
    await expect(page).toHaveURL(/\/categories$/);
    await expect(page.locator("#site-nav-panel")).toHaveCount(0);
  });

  test("the theme toggle cycles light, dark and system", async ({ page }) => {
    await page.emulateMedia({ colorScheme: "light" });
    await page.goto("/");
    const html = page.locator("html");

    const toggle = page.getByRole("button", { name: /theme/i });
    await expect(html).not.toHaveClass(/dark/);
    await toggle.click(); // system -> light
    await toggle.click(); // light -> dark
    await expect(html).toHaveClass(/dark/);

    // The choice survives a reload, painted before React runs.
    await page.reload();
    await expect(html).toHaveClass(/dark/);
  });
});
