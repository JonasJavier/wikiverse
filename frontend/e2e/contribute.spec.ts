import { expect, test } from "@playwright/test";

import { registerThroughUi, signInViaApi } from "./helpers";

test.describe("contributing", () => {
  test("a new account can register and sign out", async ({ page }) => {
    const account = await registerThroughUi(page);

    await page.getByRole("button", { name: `Account menu for ${account.username}` }).click();
    await page.getByRole("menuitem", { name: "Log out" }).click();
    await expect(page.getByRole("link", { name: "Log in" })).toBeVisible();
  });

  test("anonymous readers are sent to log in before editing", async ({ page }) => {
    await page.goto("/wiki/e2e-edit-me/edit");
    await expect(page).toHaveURL(/\/login$/);
  });

  test("an edit becomes a revision with its summary", async ({ page }) => {
    await signInViaApi(page);
    const marker = `Edited by the end-to-end suite at ${Date.now()}.`;
    const summary = `e2e edit ${Date.now()}`;

    await page.goto("/wiki/e2e-edit-me/edit");
    const body = page.getByLabel("Body", { exact: true });
    await expect(body).toHaveValue(/E2E edit me/);
    await body.fill(`${await body.inputValue()}\n\n${marker}`);
    await page.getByLabel("Edit summary").fill(summary);
    await page.getByRole("button", { name: "Save changes" }).click();

    await expect(page).toHaveURL(/\/wiki\/e2e-edit-me$/);
    await expect(page.getByText(marker)).toBeVisible();

    await page.goto("/wiki/e2e-edit-me/history");
    await expect(page.getByText(summary)).toBeVisible();
  });

  test("a comment can be added to an existing talk topic", async ({ page }) => {
    await signInViaApi(page);
    const comment = `A reply from the end-to-end suite, ${Date.now()}.`;

    await page.goto("/wiki/e2e-talk-me/talk");
    await expect(page.getByRole("heading", { level: 1, name: "Talk: E2E talk me" })).toBeVisible();

    await page.getByPlaceholder("Add to this topic.").first().fill(comment);
    await page.getByRole("button", { name: "Add comment" }).first().click();
    await expect(page.getByText(comment)).toBeVisible();
  });
});
