import {
  Bold,
  Braces,
  Italic,
  Link2,
  List,
  Quote,
  Superscript,
  Table,
} from "lucide-react";
import type { RefObject } from "react";

import type { EditorInsertion } from "@/api/editor";
import { cn } from "@/lib/utils";

/**
 * One toolbar entry.
 *
 * `label` is TEXT and it is always rendered — design-ui §5.6: "every toolbar
 * button has a text label, not only an icon". The icon is decorative and
 * `aria-hidden`; it is there so the toolbar can be scanned at a glance, not so
 * the label can be dropped. `hint` goes in `title` and in the accessible name,
 * because "H2" alone does not say what it does.
 */
interface ToolbarItem {
  label: string;
  hint: string;
  icon?: typeof Bold;
  insertion: EditorInsertion;
}

const TOOLBAR: ToolbarItem[][] = [
  [
    {
      label: "H2",
      hint: "Section heading",
      insertion: { before: "## ", placeholder: "Section", block: true },
    },
    {
      label: "H3",
      hint: "Subsection heading",
      insertion: { before: "### ", placeholder: "Subsection", block: true },
    },
  ],
  [
    {
      label: "Bold",
      hint: "Bold",
      icon: Bold,
      insertion: { before: "**", after: "**", placeholder: "bold text" },
    },
    {
      label: "Italic",
      hint: "Italic",
      icon: Italic,
      insertion: { before: "*", after: "*", placeholder: "italic text" },
    },
  ],
  [
    {
      label: "[[Link]]",
      hint: "Link to another article in this encyclopedia",
      insertion: { before: "[[", after: "]]", placeholder: "Article Title" },
    },
    {
      label: "URL",
      hint: "Link to a page outside this encyclopedia",
      icon: Link2,
      insertion: { before: "[", after: "](https://)", placeholder: "link text" },
    },
    {
      label: "[^ref]",
      hint: "Citation marker — it must match a reference key below",
      icon: Superscript,
      insertion: { before: "[^", after: "]", placeholder: "key" },
    },
  ],
  [
    {
      label: "List",
      hint: "Bulleted list",
      icon: List,
      insertion: { before: "- ", placeholder: "item", block: true },
    },
    {
      label: "Quote",
      hint: "Block quotation",
      icon: Quote,
      insertion: { before: "> ", placeholder: "quoted text", block: true },
    },
    {
      label: "Table",
      hint: "Table",
      icon: Table,
      insertion: {
        before: "| ",
        after: " | Value |\n| --- | --- |\n|  |  |",
        placeholder: "Column",
        block: true,
      },
    },
    {
      label: "Code",
      hint: "Fenced code block",
      icon: Braces,
      insertion: {
        before: "```\n",
        after: "\n```",
        placeholder: "code",
        block: true,
      },
    },
  ],
];

interface MarkdownEditorProps {
  id: string;
  value: string;
  onChange: (next: string) => void;
  /** Owned by the page, so the reference editor writes into the same textarea. */
  textareaRef: RefObject<HTMLTextAreaElement | null>;
  /** The one implementation of "put this at the caret". */
  onInsert: (insertion: EditorInsertion) => void;
  /** Ids of the hint and error lines, for `aria-describedby`. */
  describedBy?: string;
  invalid?: boolean;
}

/**
 * The body field: a plain `<textarea>` on the inset surface in the mono voice,
 * with a toolbar that only ever inserts markup at the caret.
 *
 * Deliberately NOT a rich-text or CodeMirror surface. The thing being edited is
 * Markdown, the preview pane already shows the result, and a contenteditable
 * would put a second, divergent idea of the document between the author and the
 * text they typed. It also keeps `Tab` doing what `Tab` does — moving focus.
 * Hijacking it for indentation is the classic keyboard trap, and a11y is a gate
 * here.
 */
export function MarkdownEditor({
  id,
  value,
  onChange,
  textareaRef,
  onInsert,
  describedBy,
  invalid,
}: MarkdownEditorProps) {
  const words = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <div>
      {/* `role="group"`, not `role="toolbar"`: a toolbar promises arrow-key
          navigation and a single tab stop, and claiming a pattern that is not
          implemented is worse for a screen-reader user than a plain group of
          buttons, which is exactly what this is. */}
      <div
        role="group"
        aria-label="Markup"
        className={cn(
          "flex flex-wrap items-center gap-x-1 gap-y-1 rounded-t-chrome",
          "border border-b-0 border-rule bg-panel px-1.5 py-1",
        )}
      >
        {TOOLBAR.map((group, index) => (
          <div key={group[0].label} className="flex items-center gap-1">
            {index > 0 && (
              <span aria-hidden="true" className="mx-0.5 h-4 w-px bg-rule" />
            )}
            {group.map((item) => (
              <button
                key={item.label}
                type="button"
                title={item.hint}
                aria-label={`${item.label} — ${item.hint}`}
                onClick={() => onInsert(item.insertion)}
                className={cn(
                  "inline-flex h-7 cursor-pointer items-center gap-1 rounded-chrome px-1.5",
                  "text-2xs text-ink-2 transition-colors duration-100",
                  "hover:bg-inset hover:text-ink",
                )}
              >
                {item.icon && (
                  <item.icon aria-hidden="true" className="size-3.5" />
                )}
                <span className="font-mono">{item.label}</span>
              </button>
            ))}
          </div>
        ))}
      </div>

      <textarea
        id={id}
        ref={textareaRef}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        spellCheck
        aria-describedby={describedBy}
        aria-invalid={invalid || undefined}
        style={{ tabSize: 2 }}
        placeholder={
          "**Photosynthesis** is the process by which…\n\n" +
          "## History\n\nLinked with [[Joseph Priestley]] and cited with [^priestley1772]."
        }
        className={cn(
          "block w-full resize-y rounded-b-chrome border border-rule bg-inset",
          "px-3 py-2.5 font-mono text-[0.9375rem] leading-[1.6] text-ink",
          "placeholder:text-ink-3 min-h-[24rem] shelf:min-h-[60vh]",
          "aria-[invalid=true]:border-danger",
        )}
      />

      <p className="mt-1 flex justify-between gap-3 text-2xs text-ink-3">
        <span>
          <code className="font-mono">[[Title]]</code> links an article ·{" "}
          <code className="font-mono">[^key]</code> cites a reference
        </span>
        <span>
          {words.toLocaleString("en")} {words === 1 ? "word" : "words"}
        </span>
      </p>
    </div>
  );
}
