import { Eye, Save, X } from "lucide-react";

import { LIMITS } from "@/api/editor";
import { Button } from "@/components/ui/Button";
import { Input, Label } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/Spinner";

interface EditSummaryBarProps {
  comment: string;
  onCommentChange: (next: string) => void;
  isMinor: boolean;
  onMinorChange: (next: boolean) => void;
  isPublished: boolean;
  onPublishedChange: (next: boolean) => void;
  watch: boolean;
  onWatchChange: (next: boolean) => void;
  /** Hidden for an anonymous session; watching needs an account. */
  canWatch: boolean;
  /** Below `shelf` the preview is a tab, so the button switches to it. */
  onPreview: () => void;
  showPreviewButton: boolean;
  onSave: () => void;
  onCancel: () => void;
  saving: boolean;
  dirty: boolean;
  /** `true` on `/wiki/:slug/edit`, `false` on `/new`. Changes the verbs. */
  isEdit: boolean;
  commentError?: string;
}

const CHECKBOX = "size-4 shrink-0 accent-[var(--ink-1)]";

/**
 * The foot of the editor: what this edit is, and the three things that can be
 * done with it.
 *
 * It is `sticky bottom-0`, because the save control on a page whose main field
 * is 60vh tall must not be a scroll away — and because "where is the save
 * button" is the one question a first-time editor should never have to ask.
 * The bar is opaque and separated by a hairline rule rather than a shadow: it is
 * part of the document, not floating above it.
 *
 * `Show changes` is deliberately absent. design-ui §5.6 asks for it against the
 * current revision, but `DiffViewer` belongs to another area and is not landed;
 * a button that throws is worse than a button that is not there. See the report.
 */
export function EditSummaryBar({
  comment,
  onCommentChange,
  isMinor,
  onMinorChange,
  isPublished,
  onPublishedChange,
  watch,
  onWatchChange,
  canWatch,
  onPreview,
  showPreviewButton,
  onSave,
  onCancel,
  saving,
  dirty,
  isEdit,
  commentError,
}: EditSummaryBarProps) {
  return (
    <div className="sticky bottom-0 z-10 mt-4 border-t border-rule bg-page pt-3 pb-3">
      <div>
        <Label htmlFor="edit-comment">Edit summary</Label>
        <Input
          id="edit-comment"
          value={comment}
          onChange={(event) => onCommentChange(event.target.value)}
          maxLength={LIMITS.comment}
          aria-invalid={Boolean(commentError) || undefined}
          aria-describedby="edit-comment-hint"
          placeholder={
            isEdit
              ? "Briefly describe what you changed, and why"
              : "Created the article"
          }
        />
        <p id="edit-comment-hint" className="mt-1 text-2xs text-ink-2">
          {commentError ? (
            <span className="text-danger">{commentError}</span>
          ) : (
            <>
              This line is what other readers see in the page history and in
              Recent changes. {LIMITS.comment - comment.length} characters left.
            </>
          )}
        </p>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-2">
        <label className="flex items-center gap-2 text-ui text-ink">
          <input
            type="checkbox"
            className={CHECKBOX}
            checked={isMinor}
            onChange={(event) => onMinorChange(event.target.checked)}
          />
          Minor edit
        </label>

        {canWatch && (
          <label className="flex items-center gap-2 text-ui text-ink">
            <input
              type="checkbox"
              className={CHECKBOX}
              checked={watch}
              onChange={(event) => onWatchChange(event.target.checked)}
            />
            Watch this page
          </label>
        )}

        <label className="flex items-center gap-2 text-ui text-ink">
          <input
            type="checkbox"
            className={CHECKBOX}
            checked={!isPublished}
            onChange={(event) => onPublishedChange(!event.target.checked)}
          />
          Save as a draft
        </label>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        {/* `type="button"`, not `"submit"`: the surrounding form already calls
            the same handler on submit, and a submit button that ALSO carries an
            onClick saves twice. */}
        <Button size="lg" onClick={onSave} disabled={saving}>
          {saving ? (
            <Spinner label={null} />
          ) : (
            <Save aria-hidden="true" className="size-4" />
          )}
          {isEdit ? "Save changes" : "Publish page"}
        </Button>

        {showPreviewButton && (
          <Button variant="secondary" size="lg" onClick={onPreview}>
            <Eye aria-hidden="true" className="size-4" />
            Show preview
          </Button>
        )}

        <Button variant="secondary" size="lg" onClick={onCancel} disabled={saving}>
          <X aria-hidden="true" className="size-4" />
          Cancel
        </Button>

        <span className="text-2xs text-ink-2" aria-live="polite">
          {dirty ? "Unsaved changes" : ""}
        </span>
      </div>
    </div>
  );
}
