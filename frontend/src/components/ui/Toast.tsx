import { X } from "lucide-react";

import { cn } from "@/lib/utils";
import { type Toast as ToastData, useToastStore } from "@/store/toast";

const TONE_DOT: Record<ToastData["tone"], string> = {
  success: "bg-ok",
  info: "bg-link",
  warning: "bg-warn",
  error: "bg-danger",
};

/**
 * One toast. Body surface and ink never vary by tone — the tone is a 6px dot
 * (design-ui §4.21). Two channels for the reader who cannot see the dot's hue:
 * the dot's position is fixed, and the message says what happened in words.
 */
function ToastItem({ toast }: { toast: ToastData }) {
  const dismiss = useToastStore((s) => s.dismiss);
  const isError = toast.tone === "error";

  return (
    <div
      // `role` is on the item, `aria-live` on the viewport region below. An
      // error is the only tone that interrupts.
      role={isError ? "alert" : "status"}
      className={cn(
        "pointer-events-auto flex items-start gap-2 rounded-chrome border border-rule",
        "bg-page px-3 py-2 text-ui text-ink shadow-[var(--shadow-dialog)]",
        "motion-safe:animate-[toast-in_160ms_ease-out]",
      )}
    >
      <span
        aria-hidden="true"
        className={cn("mt-1.5 size-1.5 shrink-0 rounded-full", TONE_DOT[toast.tone])}
      />
      <div className="min-w-0 flex-1">
        <p className="text-ink">{toast.message}</p>
        {toast.detail && <p className="mt-0.5 text-xs text-ink-2">{toast.detail}</p>}
      </div>
      {toast.action && (
        <button
          type="button"
          onClick={() => {
            toast.action?.onAction();
            dismiss(toast.id);
          }}
          className="shrink-0 rounded-chrome font-medium text-link hover:text-link-hover hover:underline"
        >
          {toast.action.label}
        </button>
      )}
      <button
        type="button"
        onClick={() => dismiss(toast.id)}
        aria-label="Dismiss notification"
        className="-mr-1 grid size-5 shrink-0 place-items-center rounded-chrome text-ink-2 hover:bg-panel hover:text-ink"
      >
        <X className="size-3.5" aria-hidden="true" />
      </button>
    </div>
  );
}

/**
 * The toast region. Mounted once, in `Layout.tsx`.
 *
 * Both live regions are ALWAYS in the DOM, even when empty. A live region that
 * is created at the same moment its content arrives is not announced by any
 * screen reader — the single most common way a toast system ends up silent.
 *
 * Two regions rather than one, because politeness is per region, not per node:
 * success and info wait for a pause; an error interrupts.
 *
 * `pointer-events-none` on the column with `pointer-events-auto` on each toast,
 * so the fixed region never swallows clicks on the page beneath it.
 */
export function ToastViewport() {
  const toasts = useToastStore((s) => s.toasts);
  const polite = toasts.filter((t) => t.tone !== "error");
  const assertive = toasts.filter((t) => t.tone === "error");

  return (
    <div
      className={cn(
        "pointer-events-none fixed bottom-4 left-1/2 z-50 -translate-x-1/2",
        "flex w-[min(28rem,calc(100vw-2rem))] flex-col gap-2 print:hidden",
      )}
    >
      <div aria-live="polite" aria-atomic="false" className="flex flex-col gap-2">
        {polite.map((toast) => (
          <ToastItem key={toast.id} toast={toast} />
        ))}
      </div>
      <div aria-live="assertive" aria-atomic="false" className="flex flex-col gap-2">
        {assertive.map((toast) => (
          <ToastItem key={toast.id} toast={toast} />
        ))}
      </div>
    </div>
  );
}
