import axios from "axios";
import { type FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useRegister } from "@/api/auth";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/Button";
import { FieldError, FieldHint, Input, Label } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/Spinner";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";

const LINK = "text-link hover:text-link-hover hover:underline";

/** The four fields `RegisterSerializer` accepts, plus the error summary. */
type RegisterField = "username" | "email" | "password" | "password_confirm";
type RegisterErrors = Partial<Record<RegisterField | "summary", string>>;

const LABELS: Record<RegisterField, string> = {
  username: "Username",
  email: "Email",
  password: "Password",
  password_confirm: "Confirm password",
};

/**
 * Create an account.
 *
 * The server-error mapping is the point of this page. Django's
 * `validate_password` rejects a password for four different reasons, each with
 * its own sentence, and `RegisterSerializer.validate` returns a mismatch under
 * `password_confirm` specifically. Flattening all of that into one toast — which
 * is what the old page did with `apiErrorMessage` — told the reader "Could not
 * create the account" and left them guessing which field to change. Every message
 * here lands under the control it is about, and the summary above the form exists
 * so a screen-reader user hears that something failed without having to go
 * hunting for it.
 */
export function RegisterPage() {
  const register = useRegister();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    password_confirm: "",
  });
  const [errors, setErrors] = useState<RegisterErrors>({});

  useDocumentMeta({
    title: "Create an account",
    description:
      "Create a Wikiverse account to write and edit articles. Reading needs no account.",
    robots: "noindex",
  });

  function update(field: RegisterField) {
    return (event: React.ChangeEvent<HTMLInputElement>) => {
      setForm((current) => ({ ...current, [field]: event.target.value }));
      // Clear this field's error as soon as it is being addressed; leaving a
      // stale message under a field the reader is fixing is its own small lie.
      setErrors((current) =>
        current[field] ? { ...current, [field]: undefined } : current,
      );
    };
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const next: RegisterErrors = {};
    if (form.username.trim().length < 3) {
      next.username = "Pick a username of at least 3 characters.";
    }
    if (!form.email.trim()) {
      next.email = "Enter an email address.";
    }
    if (form.password.length < 8) {
      next.password = "Use at least 8 characters.";
    }
    if (form.password_confirm !== form.password) {
      next.password_confirm = "The two passwords do not match.";
    }
    if (Object.values(next).some(Boolean)) {
      setErrors({ ...next, summary: "This account cannot be created yet." });
      return;
    }

    setErrors({});

    try {
      await register.mutateAsync({ ...form, username: form.username.trim() });
      navigate("/", { replace: true });
    } catch (error) {
      setErrors(serverErrors(error));
    }
  }

  const problems = (Object.keys(LABELS) as RegisterField[]).filter(
    (field) => errors[field],
  );

  return (
    <AuthShell
      title="Create an account"
      subtitle="An account lets you write and edit. Reading never needs one."
      footer={
        <>
          Already have an account?{" "}
          <Link to="/login" className={LINK}>
            Log in
          </Link>
          .
        </>
      }
    >
      <form onSubmit={handleSubmit} noValidate className="space-y-3">
        {errors.summary && (
          <div
            role="alert"
            className="border-l-[6px] border-l-danger border-y border-r border-rule bg-panel px-3 py-2 text-ui text-ink"
          >
            <p>{errors.summary}</p>
            {problems.length > 0 && (
              <ul className="mt-1 list-disc space-y-0.5 pl-5">
                {problems.map((field) => (
                  <li key={field}>
                    <span className="font-medium">{LABELS[field]}:</span>{" "}
                    {errors[field]}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div>
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            name="username"
            value={form.username}
            onChange={update("username")}
            autoComplete="username"
            autoCapitalize="none"
            spellCheck={false}
            aria-invalid={Boolean(errors.username) || undefined}
            aria-describedby="username-hint"
            required
          />
          <FieldHint id="username-hint">
            This is the name your edits are signed with, in every page history.
          </FieldHint>
          {errors.username && <FieldError>{errors.username}</FieldError>}
        </div>

        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            name="email"
            type="email"
            inputMode="email"
            value={form.email}
            onChange={update("email")}
            autoComplete="email"
            autoCapitalize="none"
            spellCheck={false}
            aria-invalid={Boolean(errors.email) || undefined}
            aria-describedby="email-hint"
            required
          />
          <FieldHint id="email-hint">
            Never shown to other readers, and never served by the API to anyone
            but you.
          </FieldHint>
          {errors.email && <FieldError>{errors.email}</FieldError>}
        </div>

        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={update("password")}
            autoComplete="new-password"
            aria-invalid={Boolean(errors.password) || undefined}
            aria-describedby="password-hint"
            required
          />
          <FieldHint id="password-hint">
            At least 8 characters, and not one of the common ones.
          </FieldHint>
          {errors.password && <FieldError>{errors.password}</FieldError>}
        </div>

        <div>
          <Label htmlFor="password_confirm">Confirm password</Label>
          <Input
            id="password_confirm"
            name="password_confirm"
            type="password"
            value={form.password_confirm}
            onChange={update("password_confirm")}
            autoComplete="new-password"
            aria-invalid={Boolean(errors.password_confirm) || undefined}
            aria-describedby={
              errors.password_confirm ? "password-confirm-error" : undefined
            }
            required
          />
          {errors.password_confirm && (
            <FieldError id="password-confirm-error">
              {errors.password_confirm}
            </FieldError>
          )}
        </div>

        <Button
          type="submit"
          size="lg"
          className="w-full"
          disabled={register.isPending}
        >
          {register.isPending && <Spinner label={null} />}
          Create account
        </Button>
      </form>
    </AuthShell>
  );
}

/**
 * A DRF 400 from `RegisterSerializer` → one message per field.
 *
 * `validate_password` returns a LIST of sentences ("This password is too short…",
 * "This password is too common."). They are joined rather than truncated,
 * because each one is a separate thing to fix.
 */
function serverErrors(error: unknown): RegisterErrors {
  if (!axios.isAxiosError(error)) {
    return { summary: "The account could not be created. Please try again." };
  }

  if (error.response?.status === 429) {
    return {
      summary:
        typeof (error.response.data as { detail?: unknown })?.detail === "string"
          ? String((error.response.data as { detail: string }).detail)
          : "Too many attempts. Please wait a moment and try again.",
    };
  }

  const data = error.response?.data;
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    return {
      summary:
        "The account could not be created. Check your connection and try again.",
    };
  }

  const out: RegisterErrors = {};
  const fields = new Set<string>(Object.keys(LABELS));

  for (const [field, value] of Object.entries(data as Record<string, unknown>)) {
    const message = Array.isArray(value)
      ? value.filter((item) => typeof item === "string").join(" ")
      : typeof value === "string"
        ? value
        : "";
    if (!message) continue;
    if (fields.has(field)) out[field as RegisterField] = message;
    else out.summary = message;
  }

  out.summary ??= "This account cannot be created yet.";
  return out;
}
