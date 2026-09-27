import axios, {
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from "axios";

import { useAuthStore } from "@/store/auth";
import { tokens } from "./tokens";

const rawBaseURL = import.meta.env.VITE_API_URL;

export const API_BASE_URL = (
  rawBaseURL?.trim() || "http://localhost:8000/api"
).replace(/\/+$/, "");

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Attach the access token to every request.
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const access = tokens.access();

  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }

  return config;
});

/**
 * Endpoints where a 401 means "wrong credentials", not "expired access token".
 * Refreshing on those turns a failed login into a spurious session teardown and,
 * with a dead refresh token in storage, into a second pointless round trip.
 */
const NO_REFRESH = ["/auth/login/", "/auth/register/", "/auth/refresh/", "/auth/logout/"];

function isNoRefreshPath(url: string | undefined): boolean {
  if (!url) return false;
  return NO_REFRESH.some((path) => url.includes(path));
}

// Single-flight refresh: concurrent 401s await one in-flight refresh call.
let refreshing: Promise<string | null> | null = null;

/**
 * THE LOOP LATCH.
 *
 * Without it, every subsequent request that 401s re-enters the refresh path,
 * fires another `POST /auth/refresh/` with the same dead token, gets another
 * 401, and logs out again — N requests, N refresh attempts, N teardowns. The
 * single-flight promise does not prevent this: it only collapses *concurrent*
 * attempts, and a page issues its requests in waves.
 *
 * The latch is keyed on the token VALUE rather than being a bare boolean, so it
 * releases itself the moment a new session writes a different refresh token.
 * That needs no reset call, and therefore no import cycle back through the auth
 * store.
 */
let deadRefreshToken: string | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const refresh = tokens.refresh();

  if (!refresh) return null;

  try {
    const { data } = await axios.post<{ access: string }>(
      `${API_BASE_URL}/auth/refresh/`,
      { refresh },
    );

    tokens.setAccess(data.access);
    deadRefreshToken = null;
    return data.access;
  } catch {
    // Remember WHICH token failed, so a later session is not tarred with it.
    deadRefreshToken = refresh;
    return null;
  }
}

api.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error)) {
      return Promise.reject(error);
    }

    const original = error.config as
      | (AxiosRequestConfig & { _retry?: boolean })
      | undefined;

    if (error.response?.status !== 401 || !original) {
      return Promise.reject(error);
    }
    if (original._retry || isNoRefreshPath(original.url)) {
      return Promise.reject(error);
    }

    const refresh = tokens.refresh();

    // No refresh token, or the one we have is already known dead: do not ask.
    if (!refresh) {
      useAuthStore.getState().clearSession();
      return Promise.reject(error);
    }
    if (refresh === deadRefreshToken) {
      return Promise.reject(error);
    }

    original._retry = true;

    refreshing ??= refreshAccessToken().finally(() => {
      refreshing = null;
    });

    const newAccess = await refreshing;

    if (newAccess) {
      original.headers = original.headers ?? {};
      (original.headers as Record<string, string>).Authorization =
        `Bearer ${newAccess}`;

      return api(original);
    }

    // Refresh failed. Drop the local session; the latch above stops every
    // other in-flight 401 from repeating this.
    useAuthStore.getState().clearSession();

    return Promise.reject(error);
  },
);

/** Normalize a DRF error response into a readable message. */
export function apiErrorMessage(
  error: unknown,
  fallback = "Something went wrong.",
): string {
  if (axios.isAxiosError(error) && error.response?.data) {
    const data = error.response.data as Record<string, unknown>;

    if (typeof data.detail === "string") return data.detail;

    const first = Object.values(data)[0];

    if (Array.isArray(first) && typeof first[0] === "string") {
      return first[0];
    }

    if (typeof first === "string") return first;
  }

  return fallback;
}
