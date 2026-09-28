import type { ReactNode } from "react";

import { useIsShelf, useIsTools } from "@/hooks/useMediaQuery";
import { cn } from "@/lib/utils";

interface WikiFrameProps {
  /** Left rail: site navigation, then the table of contents. */
  rail?: ReactNode;
  /** Right rail: Tools. Collapses into a disclosure at the foot below `tools`. */
  tools?: ReactNode;
  /**
   * Paint the reading surface (`--surface-page`) and give it the hairline side
   * rules. Off for pages that supply their own panels edge to edge.
   */
  paper?: boolean;
  className?: string;
  children: ReactNode;
}

/**
 * THE FRAME'S MAX-WIDTH IS THE SUM OF THE COLUMNS THAT ARE LIVE AT THAT WIDTH.
 *
 * Wikipedia's Vector 2022 declares one fixed 1596px frame and then lets the
 * rails come and go inside it, so a 1600px viewport shows a large dead gutter on
 * the right. The fix is arithmetic rather than a hack:
 *
 *   < shelf   (<960px)   content only                      54rem
 *   shelf     (≥960px)   rail + gap + content              12.25 + 1.5 + 54    = 67.75rem
 *   tools     (≥1312px)  rail + gap + content + gap + rail  67.75 + 1.5 + 12.25 = 81.5rem
 *
 * The content column is therefore always the same 864px and the whole assembly is
 * always optically centred, at every width.
 *
 * `min-w-0` on the content column is MANDATORY. Without it a wide `<pre>` or a
 * `<table>` inside a grid track pushes the track past `1fr` and the entire page
 * scrolls sideways — the classic CSS-grid overflow, and the reason the rule is
 * called out rather than merely written.
 *
 * `order-2 shelf:order-1` puts the rail after the article in the phone reading
 * order while keeping it visually first on the desktop grid. Below `shelf` the
 * site navigation lives in the masthead's disclosure instead, so the rail slot is
 * genuinely empty there rather than merely hidden.
 */
export function WikiFrame({
  rail,
  tools,
  paper = true,
  className,
  children,
}: WikiFrameProps) {
  const isShelf = useIsShelf();
  const isTools = useIsTools();

  // Rendered, not hidden. Mounting both copies of the Tools rail and hiding one
  // with `hidden` would duplicate every `id` and every landmark inside it, and
  // would run its observers twice.
  const hasRail = Boolean(rail);
  const hasTools = Boolean(tools);
  const showRail = isShelf && hasRail;
  const showToolsColumn = isTools && hasTools;
  const showToolsDisclosure = !isTools && hasTools;

  return (
    <div
      className={cn(
        "mx-auto w-full px-4 sm:px-6 tools:px-8",
        "grid max-w-[54rem] grid-cols-1 gap-x-6",
        // Only the columns a page actually supplies are declared. A track for an
        // absent rail would auto-place the content INTO the 12rem rail slot, and
        // an empty Tools track would push the page off centre.
        hasRail && "shelf:max-w-[67.75rem] shelf:grid-cols-[var(--rail-w)_minmax(0,1fr)]",
        hasRail &&
          hasTools &&
          "tools:max-w-[81.5rem] tools:grid-cols-[var(--rail-w)_minmax(0,1fr)_var(--rail-w)]",
        !hasRail &&
          hasTools &&
          "tools:max-w-[67.75rem] tools:grid-cols-[minmax(0,1fr)_var(--rail-w)]",
        className,
      )}
    >
      {showRail && (
        <div className="order-2 shelf:order-1 shelf:pt-10">{rail}</div>
      )}

      <div className="order-1 min-w-0 shelf:order-2">
        {paper ? (
          <div className="bg-page px-0 pb-16 shelf:border-x shelf:border-rule-hair shelf:px-8">
            {children}
            {showToolsDisclosure && (
              <ToolsDisclosure>{tools}</ToolsDisclosure>
            )}
          </div>
        ) : (
          <>
            {children}
            {showToolsDisclosure && <ToolsDisclosure>{tools}</ToolsDisclosure>}
          </>
        )}
      </div>

      {showToolsColumn && (
        <div className="order-3 tools:pt-10">{tools}</div>
      )}
    </div>
  );
}

/**
 * Below `tools` the right rail becomes a closed disclosure at the foot of the
 * article, above the category bar. A `<details>` rather than a floating panel:
 * it keeps the tools in document order, so they print and so a screen reader
 * meets them where they belong.
 */
function ToolsDisclosure({ children }: { children: ReactNode }) {
  return (
    <details className="mt-8 border-t border-rule-hair pt-2 text-ui print:hidden">
      <summary className="cursor-pointer list-none rounded-chrome py-1 font-semibold text-link hover:text-link-hover [&::-webkit-details-marker]:hidden">
        Tools
      </summary>
      <div className="mt-1">{children}</div>
    </details>
  );
}
