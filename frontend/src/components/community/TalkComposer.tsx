import { type ReactNode, useId, useState } from "react";
import { Link } from "react-router-dom";

import { Markdown } from "@/components/article/Markdown";
import { Button } from "@/components/ui/Button";
import { FieldError, Input, Label, Textarea } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/Spinner";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";

export interface TalkComposerValue {
  /** Only present when `withTitle` is set. */
  title?: string;
  body: string;
}

export interface TalkComposerProps {
  /** e.g. `"Post reply"`, `"Add topic"`, `"Save changes"`. */
  submitLabel: string;
  /** Collect a thread title as well as a body. For the new-topic composer. */
  withTitle?: boolean;
  initialTitle?: string;
  initialBody?: string;
  placeholder?: string;
  /** One line under the controls, e.g. what markup is accepted. */
  note?: ReactNode;
  busy?: boolean;
  autoFocus?: boolean;
  onSubmit: (value: TalkComposerValue) => void;
  onCancel?: () => void;
  className?: string;
}

/**
 * The one composer: new topic, reply and edit all use it.
 *
 * **Markdown goes through the same renderer as an article body.** The preview
 * mounts `components/article/Markdown.tsx` rather than a second pipeline,
 * which is the whole point: DECISIONS §0.5 and §12 require `react-markdown`
 * without `rehype-raw` for talk messages exactly as for articles, and the
 * cheapest way to guarantee that is to have no second renderer to get wrong.
 *
 * **An anonymous reader sees the composer, disabled, with a reason.** Hiding
 * it would leave the page looking as if discussion were closed; showing an
 * enabled box that 401s on submit is worse. `CanPostToTalk` requires
 * authentication, so the UI says so before the keystroke.
 *
 * The draft lives in local state, and deliberately so: DECISIONS' "filters
 * live in the URL" rule is about *views*, and putting half a sentence in the
 * address bar on every keystroke would be its own bug. To clear a composer
 * after a successful post, remount it with a changed `key`.
 */
export function TalkComposer({
  submitLabel,
  withTitle = false,
  initialTitle = "",
  initialBody = "",
  placeholder = "Write your comment. Markdown is supported; raw HTML is not.",
  note,
  busy = false,
  autoFocus = false,
  onSubmit,
  onCancel,
  className,
}: TalkComposerProps) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [title, setTitle] = useState(initialTitle);
  const [body, setBody] = useState(initialBody);
  const [preview, setPreview] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const titleId = useId();
  const bodyId = useId();
  const noteId = useId();
  const errorId = useId();

  function submit(): void {
    const trimmedBody = body.trim();
    const trimmedTitle = title.trim();

    if (withTitle && trimmedTitle.length < 3) {
      setError("A topic title needs at least three characters.");
      return;
    }
    if (!trimmedBody) {
      setError("A comment needs something in it.");
      return;
    }

    setError(null);
    onSubmit(
      withTitle ? { title: trimmedTitle, body: trimmedBody } : { body: trimmedBody },
    );
  }

  return (
    <div
      className={cn(
        "rounded-chrome border border-rule-hair bg-panel p-3",
        className,
      )}
    >
      {!isAuthenticated && (
        <p className="mb-2 text-ui text-ink-2">
          <Link to="/login" className="text-link hover:underline">
            Sign in
          </Link>{" "}
          to join this discussion. Anonymous readers can read every talk page
          but cannot post to one.
        </p>
      )}

      {withTitle && (
        <div className="mb-2">
          <Label htmlFor={titleId}>Topic title</Label>
          <Input
            id={titleId}
            value={title}
            disabled={!isAuthenticated || busy}
            autoFocus={autoFocus}
            maxLength={200}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="What should change, and why"
          />
        </div>
      )}

      <Label htmlFor={bodyId}>Comment</Label>
      {preview ? (
        <div
          className="min-h-24 rounded-chrome border border-rule bg-page px-2.5 py-1.5"
          aria-label="Comment preview"
        >
          {body.trim() ? (
            <Markdown content={body} headings={false} />
          ) : (
            <p className="text-ui text-ink-3">Nothing to preview yet.</p>
          )}
        </div>
      ) : (
        <Textarea
          id={bodyId}
          value={body}
          rows={withTitle ? 6 : 4}
          disabled={!isAuthenticated || busy}
          autoFocus={autoFocus && !withTitle}
          aria-invalid={error ? true : undefined}
          aria-describedby={cn(note ? noteId : "", error ? errorId : "").trim() || undefined}
          onChange={(event) => setBody(event.target.value)}
          placeholder={placeholder}
        />
      )}

      {error && <FieldError id={errorId}>{error}</FieldError>}

      <div className="mt-2 flex flex-wrap items-center gap-2">
        <Button
          onClick={submit}
          disabled={!isAuthenticated || busy}
          aria-disabled={!isAuthenticated || undefined}
        >
          {busy && <Spinner label={null} />}
          {submitLabel}
        </Button>
        <Button
          variant="secondary"
          aria-pressed={preview}
          onClick={() => setPreview((value) => !value)}
        >
          {preview ? "Keep writing" : "Preview"}
        </Button>
        {onCancel && (
          <Button variant="ghost" onClick={onCancel} disabled={busy}>
            Cancel
          </Button>
        )}
      </div>

      {note && (
        <p id={noteId} className="mt-1.5 text-2xs text-ink-2">
          {note}
        </p>
      )}
    </div>
  );
}
