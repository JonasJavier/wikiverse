import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { toast, useToastStore } from "./toast";

function toasts() {
  return useToastStore.getState().toasts;
}

beforeEach(() => {
  vi.useFakeTimers();
  toast.clear();
});

afterEach(() => {
  toast.clear();
  vi.useRealTimers();
});

describe("toast store", () => {
  it("pushes a toast with a unique id and the given tone", () => {
    const a = toast.success("Saved");
    const b = toast.info("Heads up", { detail: "More" });
    expect(a).not.toBe(b);
    expect(toasts()).toMatchObject([
      { id: a, tone: "success", message: "Saved" },
      { id: b, tone: "info", message: "Heads up", detail: "More" },
    ]);
  });

  it("auto-dismisses non-errors after 6 seconds", () => {
    toast.success("Saved");
    expect(toasts()[0].duration).toBe(6000);
    vi.advanceTimersByTime(5999);
    expect(toasts()).toHaveLength(1);
    vi.advanceTimersByTime(1);
    expect(toasts()).toHaveLength(0);
  });

  it("never auto-dismisses an error", () => {
    toast.error("Save failed");
    expect(toasts()[0].duration).toBeNull();
    vi.advanceTimersByTime(60_000);
    expect(toasts()).toHaveLength(1);
  });

  it("honours an explicit duration, including null", () => {
    toast.info("Short", { duration: 1000 });
    toast.warning("Sticky", { duration: null });
    vi.advanceTimersByTime(1000);
    expect(toasts().map((t) => t.message)).toEqual(["Sticky"]);
  });

  it("dismisses by id and cancels its timer", () => {
    const id = toast.success("Saved");
    toast.dismiss(id);
    expect(toasts()).toHaveLength(0);
    expect(vi.getTimerCount()).toBe(0);
  });

  it("keeps at most four, dropping the oldest dismissible toast", () => {
    toast.error("E1");
    toast.info("I1");
    toast.info("I2");
    toast.info("I3");
    toast.info("I4");
    expect(toasts().map((t) => t.message)).toEqual(["E1", "I2", "I3", "I4"]);
  });

  it("never drops an error to make room", () => {
    for (const n of [1, 2, 3, 4, 5]) toast.error(`E${n}`);
    expect(toasts().map((t) => t.message)).toEqual(["E1", "E2", "E3", "E4", "E5"]);
  });

  it("clear removes everything and every pending timer", () => {
    toast.success("a");
    toast.info("b");
    toast.clear();
    expect(toasts()).toEqual([]);
    expect(vi.getTimerCount()).toBe(0);
  });
});
