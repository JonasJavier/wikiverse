import type { FormEvent } from "react";

import { SEARCH_SORTS, type SearchFacets } from "@/api/search";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Field";
import type { SearchSort } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Everything the filter row can change, in one patch. */
export type SearchFilterPatch = Partial<SearchFacets & { ordering: SearchSort }>;

/**
 * Only the two fields the control actually reads. Deliberately NOT `Category`:
 * the wire shape of a category (`parent` as a slug string, `article_count`,
 * icons) is none of this component's business, and a structural minimum means
 * the filter row does not have to be edited when that DTO changes.
 */
export interface CategoryOption {
  slug: string;
  name: string;
}

export interface SearchFiltersProps {
  /** The facets as they appear in the URL — the single source of truth. */
  values: SearchFacets;
  ordering: SearchSort;
  categories: readonly CategoryOption[] | undefined;
  /** Merge a patch into the URL. The caller resets `page` to 1. */
  onChange: (patch: SearchFilterPatch) => void;
  className?: string;
}

const CONTROL =
  "h-8 rounded-chrome border border-rule bg-page px-2 text-ui text-ink " +
  "transition-colors duration-100";

/**
 * Sort and category sit in the open row, because they are the two a reader
 * reaches for. Author and the date range live in a `<details>` — the advanced
 * pane is a disclosure on this page rather than a second route (§5.7b), which
 * keeps the feature discoverable without another URL to maintain.
 *
 * Everything here writes to the URL and nothing to `useState`. That is what
 * makes a filtered result set shareable, the back button work, and page 2
 * crawlable. The only local state is the browser's own: the text and date
 * inputs are uncontrolled, keyed on their URL value so an external change
 * (a removed chip, a back navigation) re-seeds them, and read out of the form
 * on submit. A facet that fired on every keystroke would be one request per
 * character.
 *
 * Active facets are then repeated as removable chips, so the difference
 * between "no results" and "no results under four filters" is visible.
 */
export function SearchFilters({
  values,
  ordering,
  categories,
  onChange,
  className,
}: SearchFiltersProps) {
  const chips = activeChips(values, categories);
  const hasAdvanced = Boolean(
    values.author || values.created_after || values.created_before,
  );

  function handleAdvanced(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    onChange({
      author: String(form.get("author") ?? "").trim(),
      created_after: String(form.get("created_after") ?? ""),
      created_before: String(form.get("created_before") ?? ""),
    });
  }

  return (
    <div className={cn("border-y border-rule-hair py-2", className)}>
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-ui">
        <label className="flex items-center gap-1.5 text-ink-2">
          Sort
          <select
            value={ordering}
            onChange={(e) => onChange({ ordering: e.target.value as SearchSort })}
            className={CONTROL}
          >
            {SEARCH_SORTS.map((sort) => (
              <option key={sort.value} value={sort.value}>
                {sort.label}
              </option>
            ))}
          </select>
        </label>

        <label className="flex items-center gap-1.5 text-ink-2">
          Category
          <select
            value={values.category}
            onChange={(e) => onChange({ category: e.target.value })}
            className={CONTROL}
          >
            <option value="">All categories</option>
            {categories?.map((category) => (
              <option key={category.slug} value={category.slug}>
                {category.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      <details className="mt-2 text-ui" open={hasAdvanced}>
        <summary className="cursor-pointer list-none rounded-chrome py-0.5 font-medium text-link hover:text-link-hover hover:underline [&::-webkit-details-marker]:hidden">
          Advanced
        </summary>

        <form
          onSubmit={handleAdvanced}
          className="mt-2 flex flex-wrap items-end gap-x-4 gap-y-3"
        >
          <div>
            <label htmlFor="search-author" className="mb-1 block text-ink-2">
              Contributor
            </label>
            <Input
              id="search-author"
              name="author"
              key={`author:${values.author}`}
              defaultValue={values.author}
              placeholder="username"
              className="h-8 w-40 text-ui"
            />
          </div>

          <div>
            <label htmlFor="search-created-after" className="mb-1 block text-ink-2">
              Created after
            </label>
            <Input
              id="search-created-after"
              name="created_after"
              type="date"
              key={`after:${values.created_after}`}
              defaultValue={values.created_after}
              className="h-8 w-44 text-ui"
            />
          </div>

          <div>
            <label htmlFor="search-created-before" className="mb-1 block text-ink-2">
              Created before
            </label>
            <Input
              id="search-created-before"
              name="created_before"
              type="date"
              key={`before:${values.created_before}`}
              defaultValue={values.created_before}
              className="h-8 w-44 text-ui"
            />
          </div>

          <Button type="submit" variant="secondary">
            Apply
          </Button>
        </form>
      </details>

      {chips.length > 0 && (
        <ul className="mt-2 flex flex-wrap items-center gap-1.5">
          {chips.map((chip) => (
            <li key={chip.key}>
              <span className="inline-flex items-center rounded-chrome border border-rule bg-panel py-0.5 pl-2 text-ui text-ink">
                <span className="text-ink-2">{chip.label}:&nbsp;</span>
                {chip.value}
                <button
                  type="button"
                  onClick={() => onChange(chip.clear)}
                  aria-label={`Remove the ${chip.label.toLowerCase()} filter`}
                  className="cursor-pointer px-1.5 text-ink-2 hover:text-ink"
                >
                  <span aria-hidden="true">×</span>
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

interface Chip {
  key: keyof SearchFacets;
  label: string;
  value: string;
  /** The patch that removes this one facet, written out rather than keyed. */
  clear: SearchFilterPatch;
}

/**
 * A category chip shows the category's NAME, not its slug — the slug is a URL
 * detail and a reader who filtered by "Life sciences" should not have to read
 * back "life-sciences". It falls back to the slug while the taxonomy is still
 * loading, so the chip never renders blank.
 */
function activeChips(
  values: SearchFacets,
  categories: readonly CategoryOption[] | undefined,
): Chip[] {
  const chips: Chip[] = [];

  if (values.category) {
    const match = categories?.find((c) => c.slug === values.category);
    chips.push({
      key: "category",
      label: "Category",
      value: match?.name ?? values.category,
      clear: { category: "" },
    });
  }
  if (values.author) {
    chips.push({
      key: "author",
      label: "Contributor",
      value: values.author,
      clear: { author: "" },
    });
  }
  if (values.created_after) {
    chips.push({
      key: "created_after",
      label: "After",
      value: values.created_after,
      clear: { created_after: "" },
    });
  }
  if (values.created_before) {
    chips.push({
      key: "created_before",
      label: "Before",
      value: values.created_before,
      clear: { created_before: "" },
    });
  }

  return chips;
}
