import { create } from "zustand";

/**
 * Tone is a 6px dot, never the toast's background.
 *
 * design-ui §4.21: if the body changed colour, a screenful of toasts becomes a
 * traffic light and the text contrast has to be re-argued per tone. One surface,
 * one ink, one coloured dot.
 */
export type ToastTone = "success" | "info" | "warning" | "error";

export interface ToastAction {
  label: string;
  onAction: () => void;
}

export interface Toast {
  id: string;
  tone: ToastTone;
  message: string;
  /** An optional second line, for the detail behind the headline. */
  detail?: string;
  action?: ToastAction;
  /**
   * Milliseconds until auto-dismiss, or `null` to require a dismissal.
   *
   * Errors default to `null`. An error that disappears on its own is an error
   * the reader is not allowed to finish reading.
   */
  duration: number | null;
}

export type ToastInput = Omit<Toast, "id" | "duration"> & {
  duration?: number | null;
};

const DEFAULT_DURATION = 6000;
/** Above this, the oldest non-error toast is dropped rather than stacked. */
const MAX_VISIBLE = 4;

interface ToastState {
  toasts: Toast[];
  push: (input: ToastInput) => string;
  dismiss: (id: string) => void;
  clear: () => void;
}

/**
 * Timers live outside the store. Putting them in state makes every tick a state
 * update, and makes the store non-serialisable for no benefit.
 */
const timers = new Map<string, ReturnType<typeof setTimeout>>();

function clearTimer(id: string): void {
  const timer = timers.get(id);
  if (timer !== undefined) {
    clearTimeout(timer);
    timers.delete(id);
  }
}

let seq = 0;

export const useToastStore = create<ToastState>()((set, get) => ({
  toasts: [],

  push: (input) => {
    const id = `t${++seq}`;
    const duration =
      input.duration !== undefined
        ? input.duration
        : input.tone === "error"
          ? null
          : DEFAULT_DURATION;

    const toast: Toast = { ...input, id, duration };

    set((state) => {
      const next = [...state.toasts, toast];
      if (next.length <= MAX_VISIBLE) return { toasts: next };
      // Drop the oldest dismissible toast; never silently drop an error.
      const victim = next.find((t) => t.duration !== null);
      if (!victim) return { toasts: next };
      clearTimer(victim.id);
      return { toasts: next.filter((t) => t.id !== victim.id) };
    });

    if (duration !== null) {
      timers.set(
        id,
        setTimeout(() => get().dismiss(id), duration),
      );
    }

    return id;
  },

  dismiss: (id) => {
    clearTimer(id);
    set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) }));
  },

  clear: () => {
    for (const id of timers.keys()) clearTimer(id);
    set({ toasts: [] });
  },
}));

/**
 * Imperative helpers, for the call sites that are not components — a mutation's
 * `onError`, an axios interceptor, an event handler.
 *
 * `toast.error(...)` never auto-dismisses. That is not an oversight.
 */
export const toast = {
  success: (message: string, extra?: Partial<ToastInput>) =>
    useToastStore.getState().push({ tone: "success", message, ...extra }),
  info: (message: string, extra?: Partial<ToastInput>) =>
    useToastStore.getState().push({ tone: "info", message, ...extra }),
  warning: (message: string, extra?: Partial<ToastInput>) =>
    useToastStore.getState().push({ tone: "warning", message, ...extra }),
  error: (message: string, extra?: Partial<ToastInput>) =>
    useToastStore.getState().push({ tone: "error", message, ...extra }),
  dismiss: (id: string) => useToastStore.getState().dismiss(id),
  clear: () => useToastStore.getState().clear(),
};
