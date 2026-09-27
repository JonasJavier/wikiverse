import { ArrowDown, ArrowUp, Plus, Quote, Trash2 } from "lucide-react";

import {
  auditIsClean,
  auditReferences,
  LIMITS,
  newReferenceDraft,
  REF_KEY_PATTERN,
  referenceMarker,
  type ReferenceDraft,
} from "@/api/editor";
import { Input, Label, Textarea } from "@/components/ui/Field";
import { cn } from "@/lib/utils";

const ICON_BUTTON =
  "inline-flex size-7 shrink-0 cursor-pointer items-center justify-center rounded-chrome " +
  "border border-rule bg-page text-ink-2 transition-colors duration-100 " +
  "hover:bg-panel hover:text-ink disabled:cursor-not-allowed disabled:opacity-40";

const TEXT_BUTTON =
  "inline-flex h-7 cursor-pointer items-center gap-1 rounded-chrome border border-rule " +
  "bg-page px-2 text-ui text-ink transition-colors duration-100 hover:bg-panel " +
  "disabled:cursor-not-allowed disabled:opacity-40";

interface ReferenceEditorProps {
  value: ReferenceDraft[];
  onChange: (next: ReferenceDraft[]) => void;
  /** The body, so the audit can tell cited from uncited. */
  content: string;
  /** Writes `[^key]` at the caret in the body textarea. */
  onInsertMarker: (key: string) => void;
}

/**
 * The citation apparatus.
 *
 * Field names are the model's, verbatim (DECISIONS §11): `key`, `title`, `url`,
 * `authors`, `publisher`, `published_on`, `accessed_on`, `identifier`, `quote`.
 * Two of those labels matter enough to be spelled out here:
 *
 * - `published_on` is **free text** — "1903", "March 2019", "n.d." Real sources
 *   are irregular, and a date picker here would force an author to invent a day
 *   that the source does not have.
 * - `identifier` is **one field** for all three schemes, labelled
 *   "ISBN / DOI / arXiv". The renderer prefix-sniffs it to print `doi:`, `ISBN`
 *   or `arXiv:`. Three separate columns were the thing §11 removed.
 *
 * The insert button writes **`[^key]`**. `[ref:key]` does not exist anywhere in
 * this system and nothing renders it.
 */
export function ReferenceEditor({
  value,
  onChange,
  content,
  onInsertMarker,
}: ReferenceEditorProps) {
  const audit = auditReferences(value, content);
  const clean = auditIsClean(audit);

  function patch(index: number, partial: Partial<ReferenceDraft>) {
    onChange(value.map((ref, i) => (i === index ? { ...ref, ...partial } : ref)));
  }

  function move(index: number, delta: -1 | 1) {
    const target = index + delta;
    if (target < 0 || target >= value.length) return;
    const next = [...value];
    [next[index], next[target]] = [next[target], next[index]];
    onChange(next);
  }

  return (
    <details className="rounded-chrome border border-rule bg-panel">
      <summary className="cursor-pointer px-3 py-2 text-ui font-medium text-ink">
        References{" "}
        <span className="font-normal text-ink-2">
          {value.length === 0 ? "— none" : `— ${value.length}`}
        </span>
        {value.length > 0 && !clean && (
          <span className="ml-1 font-normal text-warn">· needs attention</span>
        )}
      </summary>

      <div className="border-t border-rule-hair px-3 py-3">
        {value.length === 0 ? (
          <p className="text-ui text-ink-2">
            No references yet. Add one, then cite it in the body with{" "}
            <code className="font-mono">[^key]</code>.
          </p>
        ) : (
          <ol className="space-y-3">
            {value.map((reference, index) => {
              const key = reference.key.trim();
              const keyValid = key !== "" && REF_KEY_PATTERN.test(key);
              const name = key || `reference ${index + 1}`;

              return (
                <li
                  key={reference.uid}
                  className="rounded-chrome border border-rule-hair bg-page p-2.5"
                >
                  <div className="flex items-start gap-2">
                    <div className="min-w-0 flex-1 space-y-2">
                      <div className="grid gap-2 sm:grid-cols-[13rem_1fr]">
                        <div>
                          <Label
                            htmlFor={`ref-key-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Key
                          </Label>
                          <Input
                            id={`ref-key-${reference.uid}`}
                            value={reference.key}
                            onChange={(event) =>
                              patch(index, { key: event.target.value })
                            }
                            maxLength={LIMITS.refKey}
                            spellCheck={false}
                            aria-invalid={key !== "" && !keyValid}
                            aria-describedby={`ref-key-hint-${reference.uid}`}
                            placeholder="curie1903"
                            className="font-mono text-ui"
                          />
                          <p
                            id={`ref-key-hint-${reference.uid}`}
                            className={cn(
                              "mt-1 text-2xs",
                              key !== "" && !keyValid
                                ? "text-danger"
                                : "text-ink-3",
                            )}
                          >
                            Letters, digits, <code className="font-mono">-</code>{" "}
                            and <code className="font-mono">_</code> only.
                          </p>
                        </div>

                        <div>
                          <Label
                            htmlFor={`ref-title-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Title
                          </Label>
                          <Input
                            id={`ref-title-${reference.uid}`}
                            value={reference.title}
                            onChange={(event) =>
                              patch(index, { title: event.target.value })
                            }
                            maxLength={LIMITS.refTitle}
                            placeholder="Recherches sur les substances radioactives"
                          />
                        </div>
                      </div>

                      <div>
                        <Label
                          htmlFor={`ref-url-${reference.uid}`}
                          className="text-2xs text-ink-2"
                        >
                          URL
                        </Label>
                        <Input
                          id={`ref-url-${reference.uid}`}
                          type="url"
                          inputMode="url"
                          value={reference.url}
                          onChange={(event) =>
                            patch(index, { url: event.target.value })
                          }
                          maxLength={LIMITS.refUrl}
                          spellCheck={false}
                          placeholder="https://example.org/paper"
                        />
                      </div>

                      <div className="grid gap-2 sm:grid-cols-2">
                        <div>
                          <Label
                            htmlFor={`ref-authors-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Authors
                          </Label>
                          <Input
                            id={`ref-authors-${reference.uid}`}
                            value={reference.authors}
                            onChange={(event) =>
                              patch(index, { authors: event.target.value })
                            }
                            maxLength={LIMITS.refAuthors}
                            placeholder="Curie, Marie"
                          />
                        </div>
                        <div>
                          <Label
                            htmlFor={`ref-publisher-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Publisher
                          </Label>
                          <Input
                            id={`ref-publisher-${reference.uid}`}
                            value={reference.publisher}
                            onChange={(event) =>
                              patch(index, { publisher: event.target.value })
                            }
                            maxLength={LIMITS.refPublisher}
                            placeholder="Gauthier-Villars"
                          />
                        </div>
                      </div>

                      <div className="grid gap-2 sm:grid-cols-3">
                        <div>
                          <Label
                            htmlFor={`ref-published-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Date published (free text)
                          </Label>
                          <Input
                            id={`ref-published-${reference.uid}`}
                            value={reference.published_on}
                            onChange={(event) =>
                              patch(index, { published_on: event.target.value })
                            }
                            maxLength={LIMITS.refPublishedOn}
                            placeholder="1903"
                          />
                        </div>
                        <div>
                          <Label
                            htmlFor={`ref-accessed-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Date accessed
                          </Label>
                          <Input
                            id={`ref-accessed-${reference.uid}`}
                            type="date"
                            value={reference.accessed_on}
                            onChange={(event) =>
                              patch(index, { accessed_on: event.target.value })
                            }
                          />
                        </div>
                        <div>
                          <Label
                            htmlFor={`ref-identifier-${reference.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            ISBN / DOI / arXiv
                          </Label>
                          <Input
                            id={`ref-identifier-${reference.uid}`}
                            value={reference.identifier}
                            onChange={(event) =>
                              patch(index, { identifier: event.target.value })
                            }
                            maxLength={LIMITS.refIdentifier}
                            spellCheck={false}
                            placeholder="doi:10.1038/nature12373"
                          />
                        </div>
                      </div>

                      <div>
                        <Label
                          htmlFor={`ref-quote-${reference.uid}`}
                          className="text-2xs text-ink-2"
                        >
                          Quote
                        </Label>
                        <Textarea
                          id={`ref-quote-${reference.uid}`}
                          value={reference.quote}
                          onChange={(event) =>
                            patch(index, { quote: event.target.value })
                          }
                          maxLength={LIMITS.refQuote}
                          rows={2}
                          placeholder="The passage that supports the claim. Optional."
                        />
                      </div>

                      <button
                        type="button"
                        className={TEXT_BUTTON}
                        disabled={!keyValid}
                        onClick={() => onInsertMarker(key)}
                        aria-label={`Insert the citation marker ${referenceMarker(name)} into the body`}
                      >
                        <Quote aria-hidden="true" className="size-3.5" />
                        Insert{" "}
                        <code className="font-mono">
                          {referenceMarker(key || "key")}
                        </code>
                      </button>
                    </div>

                    <div className="flex shrink-0 flex-col gap-1 pt-5">
                      <button
                        type="button"
                        className={ICON_BUTTON}
                        disabled={index === 0}
                        onClick={() => move(index, -1)}
                        aria-label={`Move ${name} up`}
                      >
                        <ArrowUp aria-hidden="true" className="size-3.5" />
                      </button>
                      <button
                        type="button"
                        className={ICON_BUTTON}
                        disabled={index === value.length - 1}
                        onClick={() => move(index, 1)}
                        aria-label={`Move ${name} down`}
                      >
                        <ArrowDown aria-hidden="true" className="size-3.5" />
                      </button>
                      <button
                        type="button"
                        className={cn(ICON_BUTTON, "hover:text-danger")}
                        onClick={() =>
                          onChange(value.filter((_, i) => i !== index))
                        }
                        aria-label={`Remove ${name}`}
                      >
                        <Trash2 aria-hidden="true" className="size-3.5" />
                      </button>
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
        )}

        {/* The validation line. Not a live region: it recomputes on every
            keystroke, and announcing that would be unusable. It is visible,
            beside the thing it is about, which is where a form error belongs. */}
        {!clean && (
          <ul className="mt-3 space-y-1 border-t border-rule-hair pt-3 text-2xs text-warn">
            {audit.malformed.length > 0 && (
              <li>
                Not a valid key: {audit.malformed.join(", ")}. Use letters,
                digits, hyphens and underscores.
              </li>
            )}
            {audit.duplicate.length > 0 && (
              <li>
                Used more than once: {audit.duplicate.join(", ")}. A key must be
                unique within the article.
              </li>
            )}
            {audit.untitled.length > 0 && (
              <li>No title yet: {audit.untitled.join(", ")}.</li>
            )}
            {audit.unresolved.length > 0 && (
              <li>
                Cited in the body but not defined here:{" "}
                {audit.unresolved.map((key) => referenceMarker(key)).join(", ")}.
              </li>
            )}
            {audit.uncited.length > 0 && (
              <li>
                Defined but never cited: {audit.uncited.join(", ")}. Add{" "}
                <code className="font-mono">
                  {referenceMarker(audit.uncited[0])}
                </code>{" "}
                where the claim is made.
              </li>
            )}
          </ul>
        )}

        <div className="mt-2">
          <button
            type="button"
            className={TEXT_BUTTON}
            onClick={() => onChange([...value, newReferenceDraft()])}
          >
            <Plus aria-hidden="true" className="size-3.5" />
            Add reference
          </button>
        </div>
      </div>
    </details>
  );
}
