import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, type RenderOptions } from "@testing-library/react";
import type { ReactElement, ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";

/** A QueryClient that never retries and never refetches behind a test's back. */
export function createTestQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, refetchOnWindowFocus: false, staleTime: Infinity },
      mutations: { retry: false },
    },
  });
}

interface ProviderOptions extends Omit<RenderOptions, "wrapper"> {
  /** The initial router location. */
  route?: string;
  queryClient?: QueryClient;
}

/**
 * Render inside a fresh `QueryClientProvider` and a `MemoryRouter`, which is
 * what every component that renders a `<Link>` or calls a query hook needs.
 */
export function renderWithProviders(
  ui: ReactElement,
  { route = "/", queryClient = createTestQueryClient(), ...options }: ProviderOptions = {},
) {
  function Providers({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[route]}>{children}</MemoryRouter>
      </QueryClientProvider>
    );
  }
  return { queryClient, ...render(ui, { wrapper: Providers, ...options }) };
}

/**
 * jsdom has no `matchMedia`. Install one whose answer is decided per query, so
 * a test can put a component above or below a layout hinge.
 */
export function stubMatchMedia(matches: (query: string) => boolean): void {
  vi.stubGlobal(
    "matchMedia",
    (query: string): MediaQueryList =>
      ({
        matches: matches(query),
        media: query,
        onchange: null,
        addEventListener: () => undefined,
        removeEventListener: () => undefined,
        addListener: () => undefined,
        removeListener: () => undefined,
        dispatchEvent: () => false,
      }) as MediaQueryList,
  );
}
