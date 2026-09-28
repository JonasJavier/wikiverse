import { cn, initials } from "@/lib/utils";

interface AvatarProps {
  name: string;
  src?: string | null;
  className?: string;
}

/**
 * `alt=""` is deliberate. In every place this appears — a history row, a
 * change row, a profile header — the username is already beside it as text,
 * so a real `alt` makes a screen reader announce the same name twice. An
 * empty `alt` on a decorative image is the correct answer, not an omission.
 *
 * `rounded-full` survives the radius-2px rule: an avatar is a picture of a
 * person, not chrome.
 */
export function Avatar({ name, src, className }: AvatarProps) {
  return (
    <span
      className={cn(
        "inline-flex size-8 shrink-0 items-center justify-center overflow-hidden",
        "rounded-full border border-rule-hair bg-panel text-2xs font-semibold text-ink-2",
        className,
      )}
    >
      {src ? (
        <img src={src} alt="" loading="lazy" decoding="async" className="size-full object-cover" />
      ) : (
        initials(name)
      )}
    </span>
  );
}
