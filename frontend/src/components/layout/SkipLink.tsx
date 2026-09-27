/**
 * The first focusable element in the document.
 *
 * With a masthead carrying a hamburger, a wordmark, a search combobox, two icon
 * links, a theme toggle and a user menu, a keyboard reader traversed roughly
 * eight controls before reaching the article — on every page. There was no skip
 * link at all; this is the cheapest accessibility fix in the app.
 *
 * `sr-only` until focused, then a real, visible, positioned control. The target
 * is `<main id="content" tabIndex={-1}>` in `Layout.tsx`: without `tabIndex={-1}`
 * the jump moves the SCROLL position but not the keyboard position in Safari and
 * Firefox, so the next `Tab` returns to the masthead and the link achieves
 * nothing.
 */
export function SkipLink() {
  return (
    <a
      href="#content"
      className={
        "sr-only focus-visible:not-sr-only focus-visible:fixed focus-visible:top-2 " +
        "focus-visible:left-2 focus-visible:z-50 focus-visible:rounded-chrome " +
        "focus-visible:border focus-visible:border-rule focus-visible:bg-page " +
        "focus-visible:px-3 focus-visible:py-2 focus-visible:text-ui " +
        "focus-visible:font-medium focus-visible:text-ink " +
        "focus-visible:shadow-[var(--shadow-dialog)]"
      }
    >
      Skip to content
    </a>
  );
}
