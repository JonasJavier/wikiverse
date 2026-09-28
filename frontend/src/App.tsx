import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { isAxiosError } from "axios";
import type { ComponentType } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Layout } from "@/components/layout/Layout";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { RouteErrorFallback } from "@/components/ui/ErrorBoundary";
import { ArticlePage } from "@/pages/ArticlePage";
import { HomePage } from "@/pages/HomePage";
import { NotFoundPage } from "@/pages/NotFoundPage";

/**
 * Retry what a retry can fix — a dropped connection, a 5xx while a sleeping
 * service wakes — and nothing else. A 4xx is an answer, not a failure: retrying
 * a 404 only delays the "no such article" page by three round trips.
 */
function shouldRetry(failureCount: number, error: unknown): boolean {
  if (failureCount >= 2) return false;
  if (isAxiosError(error)) {
    const status = error.response?.status;
    return status === undefined || status >= 500;
  }
  return false;
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: shouldRetry,
      retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 8000),
      refetchOnWindowFocus: false,
    },
  },
});

/**
 * Route-level code splitting. The main page, the article page and the 404 are
 * in the entry chunk because they are where readers land; everything else —
 * the editor above all — loads on first visit.
 */
function page<K extends string>(
  load: () => Promise<Record<K, ComponentType>>,
  name: K,
) {
  return async () => ({ Component: (await load())[name] });
}

function protectedPage<K extends string>(
  load: () => Promise<Record<K, ComponentType>>,
  name: K,
) {
  return async () => {
    const Page: ComponentType = (await load())[name];
    return {
      Component: () => (
        <ProtectedRoute>
          <Page />
        </ProtectedRoute>
      ),
    };
  };
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    errorElement: <RouteErrorFallback />,
    HydrateFallback: () => null,
    children: [
      {
        // Errors inside a page render in the shell, not over it.
        errorElement: <RouteErrorFallback />,
        children: [
          { path: "/", element: <HomePage /> },
          { path: "/wiki/:slug", element: <ArticlePage /> },
          {
            path: "/wiki/:slug/talk",
            lazy: page(() => import("@/pages/TalkPage"), "TalkPage"),
          },
          {
            path: "/wiki/:slug/history",
            lazy: page(() => import("@/pages/HistoryPage"), "HistoryPage"),
          },
          {
            path: "/wiki/:slug/diff",
            lazy: page(() => import("@/pages/DiffPage"), "DiffPage"),
          },
          {
            path: "/wiki/:slug/edit",
            lazy: protectedPage(() => import("@/pages/EditorPage"), "EditorPage"),
          },
          {
            path: "/new",
            lazy: protectedPage(() => import("@/pages/EditorPage"), "EditorPage"),
          },
          {
            path: "/search",
            lazy: page(() => import("@/pages/SearchPage"), "SearchPage"),
          },
          {
            path: "/browse",
            lazy: page(() => import("@/pages/BrowsePage"), "BrowsePage"),
          },
          {
            path: "/categories",
            lazy: page(() => import("@/pages/CategoriesPage"), "CategoriesPage"),
          },
          {
            path: "/category/:slug",
            lazy: page(() => import("@/pages/CategoryPage"), "CategoryPage"),
          },
          {
            path: "/changes",
            lazy: page(() => import("@/pages/RecentChangesPage"), "RecentChangesPage"),
          },
          {
            path: "/watchlist",
            lazy: page(() => import("@/pages/WatchlistPage"), "WatchlistPage"),
          },
          {
            path: "/random",
            lazy: page(() => import("@/pages/RandomPage"), "RandomPage"),
          },
          {
            path: "/about",
            lazy: page(() => import("@/pages/AboutPage"), "AboutPage"),
          },
          {
            path: "/u/:username",
            lazy: page(() => import("@/pages/ProfilePage"), "ProfilePage"),
          },
          {
            path: "/login",
            lazy: page(() => import("@/pages/LoginPage"), "LoginPage"),
          },
          {
            path: "/register",
            lazy: page(() => import("@/pages/RegisterPage"), "RegisterPage"),
          },
          { path: "*", element: <NotFoundPage /> },
        ],
      },
    ],
  },
]);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
