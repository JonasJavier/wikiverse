import type { ComponentProps } from "react";

import {
  buttonVariants,
  type ButtonSize,
  type ButtonVariant,
} from "@/components/ui/buttonVariants";
import { cn } from "@/lib/utils";

interface ButtonProps extends ComponentProps<"button"> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

/**
 * Same `variant × size` API as before, retuned values (see
 * `buttonVariants.ts`). React 19 passes `ref` as an ordinary prop, so there
 * is no `forwardRef` wrapper and no `displayName` to keep in sync.
 *
 * `type` defaults to `"button"`. A bare `<button>` inside a form submits it,
 * which is how a Cancel control ends up saving an article.
 */
export function Button({ className, variant, size, type, ...props }: ButtonProps) {
  return (
    <button
      type={type ?? "button"}
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}
