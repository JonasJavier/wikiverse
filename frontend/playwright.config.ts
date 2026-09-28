import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig, devices } from "@playwright/test";

/**
 * End-to-end journeys against a real backend and a production build.
 *
 * Playwright starts both servers itself:
 *
 *   - the Django API on :8011, against a throwaway SQLite file, migrated and
 *     loaded with `seed_e2e` (three fixture articles, DECISIONS §18);
 *   - the Vite *preview* server on :4174, serving `npm run build` output, so the
 *     tests exercise the same bundle and route-level code splitting as production.
 *
 * `E2E_PYTHON` points at the interpreter that has the backend requirements; CI
 * uses the job's `python`. Set `E2E_REUSE=1` to attach to servers you already
 * started by hand.
 */
const here = path.dirname(fileURLToPath(import.meta.url));
const backendDir = path.resolve(here, "../backend");
const python = process.env.E2E_PYTHON ?? "python";

const API_PORT = 8011;
const WEB_PORT = 4174;
const API_URL = `http://127.0.0.1:${API_PORT}/api`;
const WEB_URL = `http://127.0.0.1:${WEB_PORT}`;

const reuse = Boolean(process.env.E2E_REUSE);

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  // The journeys share one database; editing and posting run in sequence.
  workers: 1,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  timeout: 30_000,
  expect: { timeout: 7_500 },
  use: {
    baseURL: WEB_URL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    {
      command: [
        `"${python}" manage.py migrate --noinput`,
        `"${python}" manage.py seed_e2e --flush`,
        `"${python}" manage.py runserver 127.0.0.1:${API_PORT} --noreload`,
      ].join(" && "),
      cwd: backendDir,
      url: `${API_URL}/health/`,
      reuseExistingServer: reuse,
      timeout: 120_000,
      env: {
        DEBUG: "true",
        SECRET_KEY: "e2e-only-not-secret",
        DATABASE_URL: `sqlite:///${path.join(backendDir, "e2e.sqlite3").replace(/\\/g, "/")}`,
        REDIS_URL: "",
        CORS_ALLOWED_ORIGINS: WEB_URL,
        // Every journey registers its own account; the production limit of
        // five registrations an hour would fail the third run of the day.
        THROTTLE_REGISTER: "1000/min",
        THROTTLE_LOGIN: "1000/min",
        THROTTLE_WRITE: "1000/min",
      },
    },
    {
      command: `npm run build && npx vite preview --port ${WEB_PORT} --strictPort --host 127.0.0.1`,
      cwd: here,
      url: WEB_URL,
      reuseExistingServer: reuse,
      timeout: 180_000,
      env: { VITE_API_URL: API_URL },
    },
  ],
});
