/**
 * Every DTO the app exchanges with the API, in one module.
 *
 * This file is the typed mirror of the API contract in DECISIONS.md
 * (sections 1, 2, 4, 5, 10, 11, 14, 16, 17 and 19). Field names here are
 * exact and are part of the contract; nullability here is what makes the
 * rest of the frontend correct, because `tsc -b` is the only thing that
 * catches "the backend can send null here" before a reader sees a blank
 * page.
 *
 * Two conventions hold throughout:
 *  - A Django `CharField(blank=True)` arrives as `""`, never `null`, so it
 *    is typed `string`. A nullable FK or a `null=True` column is typed
 *    `T | null`. Only genuinely optional response keys use `?`.
 *  - ISO 8601 strings carry dates and datetimes. `accessed_on` is a date
 *    (`YYYY-MM-DD`); everything named `*_at` or `timestamp` is a datetime.
 */

/* =====================================================================
   Enumerations — string unions, matching the backend TextChoices values
   ===================================================================== */

/** `Article.page_type`. `is_disambiguation` is derived from this, not stored. */
export type PageType = "article" | "disambiguation" | "list";

/** `Article.protection`. */
export type ProtectionLevel = "open" | "semi" | "locked";

/** Discriminant on a Recent-Changes / watchlist / contributions row. */
export type ChangeKind = "edit" | "talk";

/** `/api/changes/?type=` — the URL is the source of truth (DECISIONS §4). */
export type ChangeTypeFilter = "edit" | "talk" | "all";

/**
 * The search sort control offers exactly these three. "most edited" was cut
 * (DECISIONS §2) — do not add it back.
 */
export type SearchSort = "relevance" | "newest" | "oldest";

/** `MainPageBlock.kind` (DECISIONS §5). "In the news" was cut. */
export type MainPageBlockKind = "featured" | "dyk" | "otd";

/* =====================================================================
   Users
   ===================================================================== */

/**
 * The signed-in user's own record. `email` is present ONLY here — never
 * render it for anybody else, and never read it off a `PublicUser`.
 */
export interface User {
  id: number;
  username: string;
  email: string;
  bio: string;
  avatar: string | null;
  article_count: number;
  edit_count: number;
  date_joined: string;
  is_staff: boolean;
  is_bot: boolean;
}

/**
 * Any other user, from `GET /api/auth/users/{username}/`. Deliberately has
 * no `email`: the old serializer served every user's address to anonymous
 * callers, and the UI must not be able to surface it even by accident.
 */
export interface PublicUser {
  id: number;
  username: string;
  bio: string;
  avatar: string | null;
  article_count: number;
  edit_count: number;
  date_joined: string;
  is_staff: boolean;
  is_bot: boolean;
}

/** The nested author/editor stub (`AuthorSerializer`). */
export interface Author {
  id: number;
  username: string;
  avatar: string | null;
}

/* =====================================================================
   Categories
   ===================================================================== */

/**
 * `color` is a hex string and is NEVER used as a text or background colour
 * (DECISIONS §9): it renders as a leading rule or a dot, with the label in
 * ordinary ink. That removes the contrast problem structurally instead of
 * policing it.
 */
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  color: string;
  /** lucide-react icon name, e.g. "atom". `""` when unset. */
  icon: string;
  order: number;
  /** Nested parent; the taxonomy is capped at two levels. */
  parent: CategoryRef | null;
  article_count: number;
}

/** The nested form of a category, as it appears inside another object. */
export interface CategoryRef {
  slug: string;
  name: string;
  color: string;
}

/* =====================================================================
   The infobox (DECISIONS §1)
   =====================================================================
   The infobox NEVER carries an image — the lead image lives on `Article`
   columns. Every `value` is a plain string that may contain
   `[[Wikilinks]]`, `*emphasis*` and `[^refkey]` footnote markers, which the
   renderer resolves. There are no object or array values.
   ===================================================================== */

/** A section break inside the box. Carries `value`, NOT `label`. */
export interface InfoboxHeaderRow {
  kind: "header";
  value: string;
}

/** The ordinary label/value pair. */
export interface InfoboxLabelRow {
  kind: "row";
  label: string;
  value: string;
}

/** A full-width cell with no label. */
export interface InfoboxFullRow {
  kind: "full";
  value: string;
}

/** Discriminated on `kind`, so a `switch` over it is exhaustive. */
export type InfoboxRow = InfoboxHeaderRow | InfoboxLabelRow | InfoboxFullRow;

/**
 * `Article.infobox` is a JSONField defaulting to `{}`, so an article with
 * no infobox arrives as an empty object (or `null` from the seed) rather
 * than as a fully-shaped value. `rows` is therefore optional, and the
 * renderer must treat a missing or empty `rows` as "no infobox".
 */
export interface Infobox {
  /** Defaults to the article title when absent. */
  title?: string;
  subtitle?: string;
  rows?: InfoboxRow[];
}

/* =====================================================================
   References (DECISIONS §11)
   =====================================================================
   The in-text marker is `[^key]` everywhere — corpus, validator, renderer
   and the editor's insert button. `[ref:key]` does not exist.
   ===================================================================== */

export interface Reference {
  /** Short slug, unique within the article, e.g. "curie1903". */
  key: string;
  order: number;
  title: string;
  url: string;
  authors: string;
  publisher: string;
  /** Free text: "1986", "Spring 2004", "n.d.". Real sources are irregular. */
  published_on: string;
  /** A real date (`YYYY-MM-DD`) or null; renders as "Retrieved 12 March 2026". */
  accessed_on: string | null;
  /** One field for all three; the renderer prefix-sniffs doi: / ISBN / arXiv:. */
  identifier: string;
  quote: string;
}

/* =====================================================================
   Articles
   ===================================================================== */

/**
 * The smallest article reference: what a change row, a backlink, a
 * "recently featured" entry or a see-also target needs.
 */
export interface ArticleStub {
  slug: string;
  title: string;
  page_type: PageType;
  category: CategoryRef | null;
}

/**
 * `ArticleListSerializer`. Deliberately carries neither `content` nor
 * `infobox` — those are exactly what the list queryset defers.
 */
export interface ArticleListItem {
  id: number;
  title: string;
  slug: string;
  summary: string;
  /** <= 90-char gloss, no final period. Powers the typeahead and hover card. */
  short_description: string;
  category: Category | null;
  author: Author | null;
  page_type: PageType;
  is_stub: boolean;
  view_count: number;
  /** Minutes, derived from `word_count` — never from `content`. */
  read_time: number;
  word_count: number;
  /** UTF-8 BYTES, not characters. */
  byte_size: number;
  lead_image_url: string;
  created_at: string;
  updated_at: string;
}

/** `ArticleDetailSerializer` — the list shape plus the whole apparatus. */
export interface Article extends ArticleListItem {
  content: string;
  last_editor: Author | null;
  is_published: boolean;
  revision_count: number;
  /** Derived from `page_type`; there is no stored boolean. */
  is_disambiguation: boolean;
  protection: ProtectionLevel;
  /** `{}` or `null` when the article has none. */
  infobox: Infobox | null;
  references: Reference[];
  /** The lead image lives here, never inside `infobox` (DECISIONS §1). */
  lead_image_alt: string;
  lead_image_caption: string;
  /**
   * Non-empty means the credit line MUST render. It is not optional
   * styling — it is the attribution requirement.
   */
  lead_image_credit: string;
  lead_image_license: string;
  lead_image_source_url: string;
  backlink_count: number;
  talk_thread_count: number;
  /** Always `false` for an anonymous reader; never a per-row query. */
  is_watched: boolean;
  /** Set when the reader arrived through a redirect; drives "(Redirected from X)". */
  redirected_from: RedirectSource | null;
  latest_revision: Revision | null;
}

export interface RedirectSource {
  slug: string;
  title: string;
}

/** `GET /api/articles/{slug}/backlinks/` — "what links here". */
export interface Backlink {
  source: ArticleStub;
}

/** `GET /api/articles/{slug}/info/` — page information (DECISIONS §17). */
export interface PageInfo {
  byte_size: number;
  word_count: number;
  revision_count: number;
  contributor_count: number;
  watcher_count: number;
  created_at: string;
  updated_at: string;
  protection: ProtectionLevel;
}

/** The write payload for `POST`/`PUT`/`PATCH /api/articles/`. */
export interface ArticleInput {
  title: string;
  summary: string;
  short_description?: string;
  content: string;
  category: string | null;
  page_type?: PageType;
  is_stub?: boolean;
  infobox?: Infobox | null;
  lead_image_url?: string;
  lead_image_alt?: string;
  lead_image_caption?: string;
  lead_image_credit?: string;
  lead_image_license?: string;
  lead_image_source_url?: string;
  references?: Reference[];
  /**
   * Submitting this without the right to change it returns a field-level
   * 400 naming the field, not a 403 (DECISIONS §15).
   */
  protection?: ProtectionLevel;
  is_published: boolean;
  comment?: string;
}

/* =====================================================================
   Revisions and history
   ===================================================================== */

/** One row of `GET /api/articles/{slug}/revisions/` (page size 50). */
export interface Revision {
  id: number;
  /** The previous revision in the chain; null on the page creation. */
  parent: number | null;
  editor: Author | null;
  comment: string;
  created_at: string;
  byte_size: number;
  /** Signed. Render with an explicit `+` or U+2212, never a hyphen. */
  byte_delta: number;
  is_minor: boolean;
  is_page_creation: boolean;
  /** Machine strings only: "seed", "revert", "api", "import". */
  tags: string[];
}

/**
 * Everything on a revision that is not a plain column, snapshotted so
 * history can be replayed. Never queried.
 */
export interface RevisionApparatus {
  /** Bumped when the shape changes, so the history viewer can branch. */
  schema: number;
  short_description: string;
  page_type: PageType;
  is_stub: boolean;
  /** Category SLUG, so a mis-click in the admin is recoverable. */
  category: string | null;
  infobox: Infobox | null;
  references: Reference[];
}

/** `GET /api/articles/{slug}/revisions/{id}/`. */
export interface RevisionDetail extends Revision {
  title: string;
  summary: string;
  content: string;
  apparatus: RevisionApparatus;
}

/* =====================================================================
   Diff — a server-rendered opcode stream. The client never diffs.
   ===================================================================== */

export type DiffOpKind = "=" | "+" | "-";

/**
 * `[kind, text]`. Concatenating every `=` and `-` text reproduces the OLD
 * line exactly; every `=` and `+` reproduces the NEW line exactly. That
 * round-trip property is what lets one payload render either side or a
 * unified view.
 */
export type DiffOp = [DiffOpKind, string];

/** `=` context · `~` modified (has word ops) · `+` added · `-` removed. */
export type DiffRowKind = "=" | "~" | "+" | "-";

export interface DiffRow {
  t: DiffRowKind;
  /** 1-based line number in the old document; null where it does not exist. */
  a: number | null;
  /** 1-based line number in the new document; null where it does not exist. */
  b: number | null;
  ops: DiffOp[];
}

export interface DiffHunk {
  a_start: number;
  b_start: number;
  rows: DiffRow[];
}

/** One side of the comparison header. */
export interface DiffSide {
  id: number;
  editor: string | null;
  comment: string;
  created_at: string;
  size: number;
}

export interface DiffStats {
  lines_added: number;
  lines_removed: number;
  lines_changed: number;
  bytes_added: number;
  bytes_removed: number;
}

/** `GET /api/articles/{slug}/diff/?from=&to=` (DECISIONS §14). */
export interface DiffPayload {
  article: { slug: string; title: string };
  /** Null when `from=0`, i.e. the diff is against the empty document. */
  from: DiffSide | null;
  to: DiffSide;
  title_changed: boolean;
  summary_changed: boolean;
  stats: DiffStats;
  /**
   * True when a changed line pair blew the ~4000-token valve and fell back
   * to whole-line ops. Surface it; silently showing a degraded diff is worse.
   */
  truncated: boolean;
  hunks: DiffHunk[];
}

/** Alias for the name used in survey-infra.md §2. Same shape. */
export type DiffResponse = DiffPayload;

/* =====================================================================
   Recent changes / watchlist / contributions (DECISIONS §4)
   =====================================================================
   One row shape, one row component, three feeds. The React key is
   `${kind}-${id}` — `id` is unique only WITHIN a kind, because an edit row
   is a Revision id and a talk row is a TalkMessage id.
   ===================================================================== */

export interface ChangeRow {
  kind: ChangeKind;
  /** Unique only within `kind`. */
  id: number;
  parent_id: number | null;
  timestamp: string;
  article: ArticleStub;
  user: Author | null;
  comment: string;
  /** NULL on talk rows — render the grey em-dash, not a zero. */
  byte_size: number | null;
  /** NULL on talk rows. Signed; prints `+` / U+2212 so colour is never alone. */
  byte_delta: number | null;
  is_minor: boolean;
  is_page_creation: boolean;
  is_bot: boolean;
  /** This revision is still the article's latest. */
  is_current: boolean;
  tags: string[];
  /** NULL on edit rows. */
  thread: TalkThreadStub | null;
}

/**
 * A contributions row is a change row. The alias exists so call sites can
 * say what they mean without a second, drifting shape.
 */
export type Contribution = ChangeRow;

/**
 * `/api/changes/` uses TIMESTAMP CURSOR pagination for every `type` value,
 * including `type=edit`, so the envelope never changes shape. Offset
 * pagination over a merged stream cannot produce an honest `count`.
 */
export interface ChangeFeed {
  results: ChangeRow[];
  /** Pass back as `?before=` to page. Null at the end of the feed. */
  next_before: string | null;
  has_more: boolean;
}

/* =====================================================================
   Talk pages (DECISIONS §12)
   ===================================================================== */

/** The nested thread reference carried by a talk-kind change row. */
export interface TalkThreadStub {
  id: number;
  title: string;
}

export interface TalkThread {
  id: number;
  article: ArticleStub;
  title: string;
  created_by: Author | null;
  created_at: string;
  updated_at: string;
  /** Null until the first message. */
  last_message_at: string | null;
  /** Denormalised; counts non-deleted messages only. */
  message_count: number;
  participant_count: number;
  is_resolved: boolean;
  is_locked: boolean;
}

export interface TalkThreadDetail extends TalkThread {
  messages: TalkMessage[];
}

/**
 * Deletion is soft and the node stays, so replies are not orphaned and the
 * audit trail survives. The SERIALIZER decides what a caller sees: `body`
 * and `author` are both null on a deleted message unless the requester is
 * staff. Render the tombstone, not an empty bubble.
 */
export interface TalkMessage {
  id: number;
  thread: number;
  parent: number | null;
  author: Author | null;
  body: string | null;
  /** 0-based, capped at 4. */
  depth: number;
  created_at: string;
  edited_at: string | null;
  is_deleted: boolean;
}

/** `POST /api/articles/{slug}/talk/`. */
export interface TalkThreadInput {
  title: string;
  body: string;
}

/** `POST /api/talk/threads/{id}/messages/`. */
export interface TalkMessageInput {
  body: string;
  parent?: number | null;
}

/* =====================================================================
   Watchlist (DECISIONS §17)
   ===================================================================== */

/**
 * A private preference, not an event: nothing about watching appears in any
 * feed. The watchlist itself is a filter over changes.
 */
export interface Watch {
  id: number;
  article: ArticleStub;
  created_at: string;
}

/* =====================================================================
   Search and suggest (DECISIONS §2, §3)
   ===================================================================== */

/**
 * `title_snippet` and `snippet` arrive as STRINGS containing literal
 * `<mark>` / `</mark>` tokens, already `html.escape()`d by the backend.
 * The `<Snippet>` component splits on those tokens and builds React
 * elements. It does not parse HTML, and it does not reach for React's
 * raw-HTML escape hatch, which appears nowhere in this app.
 */
export interface SearchResult {
  slug: string;
  title: string;
  title_snippet: string;
  snippet: string;
  rank: number;
  category: CategoryRef | null;
  updated_at: string;
  byte_size: number;
  word_count: number;
}

/**
 * The DRF page envelope plus two top-level keys. `did_you_mean` is present
 * only at zero results.
 */
export interface SearchResponse extends Paginated<SearchResult> {
  query: string;
  did_you_mean: string | null;
}

/** `/api/search/suggest/?q=` — max 10 rows, hard cap. */
export interface Suggestion {
  title: string;
  slug: string;
  /** The GLOSS, not a body snippet. That is what makes the dropdown scannable. */
  short_description: string;
  lead_image_url: string;
  page_type: PageType;
}

/** `GET /api/articles/{slug}/preview/` — the hover card. */
export interface PreviewCard {
  title: string;
  slug: string;
  short_description: string;
  /** Markdown stripped, wikilinks unwrapped, cut on a word boundary at 525 chars. */
  extract: string;
  lead_image_url: string;
  lead_image_alt: string;
  page_type: PageType;
  is_stub: boolean;
}

/* =====================================================================
   Main page (DECISIONS §5)
   =====================================================================
   "In the news" is CUT. A fabricated news feed on an encyclopedia demo
   reads as fake and would be stale the day after it shipped.
   ===================================================================== */

export interface MainPageFeatured extends ArticleStub {
  extract: string;
  /**
   * The thumbnail is the main page's LCP element. These are optional
   * because DECISIONS §5 specifies `{…ArticleStub, extract}`; treat a
   * missing url as "render the extract without a thumbnail".
   */
  short_description?: string;
  lead_image_url?: string;
  lead_image_alt?: string;
  lead_image_caption?: string;
}

/** One "On this day" entry. */
export interface OnThisDayEntry {
  year: number;
  month: number;
  day: number;
  /** Markdown, rendered through the same `skipHtml` pipeline as an article. */
  body: string;
}

export interface MainPage {
  featured: MainPageFeatured;
  recently_featured: ArticleStub[];
  /** Each literally begins "… that" and ends in "?". Markdown strings. */
  dyk: string[];
  otd: OnThisDayEntry[];
  stats: SiteStats;
}

/* =====================================================================
   Site statistics
   ===================================================================== */

export interface SiteStats {
  articles: number;
  categories: number;
  contributors: number;
  total_views: number;
  revisions: number;
  talk_messages: number;
}

/* =====================================================================
   Envelopes and auth
   ===================================================================== */

/**
 * The standard DRF page envelope. Page sizes are fixed per endpoint
 * (DECISIONS §10): 20 for articles and search, 50 for revisions, changes,
 * watchlist and category listings, 10 for suggest.
 */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
  user: User;
}

/** `POST /api/auth/logout/` blacklists the refresh token before storage is cleared. */
export interface LogoutInput {
  refresh: string;
}
