import type { ReactNode } from "react";

import type { Infobox as InfoboxData, InfoboxRow } from "@/lib/types";
import { cn } from "@/lib/utils";
import { MarkdownInline } from "./Markdown";

export interface InfoboxProps {
  /** `Article.infobox`. `{}` or `null` means the article has none. */
  infobox: InfoboxData | null;
  /** Falls back to the article title when `infobox.title` is absent. */
  title: string;
  /** The image cell's contents — a `<LeadImage variant="infobox">`. */
  image?: ReactNode;
  /** Prefix for footnote source ids, so markers in values get distinct `n`. */
  sourceId?: string;
  className?: string;
}

/**
 * The infobox: a real `<table>` of facts, floated right.
 *
 * SCHEMA (DECISIONS §1, and this is the only valid shape): `title`, `subtitle`,
 * and `rows` of three kinds — `header{value}`, `row{label,value}` and
 * `full{value}`. Note that a `header` row carries `value`, NOT `label`. Every
 * `value` is a plain string that may contain `[[wikilinks]]`, `*emphasis*` and
 * `[^refkey]` markers, all resolved by the same renderer the body uses.
 *
 * THE INFOBOX NEVER CARRIES AN IMAGE. The lead image lives on `Article`
 * columns, and it is passed in as `image` so that this component cannot become
 * a second, competing source of truth for it.
 *
 * `role="presentation"` is deliberate. The infobox is a layout of label/value
 * pairs, not a data table with meaningful row *and* column relationships, and
 * announcing "table, 14 rows, 2 columns" before the lead sentence is worse than
 * reading the pairs as text. The `scope="row"` labels still read correctly.
 *
 * Styling is Tailwind-inline rather than the semantic `.infobox*` rules
 * design-ui §4.0 would prefer, because `index.css` is owned elsewhere and does
 * not carry them yet. The class names are still on the elements, so the
 * existing `.article-prose > .infobox` measure rule and the `@media print`
 * unfloat both match, and a later CSS pass can take the styling over without
 * touching this file.
 */
export function Infobox({ infobox, title, image, sourceId = "infobox", className }: InfoboxProps) {
  const rows = infobox?.rows ?? [];
  if (rows.length === 0 && !image) return null;

  const heading = infobox?.title?.trim() || title;
  const subtitle = infobox?.subtitle?.trim();

  return (
    <table
      role="presentation"
      className={cn(
        "infobox",
        // Below 768px: unfloated, full width, ABOVE the lead, keeping its border
        // and panel fill — it does not dissolve into the page.
        "mb-5 w-full table-fixed border-collapse rounded-chrome border border-rule bg-panel p-[0.2em]",
        "font-sans text-[0.824em] leading-normal [font-variant-numeric:tabular-nums]",
        // 768px and up: the float. 16rem until `shelf`, then the full 20rem.
        "md:float-right md:clear-right md:mt-[0.3em] md:mb-[0.8em] md:ml-[1em] md:w-[16rem]",
        "shelf:w-[var(--infobox-w)]",
        className,
      )}
    >
      <caption className="infobox-above caption-top px-[0.5em] py-[0.4em] text-center text-[1.25em] font-semibold text-ink">
        {heading}
        {subtitle ? (
          <span className="mt-0.5 block text-[0.7em] font-normal text-ink-2">{subtitle}</span>
        ) : null}
      </caption>

      <tbody className="[&>tr+tr>*]:border-t [&>tr+tr>*]:border-rule-hair">
        {image ? (
          <tr>
            <td className="infobox-image p-[0.3em] text-center" colSpan={2}>
              {image}
            </td>
          </tr>
        ) : null}

        {rows.map((row, index) => (
          <InfoboxRowCells
            key={`${row.kind}-${index}`}
            row={row}
            sourceId={`${sourceId}.${index}`}
          />
        ))}
      </tbody>
    </table>
  );
}

function InfoboxRowCells({ row, sourceId }: { row: InfoboxRow; sourceId: string }) {
  switch (row.kind) {
    case "header":
      return (
        <tr>
          <th
            className="infobox-header bg-inset px-[0.5em] py-[0.25em] text-center align-top font-semibold text-ink"
            colSpan={2}
          >
            <MarkdownInline content={row.value} sourceId={sourceId} />
          </th>
        </tr>
      );

    case "row":
      return (
        <tr>
          <th
            scope="row"
            className="infobox-label w-1/3 px-[0.5em] py-[0.25em] text-left align-top font-semibold text-ink-2"
          >
            <MarkdownInline content={row.label} sourceId={`${sourceId}.label`} />
          </th>
          <td className="infobox-data px-[0.5em] py-[0.25em] align-top">
            <MarkdownInline content={row.value} sourceId={sourceId} />
          </td>
        </tr>
      );

    case "full":
      return (
        <tr>
          <td className="infobox-full-data px-[0.5em] py-[0.25em] text-center align-top" colSpan={2}>
            <MarkdownInline content={row.value} sourceId={sourceId} />
          </td>
        </tr>
      );

    default: {
      // The union is closed, so this is unreachable — but a future `kind` from
      // the backend must not blank the whole infobox.
      const unknown: never = row;
      void unknown;
      return null;
    }
  }
}
