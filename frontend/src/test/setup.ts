/**
 * Global test setup: jest-dom matchers on Vitest's `expect`, and a clean DOM
 * and clean storage between tests.
 *
 * Vitest runs without `globals: true`, so Testing Library cannot register its
 * own `afterEach(cleanup)` — it is done explicitly here instead.
 */
import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(() => {
  cleanup();
  try {
    window.localStorage.clear();
  } catch {
    // A test may have replaced localStorage with one that throws; `unstubGlobals`
    // restores the real one after this hook.
  }
});
