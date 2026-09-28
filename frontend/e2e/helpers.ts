import { expect, type Page } from "@playwright/test";

/** The backend the Playwright config starts (see playwright.config.ts). */
export const API_URL = "http://127.0.0.1:8011/api";

/**
 * A fresh account per call. Generated here rather than read from a fixture,
 * so a rerun never collides with an account a previous run left behind.
 */
export function testAccount() {
  const stamp = `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
  return {
    username: `e2e_${stamp}`,
    email: `e2e_${stamp}@example.test`,
    password: `Pw-${stamp}-${stamp}`,
  };
}

/** Register through the real form, which also signs the reader in. */
export async function registerThroughUi(page: Page) {
  const account = testAccount();
  await page.goto("/register");
  await page.getByLabel("Username").fill(account.username);
  await page.getByLabel("Email").fill(account.email);
  await page.getByLabel("Password", { exact: true }).fill(account.password);
  await page.getByLabel("Confirm password").fill(account.password);
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page).toHaveURL("/");
  await expect(
    page.getByRole("button", { name: `Account menu for ${account.username}` }),
  ).toBeVisible();
  return account;
}

/**
 * Register through the API and hand the tokens to the page — for journeys where
 * signing up is setup, not the thing under test.
 */
export async function signInViaApi(page: Page) {
  const account = testAccount();
  const registered = await page.request.post(`${API_URL}/auth/register/`, {
    data: { ...account, password_confirm: account.password },
  });
  expect(registered.ok(), await registered.text()).toBeTruthy();
  // Registration returns the user; tokens come from logging in, as in the app.
  const login = await page.request.post(`${API_URL}/auth/login/`, {
    data: { username: account.username, password: account.password },
  });
  expect(login.ok(), await login.text()).toBeTruthy();
  const body = (await login.json()) as { access: string; refresh: string };

  await page.goto("/");
  await page.evaluate(
    ({ access, refresh }) => {
      localStorage.setItem("wikiverse.access", access);
      localStorage.setItem("wikiverse.refresh", refresh);
    },
    { access: body.access, refresh: body.refresh },
  );
  await page.reload();
  await expect(
    page.getByRole("button", { name: `Account menu for ${account.username}` }),
  ).toBeVisible();
  return account;
}
