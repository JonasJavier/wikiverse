import { expect, test } from "@playwright/test";

test.describe("history and diff", () => {
  test("two revisions can be selected and compared", async ({ page }) => {
    await page.goto("/wiki/e2e-read-me/history");

    await expect(
      page.getByRole("heading", { level: 1, name: /E2E read me: revision history/ }),
    ).toBeVisible();
    await expect(page.getByText("Second revision, created by seed_e2e").first()).toBeVisible();

    // The newest pair is preselected, so comparing needs one click.
    await page.getByRole("button", { name: "Compare selected revisions" }).first().click();

    await expect(page).toHaveURL(/\/wiki\/e2e-read-me\/diff\?from=\d+&to=\d+/);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("E2E read me");
    // A diff table with at least one changed line.
    await expect(page.locator("table").first()).toBeVisible();
  });
});
