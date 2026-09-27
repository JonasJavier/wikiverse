import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  useBlocker,
  useNavigate,
  useParams,
  useSearchParams,
  type BlockerFunction,
} from "react-router-dom";

import { useArticle } from "@/api/articles";
import { useCategories } from "@/api/categories";
import {
  buildPayload,
  clearDraft,
  draftKey,
  emptyForm,
  fieldErrors,
  formFromArticle,
  LEAD_IMAGE_HOSTS,
  LIMITS,
  readDraft,
  referenceMarker,
  useSaveArticle,
  useSetWatch,
  validateForm,
  writeDraft,
  type EditorForm,
  type EditorInsertion,
  type FieldErrors,
  type StoredDraft,
} from "@/api/editor";
import { EditorPreview } from "@/components/editor/EditorPreview";
import { EditSummaryBar } from "@/components/editor/EditSummaryBar";
import { InfoboxEditor } from "@/components/editor/InfoboxEditor";
import { MarkdownEditor } from "@/components/editor/MarkdownEditor";
import { ReferenceEditor } from "@/components/editor/ReferenceEditor";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { FieldError, FieldHint, Input, Label, Textarea } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/Spinner";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useIsShelf } from "@/hooks/useMediaQuery";
import type { PageType } from "@/lib/types";
import { cn, formatDateTime } from "@/lib/utils";
import { toast } from "@/store/toast";

const SELECT_CLASS =
  "h-9 w-full rounded-chrome border border-rule bg-page px-2 text-base text-ink " +
  "transition-colors duration-100";

const PAGE_TYPES: { value: PageType; label: string }[] = [
  { value: "article", label: "Article" },
  { value: "disambiguation", label: "Disambiguation page" },
  { value: "list", label: "List" },
];

/** Human names for the error summary, keyed by the field the server names. */
const FIELD_LABELS: Record<string, string> = {
  title: "Title",
  short_description: "Short description",
  summary: "Summary",
  content: "Body",
  category: "Category",
  page_type: "Page type",
  infobox: "Infobox",
  references: "References",
  lead_image_url: "Image URL",
  lead_image_alt: "Image description",
  lead_image_credit: "Image credit",
  lead_image_license: "Image licence",
  lead_image_source_url: "Image source page",
  comment: "Edit summary",
  is_published: "Publication state",
  protection: "Protection",
};

/**
 * The editor: `/new` (honouring `?title=`) and `/wiki/:slug/edit`.
 *
 * Four behaviours here are the reason this page was rewritten rather than
 * patched:
 *
 * 1. **Hydrate once, keyed on `existing.id`.** The old version re-ran its
 *    hydration effect on the `existing` object's *identity*, so any refetch —
 *    a window focus, a cache invalidation from anywhere in the app — silently
 *    replaced whatever the author had typed with the server's copy. A ref
 *    holding the id that has already been loaded closes that permanently.
 * 2. **Nothing is lost on the way out.** A `beforeunload` guard for the tab,
 *    a router `useBlocker` with a real `ConfirmDialog` for in-app navigation
 *    (never `window.confirm`), and a debounced draft in
 *    `wikiverse.draft.<slug|new>` as the backstop.
 * 3. **A draft is never restored silently.** It is offered, with the time it
 *    was written, and the author chooses. Silently replacing what is on screen
 *    with something from yesterday is indistinguishable from data loss.
 * 4. **`?title=` is load-bearing.** A red link points at `/new?title=<Title>`
 *    (DECISIONS §14, §19). Arriving here with the title already filled in is
 *    the entire reason a red link is a feature rather than a dead end.
 */
export function EditorPage() {
  const { slug } = useParams();
  const isEdit = Boolean(slug);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const isShelf = useIsShelf();

  /** The title a red link asked for. `URLSearchParams` has already decoded it. */
  const requestedTitle = (searchParams.get("title") ?? "").trim();

  const { data: existing, isLoading, isError } = useArticle(slug ?? "");
  const { data: categories } = useCategories();
  const save = useSaveArticle(slug);
  const setWatch = useSetWatch();

  const [form, setForm] = useState<EditorForm>(() =>
    emptyForm(isEdit ? "" : requestedTitle),
  );
  const [errors, setErrors] = useState<FieldErrors>({});
  const [summary, setSummary] = useState("");
  const [tab, setTab] = useState<"write" | "preview">("write");
  const [draftOffer, setDraftOffer] = useState<StoredDraft | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  /** JSON of the form as last loaded or saved. Dirtiness is a diff against it. */
  const baselineRef = useRef<string | null>(null);
  if (baselineRef.current === null) baselineRef.current = JSON.stringify(form);
  /** Which article id has already been hydrated. THE fix for the old bug. */
  const hydratedRef = useRef<number | null>(null);
  /** Set the instant a save succeeds, so the exit guard stands down. */
  const savedRef = useRef(false);

  const key = draftKey(slug);
  const serialised = JSON.stringify(form);
  const dirty = serialised !== baselineRef.current;

  useDocumentMeta({
    title: isEdit
      ? `Editing ${existing?.title ?? slug ?? ""}`
      : requestedTitle
        ? `Creating ${requestedTitle}`
        : "Create a new page",
    // An edit form has nothing to index and must never outrank the article.
    robots: "noindex",
  });

  /* --- hydration, exactly once per article id ------------------------- */
  useEffect(() => {
    if (!isEdit || !existing) return;
    if (hydratedRef.current === existing.id) return;
    hydratedRef.current = existing.id;

    const next = formFromArticle(existing);
    baselineRef.current = JSON.stringify(next);
    setForm(next);

    const stored = readDraft(draftKey(existing.slug));
    if (stored && JSON.stringify(stored.form) !== baselineRef.current) {
      setDraftOffer(stored);
    }
  }, [isEdit, existing]);

  /* --- a draft for a page that does not exist yet --------------------- */
  useEffect(() => {
    if (isEdit) return;
    const stored = readDraft(draftKey(undefined));
    if (stored && JSON.stringify(stored.form) !== baselineRef.current) {
      setDraftOffer(stored);
    }
  }, [isEdit]);

  /* --- autosave, debounced ------------------------------------------- */
  useEffect(() => {
    if (!dirty) return;
    const timer = setTimeout(() => {
      writeDraft(key, {
        saved_at: new Date().toISOString(),
        based_on: existing?.latest_revision?.id ?? null,
        form,
      });
    }, 1000);
    return () => clearTimeout(timer);
  }, [dirty, form, key, existing]);

  /* --- the tab-close guard ------------------------------------------- */
  useEffect(() => {
    if (!dirty) return;
    const handler = (event: BeforeUnloadEvent) => {
      // The browser owns the wording; preventDefault is the whole API.
      event.preventDefault();
    };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, [dirty]);

  /* --- the in-app navigation guard ----------------------------------- */
  const shouldBlock = useCallback<BlockerFunction>(
    ({ currentLocation, nextLocation }) =>
      dirty &&
      !savedRef.current &&
      currentLocation.pathname !== nextLocation.pathname,
    [dirty],
  );
  const blocker = useBlocker(shouldBlock);

  /* --- the one implementation of "put this at the caret" -------------- */
  const insert = useCallback((insertion: EditorInsertion) => {
    const node = textareaRef.current;
    if (!node) return;

    const { value } = node;
    let start = node.selectionStart;
    let end = node.selectionEnd;
    const body = value.slice(start, end) || insertion.placeholder || "";

    let before = insertion.before;
    let after = insertion.after ?? "";

    if (insertion.block) {
      // Put a block construct on a line of its own, without stacking blank
      // lines when it is already at the start of one.
      const preceding = value.slice(0, start);
      if (preceding && !/\n\n$/.test(preceding)) {
        before = (preceding.endsWith("\n") ? "\n" : "\n\n") + before;
      }
      const following = value.slice(end);
      if (following && !/^\n/.test(following)) after += "\n";
    }

    const next = value.slice(0, start) + before + body + after + value.slice(end);
    start += before.length;
    end = start + body.length;

    setForm((current) => ({ ...current, content: next }));

    // The textarea is controlled, so the caret has to be restored after React
    // has committed the new value. A zero timeout rather than
    // `requestAnimationFrame`: rAF does not run in a hidden or backgrounded
    // tab, which would leave the caret at the wrong offset for anyone who
    // clicked a toolbar button and switched away mid-edit.
    setTimeout(() => {
      node.focus();
      node.setSelectionRange(start, end);
    }, 0);
  }, []);

  const insertMarker = useCallback(
    (refKey: string) => insert({ before: referenceMarker(refKey) }),
    [insert],
  );

  function patch(partial: Partial<EditorForm>) {
    setForm((current) => ({ ...current, ...partial }));
  }

  /* --- save ---------------------------------------------------------- */
  const saving = save.isPending || setWatch.isPending;

  async function handleSave() {
    const local = validateForm(form);
    setErrors(local);
    if (Object.keys(local).length > 0) {
      setSummary("This page cannot be saved yet.");
      return;
    }
    setSummary("");

    try {
      const article = await save.mutateAsync(buildPayload(form));

      if (form.watch !== (existing?.is_watched ?? false)) {
        try {
          await setWatch.mutateAsync({ slug: article.slug, watch: form.watch });
        } catch {
          // Watching is a preference, not the edit. Never fail a saved edit on it.
          toast.warning("The page was saved, but your watchlist was not updated.");
        }
      }

      savedRef.current = true;
      baselineRef.current = JSON.stringify(form);
      clearDraft(key);
      toast.success(
        isEdit ? "Your changes are saved." : `“${article.title}” is created.`,
      );
      navigate(`/wiki/${article.slug}`);
    } catch (error) {
      const server = fieldErrors(error);
      setErrors(server);
      setSummary(
        server.detail ??
          (Object.keys(server).length > 0
            ? "The server rejected this edit."
            : "The edit could not be saved. Check your connection and try again."),
      );
    }
  }

  const problems = useMemo(
    () =>
      Object.entries(errors).filter(
        ([field, message]) => field !== "detail" && Boolean(message),
      ) as [string, string][],
    [errors],
  );

  const remaining = LIMITS.shortDescription - form.short_description.length;

  /* --- loading / error states ---------------------------------------- */
  if (isEdit && isLoading) {
    return (
      <div className="mx-auto w-full max-w-[54rem] px-4 py-10">
        <Spinner label="Loading the page you are editing" />
      </div>
    );
  }

  if (isEdit && isError) {
    return (
      <div className="mx-auto w-full max-w-[54rem] px-4 py-10">
        <h1 className="font-serif text-h1 font-normal text-ink">
          That page could not be loaded
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-3 text-base text-ink-2">
          It may have been deleted, or the address may be wrong.
        </p>
      </div>
    );
  }

  /* --- the source pane ----------------------------------------------- */
  /**
   * Below `shelf` the two panes are a tab pair; at `shelf` they are two
   * labelled regions side by side. The ARIA changes with the layout rather
   * than being left claiming a pattern the page is not using: a `tab` whose
   * `aria-controls` points at something that is not a `tabpanel` is worse than
   * no tabs at all.
   */
  function paneProps(pane: "write" | "preview") {
    if (isShelf) {
      return { "aria-label": pane === "write" ? "Source" : "Preview" };
    }
    return {
      role: "tabpanel",
      "aria-labelledby": `editor-tab-${pane}`,
      // The panel scrolls, so it has to be reachable by keyboard (ARIA APG).
      tabIndex: 0,
      hidden: tab !== pane,
    };
  }

  const sourcePane = (
    <section
      {...paneProps("write")}
      id="editor-source"
      className={cn("space-y-4", !isShelf && tab !== "write" && "hidden")}
    >
      <div>
        <Label htmlFor="article-title">Title</Label>
        <Input
          id="article-title"
          value={form.title}
          onChange={(event) => patch({ title: event.target.value })}
          maxLength={LIMITS.title}
          aria-invalid={Boolean(errors.title) || undefined}
          aria-describedby={errors.title ? "article-title-error" : undefined}
          required
        />
        {errors.title && <FieldError id="article-title-error">{errors.title}</FieldError>}
      </div>

      <div>
        <Label htmlFor="article-short">Short description</Label>
        <Input
          id="article-short"
          value={form.short_description}
          onChange={(event) => patch({ short_description: event.target.value })}
          maxLength={LIMITS.shortDescription}
          aria-describedby="article-short-hint"
          placeholder="Polish-French physicist and chemist"
        />
        <FieldHint id="article-short-hint">
          A five-to-twelve word gloss, with no final point. It is what the
          typeahead and the hover card show. {remaining} characters left; aim for{" "}
          {LIMITS.shortDescriptionIdeal} or fewer.
        </FieldHint>
        {errors.short_description && (
          <FieldError>{errors.short_description}</FieldError>
        )}
      </div>

      <div>
        <Label htmlFor="article-summary">Summary</Label>
        <Textarea
          id="article-summary"
          value={form.summary}
          onChange={(event) => patch({ summary: event.target.value })}
          maxLength={LIMITS.summary}
          rows={2}
          aria-describedby="article-summary-hint"
          placeholder="One or two sentences. Shown on cards, in search results and as the page's meta description."
        />
        <FieldHint id="article-summary-hint">
          {LIMITS.summary - form.summary.length} characters left.
        </FieldHint>
        {errors.summary && <FieldError>{errors.summary}</FieldError>}
      </div>

      <div className="grid gap-3 sm:grid-cols-[1fr_1fr_auto]">
        <div>
          <Label htmlFor="article-category">Category</Label>
          <select
            id="article-category"
            value={form.category}
            onChange={(event) => patch({ category: event.target.value })}
            className={SELECT_CLASS}
          >
            <option value="">No category</option>
            {categories?.map((category) => (
              <option key={category.id} value={category.slug}>
                {category.name}
              </option>
            ))}
          </select>
          {errors.category && <FieldError>{errors.category}</FieldError>}
        </div>

        <div>
          <Label htmlFor="article-page-type">Page type</Label>
          <select
            id="article-page-type"
            value={form.page_type}
            onChange={(event) =>
              patch({ page_type: event.target.value as PageType })
            }
            className={SELECT_CLASS}
          >
            {PAGE_TYPES.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        <label className="flex items-center gap-2 self-end pb-2 text-ui text-ink">
          <input
            type="checkbox"
            className="size-4 shrink-0 accent-[var(--ink-1)]"
            checked={form.is_stub}
            onChange={(event) => patch({ is_stub: event.target.checked })}
          />
          Stub
        </label>
      </div>

      {/* The lead image: six ARTICLE columns. It is deliberately not part of
          the infobox — DECISIONS §1 has no `image` key, and one put there
          would be dropped by the serialiser without a word. */}
      <details className="rounded-chrome border border-rule bg-panel">
        <summary className="cursor-pointer px-3 py-2 text-ui font-medium text-ink">
          Lead image{" "}
          <span className="font-normal text-ink-2">
            {form.lead_image_url ? "— set" : "— none"}
          </span>
        </summary>
        <div className="space-y-3 border-t border-rule-hair px-3 py-3">
          <div>
            <Label htmlFor="image-url">Image URL</Label>
            <Input
              id="image-url"
              type="url"
              inputMode="url"
              value={form.lead_image_url}
              onChange={(event) => patch({ lead_image_url: event.target.value })}
              spellCheck={false}
              aria-invalid={Boolean(errors.lead_image_url) || undefined}
              aria-describedby="image-url-hint"
              placeholder="https://upload.wikimedia.org/…"
            />
            <FieldHint id="image-url-hint">
              Only {LEAD_IMAGE_HOSTS.join(" and ")} are allowed; the page's
              Content Security Policy refuses every other origin.
            </FieldHint>
            {errors.lead_image_url && (
              <FieldError>{errors.lead_image_url}</FieldError>
            )}
          </div>

          <div>
            <Label htmlFor="image-alt">
              Image description <span className="text-ink-2">(required)</span>
            </Label>
            <Input
              id="image-alt"
              value={form.lead_image_alt}
              onChange={(event) => patch({ lead_image_alt: event.target.value })}
              aria-invalid={Boolean(errors.lead_image_alt) || undefined}
              aria-describedby="image-alt-hint"
              placeholder="A seated woman in a dark dress beside laboratory glassware"
            />
            <FieldHint id="image-alt-hint">
              What the image shows, for a reader who cannot see it. Not the same
              text as the caption.
            </FieldHint>
            {errors.lead_image_alt && (
              <FieldError>{errors.lead_image_alt}</FieldError>
            )}
          </div>

          <div>
            <Label htmlFor="image-caption">Caption</Label>
            <Input
              id="image-caption"
              value={form.lead_image_caption}
              onChange={(event) =>
                patch({ lead_image_caption: event.target.value })
              }
              placeholder="Marie Curie in her laboratory, c. 1905"
            />
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <div>
              <Label htmlFor="image-credit">Credit</Label>
              <Input
                id="image-credit"
                value={form.lead_image_credit}
                onChange={(event) =>
                  patch({ lead_image_credit: event.target.value })
                }
                aria-describedby="image-credit-hint"
                placeholder="Wikimedia Commons"
              />
              <FieldHint id="image-credit-hint">
                Whenever this is filled in, the article prints the credit line.
                It is the attribution requirement, not a styling choice.
              </FieldHint>
            </div>
            <div>
              <Label htmlFor="image-license">Licence</Label>
              <Input
                id="image-license"
                value={form.lead_image_license}
                onChange={(event) =>
                  patch({ lead_image_license: event.target.value })
                }
                placeholder="CC BY-SA 4.0"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="image-source">Source page</Label>
            <Input
              id="image-source"
              type="url"
              inputMode="url"
              value={form.lead_image_source_url}
              onChange={(event) =>
                patch({ lead_image_source_url: event.target.value })
              }
              spellCheck={false}
              placeholder="https://commons.wikimedia.org/wiki/File:…"
            />
          </div>
        </div>
      </details>

      <InfoboxEditor
        value={form.infobox}
        onChange={(infobox) => patch({ infobox })}
        articleTitle={form.title}
      />

      <ReferenceEditor
        value={form.references}
        onChange={(references) => patch({ references })}
        content={form.content}
        onInsertMarker={insertMarker}
      />

      <div>
        <Label htmlFor="article-content">Body</Label>
        <MarkdownEditor
          id="article-content"
          value={form.content}
          onChange={(content) => patch({ content })}
          textareaRef={textareaRef}
          onInsert={insert}
          invalid={Boolean(errors.content)}
          describedBy={errors.content ? "article-content-error" : undefined}
        />
        {errors.content && (
          <FieldError id="article-content-error">{errors.content}</FieldError>
        )}
      </div>
    </section>
  );

  const previewPane = (
    <section
      {...paneProps("preview")}
      id="editor-preview"
      className={cn(!isShelf && tab !== "preview" && "hidden")}
    >
      <EditorPreview
        content={form.content}
        title={form.title}
        short_description={form.short_description}
        references={form.references}
        className={cn(
          "max-h-none",
          isShelf &&
            "sticky top-[calc(var(--subheader-h)+1rem)] max-h-[calc(100vh-var(--subheader-h)-3rem)]",
        )}
      />
    </section>
  );

  return (
    <div className="mx-auto w-full max-w-[82rem] px-4 py-6">
      <h1 className="font-serif text-h1 font-normal text-ink">
        {isEdit ? `Editing ${existing?.title ?? ""}` : "Create a new page"}
      </h1>
      <hr className="mt-1.5 border-0 border-t border-rule" />
      <p className="mt-1.5 text-ui text-ink-2">
        {isEdit ? (
          <>
            Every edit is recorded in the page history under your name, with the
            summary you write below.
          </>
        ) : requestedTitle ? (
          <>
            This page does not exist yet. You arrived from a red link to{" "}
            <span className="font-medium text-ink">{requestedTitle}</span> — the
            title is filled in for you.
          </>
        ) : (
          <>
            Write in neutral, third-person prose. Start the body at{" "}
            <code className="font-mono">##</code>; the title above becomes the
            page's only heading.
          </>
        )}
      </p>

      {/* The draft offer. Visible, dated, and dismissible — never automatic. */}
      {draftOffer && (
        <div
          role="status"
          className="mt-4 rounded-chrome border-l-[6px] border-l-banner-notice border-y border-r border-rule bg-panel px-3 py-2.5"
        >
          <p className="text-base text-ink">
            Restore the draft you were writing at{" "}
            {formatDateTime(draftOffer.saved_at)}?
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            <Button
              size="sm"
              onClick={() => {
                setForm(draftOffer.form);
                setDraftOffer(null);
              }}
            >
              Restore the draft
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setDraftOffer(null)}
            >
              Keep what is here
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => {
                clearDraft(key);
                setDraftOffer(null);
              }}
            >
              Discard the draft
            </Button>
          </div>
        </div>
      )}

      {/* One summary above the form, plus an inline message under each control.
          Never a toast: a toast for a validation error disappears before it can
          be acted on, and cannot be re-read. */}
      {(summary || problems.length > 0) && (
        <div
          role="alert"
          className="mt-4 rounded-chrome border-l-[6px] border-l-danger border-y border-r border-rule bg-panel px-3 py-2.5"
        >
          <p className="text-base font-medium text-ink">
            {summary || "This page cannot be saved yet."}
          </p>
          {problems.length > 0 && (
            <ul className="mt-1 list-disc space-y-0.5 pl-5 text-ui text-ink">
              {problems.map(([field, message]) => (
                <li key={field}>
                  <span className="font-medium">
                    {FIELD_LABELS[field] ?? field}:
                  </span>{" "}
                  {message}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Below `shelf` the two panes become a tab pair. Both stay mounted —
          the hidden one carries no ids of its own, so nothing is duplicated,
          and keeping it mounted means switching to Preview does not re-run the
          markdown pipeline from cold on a phone. */}
      {!isShelf && (
        <div
          role="tablist"
          aria-label="Editor view"
          className="mt-4 flex gap-1 border-b border-rule"
        >
          {(["write", "preview"] as const).map((value) => (
            <button
              key={value}
              type="button"
              role="tab"
              id={`editor-tab-${value}`}
              aria-selected={tab === value}
              aria-controls={value === "write" ? "editor-source" : "editor-preview"}
              onClick={() => setTab(value)}
              className={cn(
                "-mb-px cursor-pointer border-b-2 px-3 py-1.5 text-ui transition-colors duration-100",
                tab === value
                  ? "border-b-ink font-medium text-ink"
                  : "border-b-transparent text-ink-2 hover:text-ink",
              )}
            >
              {value === "write" ? "Write" : "Preview"}
            </button>
          ))}
        </div>
      )}

      <form
        onSubmit={(event) => {
          event.preventDefault();
          void handleSave();
        }}
      >
        <div className="mt-4 grid items-start gap-4 shelf:grid-cols-2 shelf:gap-6">
          {sourcePane}
          {previewPane}
        </div>

        <EditSummaryBar
          comment={form.comment}
          onCommentChange={(comment) => patch({ comment })}
          isMinor={form.is_minor}
          onMinorChange={(is_minor) => patch({ is_minor })}
          isPublished={form.is_published}
          onPublishedChange={(is_published) => patch({ is_published })}
          watch={form.watch}
          onWatchChange={(watch) => patch({ watch })}
          canWatch
          onPreview={() => {
            setTab("preview");
            document.getElementById("editor-preview")?.scrollIntoView({
              behavior: "auto",
              block: "start",
            });
          }}
          showPreviewButton={!isShelf}
          onSave={() => void handleSave()}
          onCancel={() => navigate(isEdit && slug ? `/wiki/${slug}` : "/")}
          saving={saving}
          dirty={dirty}
          isEdit={isEdit}
          commentError={errors.comment}
        />
      </form>

      <ConfirmDialog
        open={blocker.state === "blocked"}
        title="Leave without saving?"
        body={
          <p>
            Your changes to{" "}
            <span className="font-medium">
              {form.title.trim() || "this page"}
            </span>{" "}
            have not been saved. A draft is kept in this browser, so you can pick
            it up where you left off.
          </p>
        }
        tone="danger"
        confirmLabel="Leave the page"
        cancelLabel="Keep editing"
        onConfirm={() => blocker.proceed?.()}
        onCancel={() => blocker.reset?.()}
      />
    </div>
  );
}
