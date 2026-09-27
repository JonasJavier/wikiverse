import axios from "axios";
import { type FormEvent, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useLogin } from "@/api/auth";
import { apiErrorMessage } from "@/lib/api";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/Button";
import { FieldError, Input, Label } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/Spinner";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";

const LINK = "text-link hover:text-link-hover hover:underline";

/**
 * Log in.
 *
 * **The demo-credentials block is gone and must not come back.** It rendered a
 * working `admin` username and password into the DOM of a public page, for an
 * account the seed created as `is_staff` and `is_superuser`, on a deployment
 * whose `/admin/` is publicly proxied. DECISIONS §8 and `SECURITY.md` record
 * that password as permanently burned — it is not repeated here either:
 * it is in git history, the legacy `admin` user has had its password made
 * unusable and its staff flags cleared by `accounts/0003_revoke_legacy_admin`,
 * and `manage.py ensure_admin` is now the only way a superuser exists. If a demo
 * login is ever wanted it has to be a non-staff, read-mostly account, and its
 * credentials still may not be printed on a public page.
 *
 * Errors: one `role="alert"` summary above the form and an inline message under
 * each field. Never a toast — a toast for a form error vanishes before it can be
 * acted on, and cannot be re-read.
 */
export function LoginPage() {
  const login = useLogin();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: string } | null)?.from ?? "/";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{
    username?: string;
    password?: string;
    summary?: string;
  }>({});

  useDocumentMeta({
    title: "Log in",
    description:
      "Log in to Wikiverse to write and edit articles. You do not need an account to read.",
    // A sign-in form has nothing to index, and indexing it invites credential
    // phishing results against the site's own name.
    robots: "noindex",
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const next: typeof errors = {};
    if (!username.trim()) next.username = "Enter your username.";
    if (!password) next.password = "Enter your password.";
    if (Object.keys(next).length > 0) {
      setErrors({ ...next, summary: "Complete both fields to log in." });
      return;
    }

    setErrors({});

    try {
      await login.mutateAsync({ username: username.trim(), password });
      navigate(from, { replace: true });
    } catch (error) {
      const status = axios.isAxiosError(error)
        ? error.response?.status
        : undefined;
      setErrors({
        summary:
          status === 401
            ? // Neither the server nor this message says WHICH of the two was
              // wrong. Distinguishing them confirms that a username exists.
              "That username and password do not match an account."
            : // 429 in particular has something worth reading: the login
              // throttle keys on the username as well as the IP (DECISIONS §7.5),
              // and its message says how long to wait.
              apiErrorMessage(
                error,
                "Log in failed. Check your connection and try again.",
              ),
      });
    }
  }

  return (
    <AuthShell
      title="Log in"
      subtitle="You do not need an account to read Wikiverse."
      footer={
        <>
          No account?{" "}
          <Link to="/register" className={LINK}>
            Create one
          </Link>
          .
        </>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-3">
        {errors.summary && (
          <p
            role="alert"
            className="border-l-[6px] border-l-danger border-y border-r border-rule bg-panel px-3 py-2 text-ui text-ink"
          >
            {errors.summary}
          </p>
        )}

        <div>
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            name="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            autoCapitalize="none"
            spellCheck={false}
            aria-invalid={Boolean(errors.username) || undefined}
            aria-describedby={errors.username ? "username-error" : undefined}
            required
          />
          {errors.username && (
            <FieldError id="username-error">{errors.username}</FieldError>
          )}
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            aria-invalid={Boolean(errors.password) || undefined}
            aria-describedby={errors.password ? "password-error" : undefined}
            required
          />
          {errors.password && (
            <FieldError id="password-error">{errors.password}</FieldError>
          )}
        </div>

        <Button
          type="submit"
          size="lg"
          className="w-full"
          disabled={login.isPending}
        >
          {login.isPending && <Spinner label={null} />}
          Log in
        </Button>
      </form>
    </AuthShell>
  );
}
