import type { ReactNode } from "react";

/**
 * The frame around Log in and Register.
 *
 * The floating `rounded-2xl` card with its shadow is gone (design-ui §5.15).
 * Rule 2 of the design system is "rules, not shadows": a shadow belongs only to
 * something that floats above the document and can be dismissed — a menu, a
 * hover card, a dialog, a toast. A sign-in form is the page, so it gets the same
 * title block as every other page: serif `h1` at weight 400, one hairline rule
 * under it, one line of context.
 *
 * `24rem`, not `28rem`: a username and a password are short fields, and a form
 * as wide as an article's measure reads as a landing page.
 */
interface AuthShellProps {
  /** The `h1`. One per page, and this is it. */
  title: string;
  /** One line under the rule. Context, not marketing. */
  subtitle: ReactNode;
  children: ReactNode;
  /** The cross-link to the other form, below a hairline. */
  footer: ReactNode;
}

export function AuthShell({
  title,
  subtitle,
  children,
  footer,
}: AuthShellProps) {
  return (
    <div className="mx-auto w-full max-w-[24rem] px-4 py-10">
      <h1 className="font-serif text-h1 font-normal text-ink">{title}</h1>
      <hr className="mt-1.5 border-0 border-t border-rule" />
      <p className="mt-1.5 text-ui text-ink-2">{subtitle}</p>

      <div className="mt-5">{children}</div>

      <p className="mt-4 border-t border-rule-hair pt-3 text-ui text-ink-2">
        {footer}
      </p>
    </div>
  );
}
