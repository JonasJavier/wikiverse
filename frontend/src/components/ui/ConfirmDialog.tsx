import { type ReactNode, useEffect, useId, useRef, useState } from "react";

import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { cn } from "@/lib/utils";

export interface ConfirmDialogProps {
  open: boolean;
  /** The question, e.g. `Delete “Marie Curie”?`. Rendered as the dialog's h2. */
  title: string;
  /**
   * What else is destroyed. A destructive confirmation on a wiki has to name the
   * collateral — the revisions, the talk threads — which is the one thing a
   * `window.confirm` string cannot do well.
   */
  body?: ReactNode;
  /**
   * When set, a required checkbox carrying this label. The confirm button stays
   * disabled until it is ticked.
   */
  acknowledge?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  tone?: "default" | "danger";
  /** Disables both buttons and shows a spinner while the mutation runs. */
  busy?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

/**
 * A native `<dialog>` driven by `showModal()`.
 *
 * This replaces `window.confirm`, which was blocking, unthemed, ignored dark
 * mode, could not name what else was being destroyed, and — the reason it
 * blocked the test work — needs a Playwright dialog handler rather than being
 * drivable as ordinary DOM.
 *
 * `showModal()` is chosen over a hand-rolled overlay because the platform then
 * owns the parts that are always got wrong: the focus trap, `Escape`, the
 * inertness of everything behind it (real `inert`, not `aria-hidden`), and the
 * top-layer stacking that no `z-index` can be wrong about.
 *
 * What the platform does NOT give, and is added here:
 *   - Backdrop click to dismiss. A click on `::backdrop` targets the dialog
 *     element itself, so comparing `event.target` to the dialog distinguishes it
 *     from a click on the contents.
 *   - Scroll lock. A modal dialog is inert-behind but the page still scrolls.
 *   - Focus placed on the SAFE control. The destructive button must never be
 *     what `Enter` hits on open.
 */
export function ConfirmDialog({
  open,
  title,
  body,
  acknowledge,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  tone = "default",
  busy = false,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  const ref = useRef<HTMLDialogElement>(null);
  const cancelRef = useRef<HTMLButtonElement>(null);
  const [acknowledged, setAcknowledged] = useState(false);
  const titleId = useId();
  const bodyId = useId();

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;

    if (open) {
      if (!dialog.open) dialog.showModal();
      setAcknowledged(false);
      // Focus the safe control, not the destructive one.
      cancelRef.current?.focus();
      const { overflow } = document.documentElement.style;
      document.documentElement.style.overflow = "hidden";
      return () => {
        document.documentElement.style.overflow = overflow;
      };
    }

    if (dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      aria-labelledby={titleId}
      aria-describedby={body ? bodyId : undefined}
      // `close` covers Escape, the platform's own dismissal and our own
      // `dialog.close()`, so there is exactly one path out.
      onClose={() => {
        if (open) onCancel();
      }}
      onClick={(event) => {
        if (event.target === ref.current && !busy) onCancel();
      }}
      className={cn(
        "m-auto w-[min(30rem,calc(100vw-2rem))] rounded-chrome border border-rule",
        "bg-page p-0 text-ink shadow-[var(--shadow-dialog)]",
        "backdrop:bg-black/40 backdrop:motion-safe:animate-[menu-in_120ms_linear]",
      )}
    >
      <div className="p-4">
        <h2 id={titleId} className="font-serif text-h2 font-normal text-ink">
          {title}
        </h2>
        <hr className="my-2 border-0 border-t border-rule" />
        {body && (
          <div id={bodyId} className="text-base text-ink">
            {body}
          </div>
        )}

        {acknowledge && (
          <label className="mt-3 flex items-start gap-2 text-ui text-ink">
            <input
              type="checkbox"
              checked={acknowledged}
              onChange={(event) => setAcknowledged(event.target.checked)}
              className="mt-0.5 size-4 shrink-0 accent-[var(--ink-1)]"
            />
            <span>{acknowledge}</span>
          </label>
        )}

        <div className="mt-4 flex items-center justify-end gap-2">
          <Button
            ref={cancelRef}
            variant="secondary"
            onClick={onCancel}
            disabled={busy}
          >
            {cancelLabel}
          </Button>
          <Button
            variant={tone === "danger" ? "danger" : "primary"}
            onClick={onConfirm}
            disabled={busy || (Boolean(acknowledge) && !acknowledged)}
          >
            {busy && <Spinner label={null} />}
            {confirmLabel}
          </Button>
        </div>
      </div>
    </dialog>
  );
}
