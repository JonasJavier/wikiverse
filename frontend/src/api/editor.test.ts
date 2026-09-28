import { AxiosError, AxiosHeaders, type AxiosResponse } from "axios";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { Infobox } from "@/lib/types";
import {
  auditIsClean,
  auditReferences,
  buildPayload,
  citedKeys,
  clearDraft,
  draftKey,
  emptyForm,
  fieldErrors,
  infoboxToDraft,
  LEAD_IMAGE_HOSTS,
  newInfoboxRow,
  newReferenceDraft,
  readDraft,
  referenceMarker,
  referencesToDrafts,
  toInfobox,
  toReferences,
  validateForm,
  writeDraft,
  type EditorForm,
  type ReferenceDraft,
  type StoredDraft,
} from "./editor";

vi.mock("@/lib/api", () => ({
  API_BASE_URL: "http://api.test/api",
  api: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  apiErrorMessage: () => "error",
}));

function refDraft(key: string, title = `Title of ${key}`, extra: Partial<ReferenceDraft> = {}) {
  return { ...newReferenceDraft(), key, title, ...extra };
}

function form(patch: Partial<EditorForm> = {}): EditorForm {
  return { ...emptyForm("Photosynthesis"), content: "Body.", ...patch };
}

describe("infobox draft ⇄ DECISIONS §1 schema", () => {
  const infobox: Infobox = {
    title: "Marie Curie",
    subtitle: "Physicist and chemist",
    rows: [
      { kind: "header", value: "Personal details" },
      { kind: "row", label: "Born", value: "7 November 1867[^curie]" },
      { kind: "full", value: "*Nobel laureate* in [[Physics]]" },
    ],
  };

  it("round-trips exactly", () => {
    expect(toInfobox(infoboxToDraft(infobox))).toEqual(infobox);
  });

  it("gives every draft row a uid that is stripped on the way out", () => {
    const draft = infoboxToDraft(infobox);
    expect(new Set(draft.rows.map((r) => r.uid)).size).toBe(3);
    for (const row of toInfobox(draft)?.rows ?? []) expect(row).not.toHaveProperty("uid");
  });

  it("emits header and full rows WITHOUT a label, even if one was typed", () => {
    const draft = infoboxToDraft(null);
    draft.rows.push(
      { ...newInfoboxRow("header"), label: "leftover", value: "Section" },
      { ...newInfoboxRow("full"), label: "leftover", value: "Wide" },
    );
    expect(toInfobox(draft)?.rows).toEqual([
      { kind: "header", value: "Section" },
      { kind: "full", value: "Wide" },
    ]);
  });

  it("trims, drops rows with no value, and omits a blank title/subtitle", () => {
    const draft = infoboxToDraft(null);
    draft.title = "   ";
    draft.rows.push(
      { ...newInfoboxRow("row"), label: " Born ", value: " 1867 " },
      { ...newInfoboxRow("row"), label: "Died", value: "   " },
    );
    const out = toInfobox(draft);
    expect(out).toEqual({ rows: [{ kind: "row", label: "Born", value: "1867" }] });
    expect(out).not.toHaveProperty("title");
    expect(out).not.toHaveProperty("image");
  });

  it("serialises an empty infobox as null, so removal is expressible", () => {
    expect(toInfobox(infoboxToDraft(null))).toBeNull();
    expect(toInfobox(infoboxToDraft({}))).toBeNull();
  });
});

describe("references", () => {
  it("the in-text marker is [^key] (DECISIONS §11)", () => {
    expect(referenceMarker("curie1903")).toBe("[^curie1903]");
  });

  it("citedKeys lists each [^key] once, in first-appearance order", () => {
    expect(citedKeys("A[^b] B[^a] C[^b] [ref:c] [^not valid]")).toEqual(["b", "a"]);
  });

  it("audits uncited, unresolved, duplicate, malformed and untitled keys", () => {
    const drafts = [
      refDraft("used"),
      refDraft("unused"),
      refDraft("dup"),
      refDraft("dup"),
      refDraft("bad key"),
      refDraft("notitle", "  "),
      refDraft("", ""),
    ];
    const audit = auditReferences(drafts, "x[^used] y[^dup] z[^ghost] w[^notitle]");
    expect(audit).toEqual({
      uncited: ["unused", "bad key"],
      unresolved: ["ghost"],
      duplicate: ["dup"],
      malformed: ["bad key"],
      untitled: ["notitle"],
    });
    expect(auditIsClean(audit)).toBe(false);
  });

  it("a fully cited, well-formed list is clean", () => {
    const audit = auditReferences([refDraft("a"), refDraft("b-2")], "x[^a] y[^b-2]");
    expect(auditIsClean(audit)).toBe(true);
  });

  it("toReferences drops keyless rows, re-indexes order and nulls a blank date", () => {
    const out = toReferences([
      refDraft(" a ", " A title ", { accessed_on: "" }),
      refDraft("", "orphan"),
      refDraft("b", "B", { accessed_on: "2026-09-26" }),
    ]);
    expect(out.map((r) => [r.key, r.order, r.title, r.accessed_on])).toEqual([
      ["a", 0, "A title", null],
      ["b", 1, "B", "2026-09-26"],
    ]);
    expect(out[0]).not.toHaveProperty("uid");
  });

  it("referencesToDrafts sorts by order and blanks a null date", () => {
    const drafts = referencesToDrafts(
      toReferences([refDraft("x"), refDraft("y", "Y", { accessed_on: "2026-01-02" })])
        .reverse(),
    );
    expect(drafts.map((d) => [d.key, d.accessed_on])).toEqual([
      ["x", ""],
      ["y", "2026-01-02"],
    ]);
  });
});

describe("buildPayload", () => {
  it("trims text fields but never the body", () => {
    const payload = buildPayload(
      form({ title: "  Photosynthesis  ", summary: " S ", content: "  indented code\n" }),
    );
    expect(payload.title).toBe("Photosynthesis");
    expect(payload.summary).toBe("S");
    expect(payload.content).toBe("  indented code\n");
  });

  it("sends a blank category as null and the infobox in §1 shape", () => {
    const f = form();
    f.infobox.rows.push({ ...newInfoboxRow("header"), label: "x", value: "Facts" });
    const payload = buildPayload(f);
    expect(payload.category).toBeNull();
    expect(payload.infobox).toEqual({ rows: [{ kind: "header", value: "Facts" }] });
    expect(buildPayload(form({ category: "biology" })).category).toBe("biology");
  });

  it("carries the lead image as Article columns, and never the local-only `watch`", () => {
    const payload = buildPayload(
      form({ lead_image_url: " https://upload.wikimedia.org/a.jpg ", lead_image_credit: " NASA " }),
    );
    expect(payload.lead_image_url).toBe("https://upload.wikimedia.org/a.jpg");
    expect(payload.lead_image_credit).toBe("NASA");
    expect(payload).not.toHaveProperty("watch");
    expect(payload.infobox).toBeNull();
  });

  it("includes the revision metadata", () => {
    const payload = buildPayload(form({ comment: " typo ", is_minor: true }));
    expect(payload.comment).toBe("typo");
    expect(payload.is_minor).toBe(true);
  });
});

describe("validateForm", () => {
  it("accepts a minimal valid form", () => {
    expect(validateForm(form())).toEqual({});
  });

  it("requires a 3-character title and a body", () => {
    const errors = validateForm(form({ title: " ab ", content: "   " }));
    expect(Object.keys(errors).sort()).toEqual(["content", "title"]);
  });

  it("requires alt text whenever there is a lead image", () => {
    const errors = validateForm(
      form({ lead_image_url: "https://upload.wikimedia.org/x.jpg", lead_image_alt: " " }),
    );
    expect(errors.lead_image_alt).toBeDefined();
    expect(errors.lead_image_url).toBeUndefined();
  });

  it.each([
    "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
    "https://commons.wikimedia.org/wiki/File:Example.jpg",
    "https://UPLOAD.WIKIMEDIA.ORG/x.jpg",
  ])("allows %s", (url) => {
    expect(validateForm(form({ lead_image_url: url, lead_image_alt: "A photo" }))).toEqual({});
  });

  it.each([
    "https://example.com/x.jpg",
    "https://upload.wikimedia.org.evil.example/x.jpg",
    "https://evil.example/upload.wikimedia.org/x.jpg",
    "http://upload.wikimedia.org/x.jpg",
    "//upload.wikimedia.org/x.jpg",
    "javascript:alert(1)",
    "not a url",
  ])("rejects %s", (url) => {
    const errors = validateForm(form({ lead_image_url: url, lead_image_alt: "A photo" }));
    expect(errors.lead_image_url).toMatch(/upload\.wikimedia\.org/);
  });

  it("uses the same two hosts as the CSP img-src (DECISIONS §7)", () => {
    expect(LEAD_IMAGE_HOSTS).toEqual(["upload.wikimedia.org", "commons.wikimedia.org"]);
  });
});

describe("fieldErrors", () => {
  function axiosError(data: unknown): AxiosError {
    const response = {
      data,
      status: 400,
      statusText: "Bad Request",
      headers: {},
      config: { headers: new AxiosHeaders() },
    } as AxiosResponse;
    return new AxiosError("Bad Request", "ERR_BAD_REQUEST", undefined, undefined, response);
  }

  it("flattens DRF field, non-field and nested errors", () => {
    expect(
      fieldErrors(
        axiosError({
          title: ["Too short.", "Taken."],
          non_field_errors: ["Nope."],
          references: [{ key: ["Invalid slug."] }, {}],
          is_published: "You may not change this.",
        }),
      ),
    ).toEqual({
      title: "Too short. Taken.",
      detail: "Nope.",
      references: "key: Invalid slug.",
      is_published: "You may not change this.",
    });
  });

  it("returns nothing for a non-axios error or a non-object body", () => {
    expect(fieldErrors(new Error("boom"))).toEqual({});
    expect(fieldErrors(axiosError("<html>502</html>"))).toEqual({});
    expect(fieldErrors(axiosError(["list"]))).toEqual({});
  });
});

describe("draft storage", () => {
  const key = draftKey("photosynthesis");
  const stored: StoredDraft = {
    saved_at: "2026-09-27T10:00:00.000Z",
    based_on: 42,
    form: form({ content: "Draft body" }),
  };

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("namespaces keys as wikiverse.draft.<slug|new>", () => {
    expect(key).toBe("wikiverse.draft.photosynthesis");
    expect(draftKey()).toBe("wikiverse.draft.new");
  });

  it("writes, reads back and clears a draft", () => {
    writeDraft(key, stored);
    expect(readDraft(key)).toEqual(stored);
    clearDraft(key);
    expect(readDraft(key)).toBeNull();
  });

  it("merges an old draft over a fresh form so new fields are never undefined", () => {
    window.localStorage.setItem(
      key,
      JSON.stringify({ saved_at: stored.saved_at, based_on: "x", form: { title: "Old" } }),
    );
    const draft = readDraft(key);
    expect(draft?.based_on).toBeNull();
    expect(draft?.form.title).toBe("Old");
    expect(draft?.form.lead_image_credit).toBe("");
    expect(draft?.form.references).toEqual([]);
  });

  it.each([
    ["corrupt JSON", "{not json"],
    ["no form", JSON.stringify({ saved_at: "2026-09-27" })],
    ["no timestamp", JSON.stringify({ form: {} })],
    ["null", "null"],
  ])("treats %s as no draft", (_label, raw) => {
    window.localStorage.setItem(key, raw);
    expect(readDraft(key)).toBeNull();
  });

  it("survives blocked storage without throwing", () => {
    const blocked = () => {
      throw new DOMException("The operation is insecure.", "SecurityError");
    };
    vi.stubGlobal("localStorage", {
      getItem: blocked,
      setItem: blocked,
      removeItem: blocked,
      clear: blocked,
      key: blocked,
      length: 0,
    });
    expect(() => writeDraft(key, stored)).not.toThrow();
    expect(readDraft(key)).toBeNull();
    expect(() => clearDraft(key)).not.toThrow();
  });
});
