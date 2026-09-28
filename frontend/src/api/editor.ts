/**
 * The editor's data layer: the write payload, the draft store, and the
 * translation between the API's shapes and the shapes a form can hold.
 *
 * Why the form does not hold `Infobox` and `Reference` directly:
 *
 *  - `InfoboxRow` is a discriminated union whose *key set* changes with `kind`
 *    (`header` carries `value` and NOT `label`, DECISIONS §1). A form that
 *    edited that object in place would have to delete and recreate keys on
 *    every change of a `<select>`, and would lose a typed label the moment the
 *    author previewed a row as a header. So the form holds a flat draft row
 *    with every field present, and `toInfobox()` is the single place that emits
 *    the exact §1 schema. There is precisely one `switch` over `kind`, here.
 *  - Reordering with ↑/↓ buttons needs a React key that survives a move, and
 *    neither a row nor a reference has an id before it is saved. Draft rows
 *    therefore carry a `uid`, stripped on the way out.
 *
 * Everything this module emits is checked against DECISIONS §1 (infobox),
 * §11 (references, and the `[^key]` marker) and §19 (the corpus contract the
 * backend serialisers mirror).
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

import { articleKeys } from "@/api/articles";
import { api } from "@/lib/api";
import type {
  Article,
  ArticleInput,
  Infobox,
  InfoboxRow,
  PageType,
  Reference,
} from "@/lib/types";

/* =====================================================================
   Limits — every one of them is the backend column's own `max_length`
   =====================================================================
   They are mirrored here so the form truncates where the database would
   otherwise 400, and so a reader never loses a paragraph to a limit that
   was never shown to them.
   ===================================================================== */

export const LIMITS = {
  title: 200,
  /** `Article.short_description` is 120; the corpus style guide asks for ≤ 90. */
  shortDescription: 120,
  shortDescriptionIdeal: 90,
  summary: 300,
  /** `Revision.comment`. */
  comment: 255,
  refKey: 60,
  refTitle: 300,
  refUrl: 600,
  refAuthors: 300,
  refPublisher: 200,
  refPublishedOn: 40,
  refIdentifier: 120,
  refQuote: 300,
  infoboxTitle: 200,
  infoboxLabel: 120,
} as const;

/**
 * `Reference.key` is a Django `SlugField`, so the server accepts exactly this
 * alphabet. Validating it in the form is what stops a `[^key]` marker that can
 * never resolve from being written into the body.
 */
export const REF_KEY_PATTERN = /^[a-zA-Z0-9_-]+$/;

/**
 * The in-text citation marker. `[^key]` everywhere — corpus, validator,
 * renderer and this editor's insert button (DECISIONS §11). `[ref:key]` does
 * not exist and nothing renders it.
 */
export function referenceMarker(key: string): string {
  return `[^${key}]`;
}

/** Global, so every call site must reset `lastIndex` or use `matchAll`. */
const MARKER_RE = /\[\^([a-zA-Z0-9_-]+)\]/g;

/** Every `[^key]` cited in a body, in the order they first appear. */
export function citedKeys(content: string): string[] {
  const seen = new Set<string>();
  for (const match of content.matchAll(MARKER_RE)) {
    seen.add(match[1]);
  }
  return [...seen];
}

/* =====================================================================
   The infobox draft (DECISIONS §1)
   ===================================================================== */

export type InfoboxRowKind = InfoboxRow["kind"];

export const INFOBOX_ROW_KINDS: { value: InfoboxRowKind; label: string }[] = [
  { value: "row", label: "Label and value" },
  { value: "header", label: "Section header" },
  { value: "full", label: "Full width" },
];

/**
 * A flat, always-complete row. `label` is kept even while `kind` is `header`
 * or `full` so toggling the kind back does not silently discard typing; it is
 * dropped on the way out, because a `header` row carrying `label` is not the
 * §1 schema.
 */
export interface InfoboxRowDraft {
  uid: string;
  kind: InfoboxRowKind;
  label: string;
  value: string;
}

export interface InfoboxDraft {
  /** Blank means "default to the article title" — the key is then omitted. */
  title: string;
  subtitle: string;
  rows: InfoboxRowDraft[];
}

export function emptyInfoboxDraft(): InfoboxDraft {
  return { title: "", subtitle: "", rows: [] };
}

export function newInfoboxRow(kind: InfoboxRowKind = "row"): InfoboxRowDraft {
  return { uid: uid(), kind, label: "", value: "" };
}

/** The API shape → the form shape. */
export function infoboxToDraft(infobox: Infobox | null | undefined): InfoboxDraft {
  if (!infobox) return emptyInfoboxDraft();
  return {
    title: infobox.title ?? "",
    subtitle: infobox.subtitle ?? "",
    rows: (infobox.rows ?? []).map((row) => ({
      uid: uid(),
      kind: row.kind,
      label: row.kind === "row" ? row.label : "",
      value: row.value,
    })),
  };
}

/**
 * The form shape → EXACTLY the DECISIONS §1 schema, and nothing else.
 *
 * - `value` is always a plain string. No objects, no arrays.
 * - A `header` row emits `{kind, value}`; it never emits `label`.
 * - A `full` row emits `{kind, value}`.
 * - There is no `image` key, ever. The lead image lives on `Article` columns.
 * - Rows with an empty `value` are dropped: a blank row renders as a blank
 *   line in the box, which is never what was meant.
 * - An infobox with no rows serialises as `null`, not `{}`, so "remove the
 *   infobox" is expressible.
 */
export function toInfobox(draft: InfoboxDraft): Infobox | null {
  const rows: InfoboxRow[] = [];

  for (const row of draft.rows) {
    const value = row.value.trim();
    if (!value) continue;

    switch (row.kind) {
      case "header":
        rows.push({ kind: "header", value });
        break;
      case "full":
        rows.push({ kind: "full", value });
        break;
      case "row":
        rows.push({ kind: "row", label: row.label.trim(), value });
        break;
    }
  }

  const title = draft.title.trim();
  const subtitle = draft.subtitle.trim();

  if (rows.length === 0 && !title && !subtitle) return null;

  const infobox: Infobox = { rows };
  if (title) infobox.title = title;
  if (subtitle) infobox.subtitle = subtitle;
  return infobox;
}

/* =====================================================================
   The reference draft (DECISIONS §11)
   ===================================================================== */

/**
 * `order` is not in the draft: it is the array index, recomputed on save, so
 * the ↑/↓ buttons cannot leave two references claiming the same position.
 * `accessed_on` is a string here (`""` or `YYYY-MM-DD`) because that is what
 * `<input type="date">` produces; `toReferences` turns `""` into `null`.
 */
export interface ReferenceDraft {
  uid: string;
  key: string;
  title: string;
  url: string;
  authors: string;
  publisher: string;
  published_on: string;
  accessed_on: string;
  identifier: string;
  quote: string;
}

export function newReferenceDraft(): ReferenceDraft {
  return {
    uid: uid(),
    key: "",
    title: "",
    url: "",
    authors: "",
    publisher: "",
    published_on: "",
    accessed_on: "",
    identifier: "",
    quote: "",
  };
}

export function referencesToDrafts(references: Reference[]): ReferenceDraft[] {
  return [...references]
    .sort((a, b) => a.order - b.order)
    .map((reference) => ({
      uid: uid(),
      key: reference.key,
      title: reference.title,
      url: reference.url,
      authors: reference.authors,
      publisher: reference.publisher,
      published_on: reference.published_on,
      accessed_on: reference.accessed_on ?? "",
      identifier: reference.identifier,
      quote: reference.quote,
    }));
}

/** The form shape → the `ReferenceSerializer` field list, in its own order. */
export function toReferences(drafts: ReferenceDraft[]): Reference[] {
  return drafts
    .filter((draft) => draft.key.trim() !== "")
    .map((draft, index) => ({
      key: draft.key.trim(),
      order: index,
      title: draft.title.trim(),
      url: draft.url.trim(),
      authors: draft.authors.trim(),
      publisher: draft.publisher.trim(),
      published_on: draft.published_on.trim(),
      accessed_on: draft.accessed_on.trim() || null,
      identifier: draft.identifier.trim(),
      quote: draft.quote.trim(),
    }));
}

/** What the citation validator found. Empty arrays mean "nothing to say". */
export interface ReferenceAudit {
  /** Defined here but never cited with `[^key]` in the body. */
  uncited: string[];
  /** Cited in the body with no matching reference record. */
  unresolved: string[];
  /** The same `key` used by more than one reference. */
  duplicate: string[];
  /** A `key` the server's `SlugField` would reject. */
  malformed: string[];
  /** A reference with a key but no title. */
  untitled: string[];
}

export function auditReferences(
  drafts: ReferenceDraft[],
  content: string,
): ReferenceAudit {
  const keys = drafts.map((draft) => draft.key.trim()).filter(Boolean);
  const defined = new Set(keys);
  const cited = citedKeys(content);

  const counts = new Map<string, number>();
  for (const key of keys) counts.set(key, (counts.get(key) ?? 0) + 1);

  return {
    uncited: keys.filter((key) => !cited.includes(key)),
    unresolved: cited.filter((key) => !defined.has(key)),
    duplicate: [...counts.entries()].filter(([, n]) => n > 1).map(([key]) => key),
    malformed: keys.filter((key) => !REF_KEY_PATTERN.test(key)),
    untitled: drafts
      .filter((draft) => draft.key.trim() && !draft.title.trim())
      .map((draft) => draft.key.trim()),
  };
}

export function auditIsClean(audit: ReferenceAudit): boolean {
  return (
    audit.uncited.length === 0 &&
    audit.unresolved.length === 0 &&
    audit.duplicate.length === 0 &&
    audit.malformed.length === 0 &&
    audit.untitled.length === 0
  );
}

/* =====================================================================
   The whole form
   ===================================================================== */

export interface EditorForm {
  title: string;
  short_description: string;
  summary: string;
  /** A category SLUG, or `""` for none. */
  category: string;
  content: string;
  page_type: PageType;
  is_stub: boolean;
  infobox: InfoboxDraft;
  references: ReferenceDraft[];
  /** The lead image is six `Article` columns, never an infobox key (§1). */
  lead_image_url: string;
  lead_image_alt: string;
  lead_image_caption: string;
  lead_image_credit: string;
  lead_image_license: string;
  lead_image_source_url: string;
  /** Revision metadata, not article data. */
  comment: string;
  is_minor: boolean;
  is_published: boolean;
  /** Not part of the payload — a separate `POST`/`DELETE …/watch/` call. */
  watch: boolean;
}

/**
 * A fresh form. `watch` defaults on for a new article (design-ui §5.6): an
 * author is by definition interested in what happens to the page they just
 * wrote.
 */
export function emptyForm(title = ""): EditorForm {
  return {
    title,
    short_description: "",
    summary: "",
    category: "",
    content: "",
    page_type: "article",
    is_stub: false,
    infobox: emptyInfoboxDraft(),
    references: [],
    lead_image_url: "",
    lead_image_alt: "",
    lead_image_caption: "",
    lead_image_credit: "",
    lead_image_license: "",
    lead_image_source_url: "",
    comment: "",
    is_minor: false,
    is_published: true,
    watch: true,
  };
}

export function formFromArticle(article: Article): EditorForm {
  return {
    title: article.title,
    short_description: article.short_description,
    summary: article.summary,
    category: article.category?.slug ?? "",
    content: article.content,
    page_type: article.page_type,
    is_stub: article.is_stub,
    infobox: infoboxToDraft(article.infobox),
    references: referencesToDrafts(article.references),
    lead_image_url: article.lead_image_url,
    lead_image_alt: article.lead_image_alt,
    lead_image_caption: article.lead_image_caption,
    lead_image_credit: article.lead_image_credit,
    lead_image_license: article.lead_image_license,
    lead_image_source_url: article.lead_image_source_url,
    // Revision metadata always starts empty: the previous edit's summary is
    // not this edit's summary, and a pre-ticked "minor" is a lie.
    comment: "",
    is_minor: false,
    is_published: article.is_published,
    watch: article.is_watched,
  };
}

/**
 * `ArticleInput` in `lib/types.ts` has no `is_minor`, but
 * `ArticleWriteSerializer` declares it (write-only, it lands on the Revision).
 * Intersecting locally rather than editing another agent's module — see the
 * report.
 */
export type ArticleWriteInput = ArticleInput & { is_minor?: boolean };

/**
 * The form → the write payload.
 *
 * Trimming happens here rather than in the inputs, so the caret never jumps
 * while somebody is typing a title with a space in the middle of it.
 */
export function buildPayload(form: EditorForm): ArticleWriteInput {
  return {
    title: form.title.trim(),
    short_description: form.short_description.trim(),
    summary: form.summary.trim(),
    content: form.content,
    category: form.category || null,
    page_type: form.page_type,
    is_stub: form.is_stub,
    infobox: toInfobox(form.infobox),
    lead_image_url: form.lead_image_url.trim(),
    lead_image_alt: form.lead_image_alt.trim(),
    lead_image_caption: form.lead_image_caption.trim(),
    lead_image_credit: form.lead_image_credit.trim(),
    lead_image_license: form.lead_image_license.trim(),
    lead_image_source_url: form.lead_image_source_url.trim(),
    references: toReferences(form.references),
    is_published: form.is_published,
    comment: form.comment.trim(),
    is_minor: form.is_minor,
  };
}

/* =====================================================================
   Local validation
   =====================================================================
   Client-side checks exist to save a round trip and to put the message next
   to the control. The server is still the authority: `fieldErrors()` below
   maps its answer back onto the same field names.
   ===================================================================== */

export type FieldErrors = Partial<Record<keyof EditorForm | "detail", string>>;

/**
 * The hosts a lead image may come from.
 *
 * Deliberately the same two as the CSP's `img-src` and the server's
 * `LEAD_IMAGE_ALLOWED_HOSTS` (DECISIONS §7.3, §7.4). Checking it here is not a
 * substitute for the server check — it is so the author is told before they
 * save, rather than getting a field-level 400 after.
 */
export const LEAD_IMAGE_HOSTS = [
  "upload.wikimedia.org",
  "commons.wikimedia.org",
];

export function validateForm(form: EditorForm): FieldErrors {
  const errors: FieldErrors = {};

  if (form.title.trim().length < 3) {
    errors.title = "A title needs at least 3 characters.";
  }
  if (form.content.trim().length === 0) {
    errors.content = "An article needs a body.";
  }

  const imageUrl = form.lead_image_url.trim();
  if (imageUrl) {
    if (!form.lead_image_alt.trim()) {
      errors.lead_image_alt =
        "Describe the image for readers who cannot see it. This is required.";
    }
    let host = "";
    try {
      host = new URL(imageUrl).hostname.toLowerCase();
    } catch {
      host = "";
    }
    if (!LEAD_IMAGE_HOSTS.includes(host)) {
      errors.lead_image_url = `An image must be hosted on ${LEAD_IMAGE_HOSTS.join(" or ")}. The page's Content Security Policy refuses every other origin.`;
    }
  }

  return errors;
}

/**
 * A DRF error body → the same field names the form uses.
 *
 * DRF answers `{field: ["message"]}`, `{detail: "message"}`, or a nested
 * `{references: [{key: ["message"]}]}`. All three flatten to one string per
 * top-level field, which is what an inline message under a control can show.
 * DECISIONS §15: submitting `protection` or `is_published` without the right
 * to change it arrives here as a field-level 400 naming the field — so it
 * lands under that field, not in a toast.
 */
export function fieldErrors(error: unknown): FieldErrors {
  if (!axios.isAxiosError(error)) return {};
  const data = error.response?.data;
  if (!data || typeof data !== "object" || Array.isArray(data)) return {};

  const out: Record<string, string> = {};
  for (const [key, value] of Object.entries(data as Record<string, unknown>)) {
    const message = flattenError(value);
    if (message) out[key === "non_field_errors" ? "detail" : key] = message;
  }
  return out as FieldErrors;
}

function flattenError(value: unknown): string {
  if (typeof value === "string") return value;
  if (Array.isArray(value)) {
    return value.map(flattenError).filter(Boolean).join(" ");
  }
  if (value && typeof value === "object") {
    return Object.entries(value as Record<string, unknown>)
      .map(([key, nested]) => {
        const message = flattenError(nested);
        return message ? `${key}: ${message}` : "";
      })
      .filter(Boolean)
      .join(" ");
  }
  return "";
}

/* =====================================================================
   Drafts
   =====================================================================
   `wikiverse.draft.<slug|new>` (design-ui §5.6). Restored only behind a
   visible notice, never silently: silently replacing what is on screen with
   something from last Tuesday is indistinguishable from data loss.
   ===================================================================== */

export const DRAFT_PREFIX = "wikiverse.draft.";

export function draftKey(slug?: string): string {
  return `${DRAFT_PREFIX}${slug ?? "new"}`;
}

export interface StoredDraft {
  /** ISO timestamp, shown in the restore notice. */
  saved_at: string;
  /** The revision the draft was based on, so a stale draft is detectable. */
  based_on: number | null;
  form: EditorForm;
}

export function readDraft(key: string): StoredDraft | null {
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<StoredDraft>;
    if (!parsed || typeof parsed !== "object" || !parsed.form) return null;
    if (typeof parsed.saved_at !== "string") return null;
    return {
      saved_at: parsed.saved_at,
      based_on: typeof parsed.based_on === "number" ? parsed.based_on : null,
      // Merge over a fresh form so a draft written by an older build, before a
      // field existed, still restores instead of rendering `undefined`.
      form: { ...emptyForm(), ...parsed.form },
    };
  } catch {
    // Blocked storage, private mode, or a half-written value. Not having a
    // draft is a normal state; throwing out of the editor's mount is not.
    return null;
  }
}

export function writeDraft(key: string, draft: StoredDraft): void {
  try {
    window.localStorage.setItem(key, JSON.stringify(draft));
  } catch {
    // Quota or private mode. Autosave is a courtesy, not a contract.
  }
}

export function clearDraft(key: string): void {
  try {
    window.localStorage.removeItem(key);
  } catch {
    /* see above */
  }
}

/* =====================================================================
   Mutations
   ===================================================================== */

/**
 * Create (`POST /articles/`) or edit (`PATCH /articles/{slug}/`).
 *
 * `PATCH` rather than `PUT`: the serialiser treats a write to an existing
 * instance as a partial replace, and a wiki edit form posts what it edited.
 */
export function useSaveArticle(slug?: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: ArticleWriteInput) => {
      if (slug) {
        const { data } = await api.patch<Article>(`/articles/${slug}/`, payload);
        return data;
      }
      const { data } = await api.post<Article>("/articles/", payload);
      return data;
    },
    onSuccess: (article) => {
      queryClient.setQueryData(articleKeys.detail(article.slug), article);
      queryClient.invalidateQueries({ queryKey: articleKeys.all });
      // The feeds this edit now appears in.
      queryClient.invalidateQueries({ queryKey: ["changes"] });
      queryClient.invalidateQueries({ queryKey: ["main-page"] });
    },
  });
}

/** `POST` / `DELETE /api/articles/{slug}/watch/` (DECISIONS §17). */
export function useSetWatch() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ slug, watch }: { slug: string; watch: boolean }) => {
      if (watch) await api.post(`/articles/${slug}/watch/`);
      else await api.delete(`/articles/${slug}/watch/`);
      return watch;
    },
    onSuccess: (_watch, { slug }) => {
      queryClient.invalidateQueries({ queryKey: articleKeys.detail(slug) });
      queryClient.invalidateQueries({ queryKey: ["watchlist"] });
    },
  });
}

/* =====================================================================
   Text insertion — shared by the toolbar and the reference editor
   ===================================================================== */

/**
 * One insertion into the body. The editor page owns the single implementation
 * that applies it to the textarea, so the toolbar and the reference editor
 * cannot drift into two behaviours.
 */
export interface EditorInsertion {
  /** Text placed before the selection (or before the caret). */
  before: string;
  /** Text placed after it. */
  after?: string;
  /** Used when nothing is selected, and left selected afterwards. */
  placeholder?: string;
  /** Force the insertion onto a line of its own, separated by a blank line. */
  block?: boolean;
}

let seq = 0;

/** A React key for a draft row. Not an id and never sent anywhere. */
export function uid(): string {
  return `r${++seq}`;
}
