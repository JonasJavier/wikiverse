import { WikiLink } from "./WikiLink";

export interface SeeAlsoEntry {
  /** An exact article title from the taxonomy. */
  title: string;
  /** The one-clause gloss after the em dash. Optional. */
  gloss?: string;
}

export interface SeeAlsoProps {
  /** Titles, or titles with glosses. Rendered from data, never hand-written. */
  entries: ReadonlyArray<string | SeeAlsoEntry>;
  id?: string;
  heading?: string;
}

/**
 * `## See also` — plural, and rendered from `see_also` data rather than from a
 * hand-written list in the body (DECISIONS §19), so the section can never drift
 * out of MOS order or get duplicated by an author.
 *
 * Entries pointing at unwritten titles are KEPT and rendered as red links. MOS
 * says a See-also list should contain only existing articles, and Wikipedia
 * enforces that as a review convention; here the corpus is 63 of 120 planned
 * articles, and DECISIONS §19 settles it explicitly: keep them, show them red.
 * Hiding them would hide the shape of the work still to do.
 */
export function SeeAlso({ entries, id = "see-also", heading = "See also" }: SeeAlsoProps) {
  if (entries.length === 0) return null;

  const rows = entries.map((entry) => (typeof entry === "string" ? { title: entry } : entry));

  return (
    <>
      <h2 id={id}>{heading}</h2>
      <ul className="seealso">
        {rows.map((row) => (
          <li key={row.title}>
            <WikiLink title={row.title} />
            {row.gloss ? <span className="text-ink-2"> &mdash; {row.gloss}</span> : null}
          </li>
        ))}
      </ul>
    </>
  );
}
