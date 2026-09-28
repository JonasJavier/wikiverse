import type { OnThisDayRow } from "@/api/mainpage";
import type { LinkResolver } from "@/components/article/markdownUtils";
import { WikiText } from "./WikiText";

interface OnThisDayProps {
  entries: OnThisDayRow[];
  /** The shared existence oracle, so an event's wikilink can go red. */
  resolve?: LinkResolver;
}

interface DayGroup {
  key: string;
  /** `"26 September"`, or `""` for entries carrying no date at all. */
  heading: string;
  /** Sort distance from today, in days, so today's group leads. */
  distance: number;
  entries: OnThisDayRow[];
}

const DAY_MONTH = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
});

/**
 * The year column is drawn here, so a body that also opens with its year —
 * `**1859** — On the Origin…`, as editors naturally write it — would print it
 * twice. Only a leading year equal to the entry's own is dropped.
 */
function withoutLeadingYear(body: string, year: number | null): string {
  if (year === null) return body;
  const pattern = new RegExp(`^\\s*(\\*\\*|__)?${year}\\1?\\s*[—–-]\\s*`);
  return body.replace(pattern, "");
}

/** A leap-safe reference year, so 29 February formats correctly. */
const REFERENCE_YEAR = 2024;

function headingFor(month: number, day: number): string {
  return DAY_MONTH.format(new Date(REFERENCE_YEAR, month - 1, day));
}

/** Days from today to `month`/`day`, wrapping at the year boundary. */
function distanceFromToday(month: number, day: number): number {
  const now = new Date();
  const today = Date.UTC(REFERENCE_YEAR, now.getMonth(), now.getDate());
  const target = Date.UTC(REFERENCE_YEAR, month - 1, day);
  const dayMs = 86_400_000;
  const delta = Math.round((target - today) / dayMs);
  return delta < 0 ? delta + 366 : delta;
}

function group(entries: OnThisDayRow[]): DayGroup[] {
  const groups = new Map<string, DayGroup>();

  for (const entry of entries) {
    const { month, day } = entry;
    const key = month !== null && day !== null ? `${month}-${day}` : "undated";
    let bucket = groups.get(key);
    if (!bucket) {
      bucket =
        month !== null && day !== null
          ? {
              key,
              heading: headingFor(month, day),
              distance: distanceFromToday(month, day),
              entries: [],
            }
          : {
              key,
              heading: "",
              // Undated events sort last, after every real date in the year.
              distance: 400,
              entries: [],
            };
      groups.set(key, bucket);
    }
    bucket.entries.push(entry);
  }

  const ordered = [...groups.values()].sort((a, b) => a.distance - b.distance);
  for (const bucket of ordered) {
    bucket.entries.sort((a, b) => (a.year ?? 0) - (b.year ?? 0));
  }
  return ordered;
}

/**
 * On this day — events grouped under their date, with the group nearest to
 * today first, and the years in tabular figures.
 *
 * Tabular years are the detail that makes the list scan: every year occupies
 * the same width, so the eye reads a column of dates rather than ragged bold
 * text. `tabular-nums` is already the app-wide default (§6.3); it is restated
 * on the year because the surrounding serif line is running prose.
 */
export function OnThisDay({ entries, resolve }: OnThisDayProps) {
  if (entries.length === 0) {
    return (
      <p className="text-ui text-ink-2">
        No anniversaries have been recorded yet. They are editorial blocks,
        added through the admin.
      </p>
    );
  }

  return (
    <div className="space-y-2.5">
      {group(entries).map((bucket) => (
        <div key={bucket.key}>
          {bucket.heading && (
            <h3 className="font-serif text-[1.0625rem] font-normal text-ink">
              {bucket.heading}
            </h3>
          )}
          <ul className="mt-1 list-disc space-y-1.5 pl-5 font-serif text-read leading-[1.55] text-ink marker:text-ink-3">
            {bucket.entries.map((entry, index) => (
              <li key={`${bucket.key}-${entry.year ?? "x"}-${index}`}>
                {entry.year !== null && (
                  <>
                    <b className="font-semibold tabular-nums">{entry.year}</b>
                    {" — "}
                  </>
                )}
                <WikiText resolve={resolve}>
                  {withoutLeadingYear(entry.body, entry.year)}
                </WikiText>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
