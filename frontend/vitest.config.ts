import { defineConfig, mergeConfig } from "vitest/config";

import viteConfig from "./vite.config";

/*
 * Pin the time zone for every test worker, and pin it WEST of UTC on purpose.
 *
 * Date formatting is locale- and zone-dependent, so an unpinned suite passes on
 * one machine and fails on another. A zone behind UTC is also the one that
 * exposes the classic date-only bug: `new Date("2026-09-26")` is UTC midnight,
 * which is still the 25th in the Americas. America/Santo_Domingo is UTC−4 with
 * no daylight saving, so the offset never moves under the tests.
 *
 * Set here, in the main process, so the forked workers inherit it at start-up.
 */
process.env.TZ = "America/Santo_Domingo";

// The app's own Vite config (aliases, plugins) is reused, so `@/…` imports and
// the React transform behave exactly as they do in `vite dev` / `vite build`.
// Nothing here is read by `vite build`, so the production bundle is unchanged.
export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "jsdom",
      setupFiles: ["./src/test/setup.ts"],
      include: ["src/**/*.test.{ts,tsx}"],
      // Components never import CSS in a way the assertions depend on.
      css: false,
      restoreMocks: true,
      unstubGlobals: true,
      env: { TZ: "America/Santo_Domingo" },
      coverage: {
        provider: "v8",
        include: ["src/**/*.{ts,tsx}"],
        exclude: ["src/**/*.test.{ts,tsx}", "src/test/**", "src/main.tsx", "src/vite-env.d.ts"],
        reporter: ["text-summary", "html"],
      },
    },
  }),
);
