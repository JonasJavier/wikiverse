import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";
import { tokens } from "@/lib/tokens";
import type { AuthTokens, LogoutInput, User } from "@/lib/types";
import { useAuthStore } from "@/store/auth";

interface LoginInput {
  username: string;
  password: string;
}

interface RegisterInput {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export const authKeys = {
  me: ["me"] as const,
};

export function useLogin() {
  const setSession = useAuthStore((s) => s.setSession);
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: LoginInput) => {
      const { data } = await api.post<AuthTokens>("/auth/login/", input);
      return data;
    },
    onSuccess: (data) => {
      setSession(data);
      // The previous reader's `me` must not survive a new sign-in.
      qc.setQueryData(authKeys.me, data.user);
      qc.invalidateQueries();
    },
  });
}

export function useRegister() {
  const setSession = useAuthStore((s) => s.setSession);
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: RegisterInput) => {
      await api.post("/auth/register/", input);
      // Auto-login after a successful registration.
      const { data } = await api.post<AuthTokens>("/auth/login/", {
        username: input.username,
        password: input.password,
      });
      return data;
    },
    onSuccess: (data) => {
      setSession(data);
      qc.setQueryData(authKeys.me, data.user);
      qc.invalidateQueries();
    },
  });
}

/**
 * Sign out properly.
 *
 * DECISIONS §7.2: `POST /api/auth/logout/` takes `{refresh}` and blacklists it.
 * Without that call the refresh token stays valid for its full
 * `REFRESH_TOKEN_LIFETIME` (two days) after the reader believes they have signed
 * out — so "log out" on a shared machine meant nothing.
 *
 * The local session is cleared in `onSettled`, not `onSuccess`: a network
 * failure must not leave the reader signed in on a machine they are trying to
 * leave. Best effort server-side, unconditional client-side.
 */
export function useLogout() {
  const clearSession = useAuthStore((s) => s.clearSession);
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const refresh = tokens.refresh();
      if (!refresh) return;
      const body: LogoutInput = { refresh };
      await api.post("/auth/logout/", body);
    },
    onSettled: () => {
      clearSession();
      // Drop every cached response: some of it was authorised.
      qc.clear();
    },
  });
}

/** Hydrate / validate the current session against the backend. */
export function useMe() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const setUser = useAuthStore((s) => s.setUser);
  const clearSession = useAuthStore((s) => s.clearSession);

  return useQuery({
    queryKey: authKeys.me,
    queryFn: async () => {
      try {
        const { data } = await api.get<User>("/auth/me/");
        setUser(data);
        return data;
      } catch (error) {
        // `lib/api.ts` already tore the session down if the refresh failed.
        // This covers the case where there was never a refresh token to try.
        if (!tokens.refresh()) clearSession();
        throw error;
      }
    },
    enabled: isAuthenticated,
    retry: false,
    staleTime: 60 * 1000,
  });
}
