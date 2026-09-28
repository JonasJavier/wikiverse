import { ArrowDown, ArrowUp, Plus, Trash2 } from "lucide-react";

import {
  INFOBOX_ROW_KINDS,
  LIMITS,
  newInfoboxRow,
  type InfoboxDraft,
  type InfoboxRowDraft,
  type InfoboxRowKind,
} from "@/api/editor";
import { Input, Label, Textarea } from "@/components/ui/Field";
import { cn } from "@/lib/utils";

const SELECT_CLASS =
  "h-9 w-full rounded-chrome border border-rule bg-page px-2 text-base text-ink " +
  "transition-colors duration-100";

const ICON_BUTTON =
  "inline-flex size-7 shrink-0 cursor-pointer items-center justify-center rounded-chrome " +
  "border border-rule bg-page text-ink-2 transition-colors duration-100 " +
  "hover:bg-panel hover:text-ink disabled:cursor-not-allowed disabled:opacity-40";

interface InfoboxEditorProps {
  value: InfoboxDraft;
  onChange: (next: InfoboxDraft) => void;
  /** Placeholder for the box title: an empty title defaults to this (§1). */
  articleTitle: string;
}

/**
 * The structured infobox, edited as a list of rows.
 *
 * It emits the DECISIONS §1 schema and nothing else — see `toInfobox()` in
 * `api/editor.ts`, which is the single place the wire shape is built. Two
 * consequences are visible in this form:
 *
 * - **There is no image field here.** The lead image is six `Article` columns
 *   (`lead_image_url` and friends), never an infobox key, so it is edited in its
 *   own section of the page. An `infobox.image` would be silently dropped by the
 *   serialiser, which is the worst kind of bug: the author sees it saved.
 * - **Reordering is ↑/↓ buttons, not drag.** Drag-and-drop is unusable with a
 *   keyboard and awkward with a screen reader, and this is a form, not a canvas
 *   (design-ui §5.6).
 *
 * Each row keeps a `uid`, so the React key survives a move and focus therefore
 * travels with the row the author is moving rather than staying on whatever
 * lands at that index.
 */
export function InfoboxEditor({
  value,
  onChange,
  articleTitle,
}: InfoboxEditorProps) {
  const { rows } = value;

  function patch(partial: Partial<InfoboxDraft>) {
    onChange({ ...value, ...partial });
  }

  function patchRow(index: number, partial: Partial<InfoboxRowDraft>) {
    patch({
      rows: rows.map((row, i) => (i === index ? { ...row, ...partial } : row)),
    });
  }

  function addRow(kind: InfoboxRowKind) {
    patch({ rows: [...rows, newInfoboxRow(kind)] });
  }

  function removeRow(index: number) {
    patch({ rows: rows.filter((_, i) => i !== index) });
  }

  function move(index: number, delta: -1 | 1) {
    const target = index + delta;
    if (target < 0 || target >= rows.length) return;
    const next = [...rows];
    [next[index], next[target]] = [next[target], next[index]];
    patch({ rows: next });
  }

  return (
    <details className="rounded-chrome border border-rule bg-panel">
      <summary className="cursor-pointer px-3 py-2 text-ui font-medium text-ink">
        Infobox{" "}
        <span className="font-normal text-ink-2">
          {rows.length === 0
            ? "— none"
            : `— ${rows.length} ${rows.length === 1 ? "row" : "rows"}`}
        </span>
      </summary>

      <div className="border-t border-rule-hair px-3 py-3">
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <Label htmlFor="infobox-title">Box title</Label>
            <Input
              id="infobox-title"
              value={value.title}
              onChange={(event) => patch({ title: event.target.value })}
              maxLength={LIMITS.infoboxTitle}
              placeholder={articleTitle || "Defaults to the article title"}
            />
          </div>
          <div>
            <Label htmlFor="infobox-subtitle">Subtitle</Label>
            <Input
              id="infobox-subtitle"
              value={value.subtitle}
              onChange={(event) => patch({ subtitle: event.target.value })}
              maxLength={LIMITS.infoboxTitle}
              placeholder="Optional, e.g. Physicist and chemist"
            />
          </div>
        </div>

        <hr className="my-3 border-0 border-t border-rule-hair" />

        {rows.length === 0 ? (
          <p className="text-ui text-ink-2">
            No rows yet. An infobox is a short table of facts — dates, places,
            figures — beside the lead.
          </p>
        ) : (
          <ol className="space-y-3">
            {rows.map((row, index) => (
              <li key={row.uid} className="rounded-chrome border border-rule-hair bg-page p-2.5">
                <div className="flex items-start gap-2">
                  <div className="min-w-0 flex-1 space-y-2">
                    <div className="grid gap-2 sm:grid-cols-[11rem_1fr]">
                      <div>
                        <Label
                          htmlFor={`row-kind-${row.uid}`}
                          className="text-2xs text-ink-2"
                        >
                          Kind
                        </Label>
                        <select
                          id={`row-kind-${row.uid}`}
                          value={row.kind}
                          onChange={(event) =>
                            patchRow(index, {
                              kind: event.target.value as InfoboxRowKind,
                            })
                          }
                          className={SELECT_CLASS}
                        >
                          {INFOBOX_ROW_KINDS.map((kind) => (
                            <option key={kind.value} value={kind.value}>
                              {kind.label}
                            </option>
                          ))}
                        </select>
                      </div>

                      {row.kind === "row" && (
                        <div>
                          <Label
                            htmlFor={`row-label-${row.uid}`}
                            className="text-2xs text-ink-2"
                          >
                            Label
                          </Label>
                          <Input
                            id={`row-label-${row.uid}`}
                            value={row.label}
                            onChange={(event) =>
                              patchRow(index, { label: event.target.value })
                            }
                            maxLength={LIMITS.infoboxLabel}
                            placeholder="Born"
                          />
                        </div>
                      )}
                    </div>

                    <div>
                      <Label
                        htmlFor={`row-value-${row.uid}`}
                        className="text-2xs text-ink-2"
                      >
                        Value
                      </Label>
                      {row.kind === "full" ? (
                        <Textarea
                          id={`row-value-${row.uid}`}
                          value={row.value}
                          onChange={(event) =>
                            patchRow(index, { value: event.target.value })
                          }
                          rows={2}
                          placeholder="A full-width note, with no label beside it"
                        />
                      ) : (
                        <Input
                          id={`row-value-${row.uid}`}
                          value={row.value}
                          onChange={(event) =>
                            patchRow(index, { value: event.target.value })
                          }
                          placeholder={
                            row.kind === "header"
                              ? "Career"
                              : "7 November 1867, [[Warsaw]]"
                          }
                        />
                      )}
                    </div>
                  </div>

                  <div className="flex shrink-0 flex-col gap-1 pt-5">
                    <button
                      type="button"
                      className={ICON_BUTTON}
                      disabled={index === 0}
                      onClick={() => move(index, -1)}
                      aria-label={`Move row ${index + 1} up`}
                    >
                      <ArrowUp aria-hidden="true" className="size-3.5" />
                    </button>
                    <button
                      type="button"
                      className={ICON_BUTTON}
                      disabled={index === rows.length - 1}
                      onClick={() => move(index, 1)}
                      aria-label={`Move row ${index + 1} down`}
                    >
                      <ArrowDown aria-hidden="true" className="size-3.5" />
                    </button>
                    <button
                      type="button"
                      className={cn(ICON_BUTTON, "hover:text-danger")}
                      onClick={() => removeRow(index)}
                      aria-label={`Remove row ${index + 1}`}
                    >
                      <Trash2 aria-hidden="true" className="size-3.5" />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ol>
        )}

        <p className="mt-3 text-2xs text-ink-2">
          A value is plain text. It may contain{" "}
          <code className="font-mono">[[Wikilinks]]</code>,{" "}
          <code className="font-mono">*emphasis*</code> and{" "}
          <code className="font-mono">[^key]</code> citation markers, which the
          article renders.
        </p>

        <div className="mt-2 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => addRow("row")}
            className="inline-flex h-7 cursor-pointer items-center gap-1 rounded-chrome border border-rule bg-page px-2 text-ui text-ink transition-colors duration-100 hover:bg-panel"
          >
            <Plus aria-hidden="true" className="size-3.5" />
            Add row
          </button>
          <button
            type="button"
            onClick={() => addRow("header")}
            className="inline-flex h-7 cursor-pointer items-center gap-1 rounded-chrome border border-rule bg-page px-2 text-ui text-ink transition-colors duration-100 hover:bg-panel"
          >
            <Plus aria-hidden="true" className="size-3.5" />
            Add section header
          </button>
          <button
            type="button"
            onClick={() => addRow("full")}
            className="inline-flex h-7 cursor-pointer items-center gap-1 rounded-chrome border border-rule bg-page px-2 text-ui text-ink transition-colors duration-100 hover:bg-panel"
          >
            <Plus aria-hidden="true" className="size-3.5" />
            Add full-width row
          </button>
        </div>
      </div>
    </details>
  );
}
