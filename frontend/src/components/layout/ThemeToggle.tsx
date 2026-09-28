import { Monitor, Moon, Sun } from "lucide-react";

import { type ThemeChoice, useThemeStore } from "@/store/theme";

const LABELS: Record<ThemeChoice, string> = {
  light: "Light theme",
  dark: "Dark theme",
  system: "System theme",
};

const NEXT: Record<ThemeChoice, ThemeChoice> = {
  light: "dark",
  dark: "system",
  system: "light",
};

/**
 * Three states — light, dark, system — cycled in that order. The icon shows the
 * current choice and the label names the next one, so "system" is always one
 * click away and never a state the reader can lose.
 */
export function ThemeToggle() {
  const choice = useThemeStore((s) => s.choice);
  const cycle = useThemeStore((s) => s.cycle);
  const Icon = choice === "light" ? Sun : choice === "dark" ? Moon : Monitor;
  const label = `${LABELS[choice]} (switch to ${LABELS[NEXT[choice]].toLowerCase()})`;

  return (
    <button
      type="button"
      onClick={cycle}
      aria-label={label}
      title={label}
      className="grid size-8 place-items-center rounded-chrome text-ink-2 hover:bg-panel hover:text-ink"
    >
      <Icon className="size-4" aria-hidden="true" />
    </button>
  );
}
