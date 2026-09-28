# Wikiverse — NORMATIVE DECISIONS (v1)

This file is the **single source of truth**. The blueprint produced five specification
documents that contradict each other in 35 places (`critique.md`). Where this file and any
other document disagree, **this file wins, always, without exception**. Do not "reconcile"
by picking the other document; do not re-litigate a decision here. If something is genuinely
not covered here, follow `design-backend.md` for the API, `design-ui.md` for the interface,
and say in your report that you had to.

Names in this file are exact. Copy them character for character: field names, URL paths,
query parameters, CSS custom properties, anchor id formats and string literals are all part
of the contract, because a test in another agent's work asserts them.

---

## 0. Hard invariants

1. `ruff check .` and `ruff format --check .` must pass in `backend/`.
2. `npx tsc -b` and `npm run lint` must pass in `frontend/`, with `--max-warnings=0`.
3. Everything must work on **both** SQLite and PostgreSQL. Postgres-only features
   (`tsvector`, `pg_trgm`, `SearchHeadline`) must degrade to an `icontains` path, chosen at
   runtime with `connection.vendor == "postgresql"`, never at import time.
4. **No `dangerouslySetInnerHTML` anywhere in the frontend.** There is no exception.
5. `react-markdown` is used **without** `rehype-raw` and **with** `skipHtml`, for article
   bodies, talk messages, infobox values and reference titles alike.
6. Every migration must apply cleanly to a database that already holds the 12 legacy
   articles, and to a completely empty one.
7. No credential, token or DSN in source. Everything from env.

---

## 1. Infobox (resolves critique #1)

The **backend schema is normative**. The infobox never carries an image.

```python
# apps/articles/infobox.py — the ONLY valid shape
{
  "title": str,            # optional; defaults to the article title
  "subtitle": str,         # optional
  "rows": [
    {"kind": "header", "value": str},           # a section break inside the box
    {"kind": "row", "label": str, "value": str},
    {"kind": "full", "value": str},             # full-width cell, no label
  ],
}
```

* `value` is **always a plain string**. It may contain `[[Article Title]]` wikilinks,
  `*emphasis*`, and `[^refkey]` footnote markers; the renderer resolves those. There are no
  object or array values. `header` rows carry `value`, **not** `label`.
* The lead image lives on **`Article` columns**, never inside `infobox`:
  `lead_image_url`, `lead_image_alt`, `lead_image_caption`, `lead_image_credit`,
  `lead_image_license`, `lead_image_source_url`.
* `Infobox.tsx` renders the credit line whenever `lead_image_credit` is non-empty. It is not
  optional — it is the attribution requirement.
* SEO reads `article.lead_image_url`. Not `infobox.image`, not `infobox.image_url`.

## 2. Search and suggest URLs (resolves critique #2, #4, #30)

Canonical, flat, and the only paths that exist:

| Path | Purpose |
| --- | --- |
| `GET /api/search/?q=` | Full results page |
| `GET /api/search/suggest/?q=` | Typeahead, **max 10**, also serves 404-page "similar titles" |

There is **no** `/api/articles/search/` and **no** `/api/articles/suggest/`. Keep `search`
and `suggest` in `RESERVED_SLUGS`. There is no separate `/api/search/similar/` — the 404 page
calls `suggest`.

`SearchResultSerializer` returns exactly:

```
slug, title, title_snippet, snippet, rank, category, updated_at, byte_size, word_count
```

plus a **top-level** `did_you_mean` on the response envelope. Date filters are
`created_after` and `created_before`. The sort control offers **relevance | newest | oldest**
only — "most edited" is cut.

The frontend uses a dedicated `useSearch` hook against `/api/search/`. It must **not** reuse
`useArticles`.

## 3. Snippet rendering — safe by construction (resolves critique #5)

Backend: `SearchHeadline(..., start_sel="\x02", stop_sel="\x03")`, then `html.escape()` the
result, then replace `\x02` → `<mark>` and `\x03` → `</mark>`. Never let `ts_headline` emit
raw HTML.

Frontend: a `<Snippet text={...} />` component **splits the string on the literal
`<mark>`/`</mark>` tokens and builds React elements**. It does not parse HTML and it does not
use `dangerouslySetInnerHTML`. Same component for `snippet` and `title_snippet`.

## 4. Recent changes row (resolves critique #3, #22, #24)

`ChangeRowSerializer` field names are normative; the UI adopts them verbatim:

```
kind            "edit" | "talk"
id              int          (unique only within kind)
parent_id       int | null
timestamp       ISO string
article         { slug, title }
user            { id, username, avatar } | null
comment         string
byte_size       int | null   (null on talk rows)
byte_delta      int | null   (null on talk rows)
is_minor        bool
is_page_creation bool
is_bot          bool
is_current      bool         (this revision is still the article's latest)
tags            string[]
thread          { id, title } | null   (null on edit rows)
```

React key is `` `${kind}-${id}` ``. The same row component serves Recent changes, Watchlist
and Contributions.

URL → query mapping for `/changes` (the URL is the source of truth):

| URL param | API param | Default |
| --- | --- | --- |
| `type` | `type` | `all` |
| `user` | `user` | — |
| `category` | `category` | — |
| `hideMinor=1` | `minor=0` | off |
| `hideBot=1` | `bots=0` | off |
| `days=N` | `since=<now-N days>` | `7` |
| `limit` | `limit` | `50` |

`/api/changes/` fetches `limit + 1` rows from **each** side before merging. The envelope is
`{results, next_before, has_more}` and needs an explicit
`@extend_schema(responses=ChangeFeedSerializer)` so `spectacular --fail-on-warn` passes.

## 5. Main page (resolves critique #6)

Ship a `MainPageBlock` model and `GET /api/main-page/`.

```python
MainPageBlock(
  kind,            # "featured" | "dyk" | "otd"
  position,        # int, ordering within kind
  body_markdown,   # for dyk/otd
  article,         # FK, nullable — set for "featured"
  event_year,      # int, nullable — for "otd"
  event_month,     # int, nullable
  event_day,       # int, nullable
)
```

**"In the news" is cut.** A fabricated news feed on an encyclopedia demo reads as fake, and
it would be stale the day after it ships. The main page has: Featured article, Did you
know…, On this day, Browse by category, Recent changes, Site statistics.

`GET /api/main-page/` returns
`{featured: {…ArticleStub, extract}, recently_featured: [ArticleStub], dyk: [string],
otd: [{year, month, day, body}], stats: SiteStats}`, cached in Redis.

## 6. Search vector and text config (resolves critique #7)

* The trigger builds the vector from `title` (A), `short_description` + `summary` (B),
  `content` (C), and fires on `UPDATE OF title, short_description, summary, content`.
  Missing `short_description` from either list is the bug this decision exists to prevent.
* Migration always creates a text search config named **`wikiverse_english`**. When
  `unaccent` is available it includes the unaccent mapping; when it is not, it is a plain
  `COPY = pg_catalog.english`. The name therefore always resolves and `settings.SEARCH_CONFIG`
  is always valid.
* Add a `django.core.checks` check asserting
  `SELECT 1 FROM pg_ts_config WHERE cfgname = settings.SEARCH_CONFIG`.
* Railway's Postgres 18.6 has `pg_trgm` 1.6, `unaccent` 1.1, `btree_gin` and `fuzzystrmatch`
  available, and the app connects as a superuser — **verified**, so `CREATE EXTENSION` in a
  migration will succeed. Still wrap it so SQLite and a non-superuser both no-op cleanly.

## 7. Auth and content security (resolves critique #8, #31)

1. Add `rest_framework_simplejwt.token_blacklist` to `INSTALLED_APPS`, set
   `BLACKLIST_AFTER_ROTATION = True`, and `REFRESH_TOKEN_LIFETIME = timedelta(days=2)`.
2. Add `POST /api/auth/logout/` taking `{refresh}` and blacklisting it. `useAuthStore.logout()`
   calls it before clearing storage.
3. Emit security headers from **Django middleware**, not only from nginx — the backend is
   publicly reachable at its own `*.up.railway.app` host, so an nginx-only header protects
   just one of the two live paths. CSP:
   `default-src 'self'; img-src 'self' https://upload.wikimedia.org https://commons.wikimedia.org data:; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://*.sentry.io; frame-ancestors 'none'; base-uri 'self'`
4. `lead_image_url` is validated server-side against that same host allowlist, in
   `ArticleWriteSerializer` **and** in the corpus validator.
5. `NUM_PROXIES = 1`. Additionally, the `login` and `register` throttles key on the submitted
   username as well as the IP, so the direct-path `X-Forwarded-For` trick cannot reset them.
6. Self-host the two webfonts under `frontend/public/fonts/` and drop the Google Fonts
   `<link>`. It removes a third-party origin, removes two preconnects, and kills the
   render-blocking request — and it makes the CSP above tight.

## 8. Legacy data and the burned admin password (resolves critique #9)

* `manage.py seed` refuses to run when it detects pre-cutover content, printing the exact
  recovery command. `seed --flush --force` wipes and reseeds.
* Ship `manage.py ensure_admin`, which creates or updates the superuser from
  `DJANGO_ADMIN_USERNAME` / `DJANGO_ADMIN_EMAIL` / `DJANGO_ADMIN_PASSWORD`. If the password
  env var is absent it generates a random one and prints it **once**. The seed never creates
  a superuser.
* Data migration `accounts/0003_revoke_legacy_admin`: for a user named `admin` that is a
  superuser and was created before the cutover, call `set_unusable_password()` and clear
  `is_staff` / `is_superuser`.
* Remove the demo credentials printed in `LoginPage.tsx`. `SECURITY.md` records that
  `adminpass123` is in git history and is permanently burned.

## 9. Category colour and chips (resolves critique #11)

`Category.color` stays a **hex string** (the taxonomy already carries muted hex values that
work in both themes). But the chip **never puts text on the category colour**: the colour is
rendered as a 6px leading bar or a small dot, with the label in normal ink. This removes the
contrast problem structurally instead of policing it with a gate, and it looks more like a
reference work than a pill-shaped SaaS tag.

## 10. Pagination sizes (resolves critique #16)

| Endpoint | Page size |
| --- | --- |
| `/api/articles/`, `/api/search/` | **20** |
| `/api/articles/{slug}/revisions/` | **50** |
| `/api/changes/`, `/api/watchlist/` | **50** |
| category article listing | **50** |
| `/api/search/suggest/` | **10** (hard cap) |

`max_page_size` stays 100. UI labels read "Previous 20" / "Next 20" and
`Results {start}–{end} of {count}` with an en dash.

## 11. References (resolves critique #18)

Model fields are normative: `key, order, title, url, authors, publisher, published_on`
(free-text `CharField`), `accessed_on` (`DateField`), `identifier` (one field: "ISBN / DOI /
arXiv"), `quote`.

The in-text marker is **`[^key]`** everywhere — corpus, validator, renderer and the editor's
insert button. `[ref:key]` does not exist. The rendered citation prefix-sniffs `identifier`
to label it `doi:` / `ISBN` / `arXiv:`.

## 12. Talk pages (resolves critique #19, #22)

* Talk markdown goes through the same renderer as articles: no raw HTML, `skipHtml`.
* `TalkThread` denormalises `message_count`, `participant_count` and `last_message_at`,
  all maintained by `touch()`.
* **The Subscribe button is cut** — there is no subscription model and a dead button is worse
  than no button.

## 13. Categories per article (resolves critique #23)

Add `Article.extra_categories = ManyToManyField(Category, related_name="secondary_articles",
blank=True)`. `ArticleDetailSerializer` exposes `categories[]` with the primary FK first.
`SeedArticle` gains a `categories` key (list of extra category names, primary stays in
`category`). The category footer bar is one of the elements that carries the encyclopedia
effect, so it gets real data rather than a single-item list.

## 14. Exact string literals (resolves critique #15)

| Thing | Value |
| --- | --- |
| Document title | `` `${page} — Wikiverse` `` (em dash) |
| Default title | `Wikiverse — the open encyclopedia` |
| Footnote note id | `cite_note-{key}` |
| Footnote backref id | `cite_ref-{key}-{n}` |
| Red link target | `/new?title=<Title>` |
| RSS feed | `/api/feeds/changes.rss` |
| Diff route | `/wiki/:slug/diff?from=<id>&to=<id>` |
| Diff API | `GET /api/articles/{slug}/diff/?from=&to=` |

## 15. Permissions (resolves critique #25, #26)

* `POST /api/articles/{slug}/restore/` uses `permission_classes=[permissions.IsAdminUser]`
  and queries an explicitly unfiltered queryset.
* Submitting `protection` or `is_published` without the right to change it returns
  **400**, field-level, naming the field. Not 403.

## 16. Sitemap and Open Graph (resolves critique #14, #28)

* `ArticleSitemap.items()` is `filter(is_published=True, is_deleted=False)` and excludes
  nothing else. `protocol` derives from `settings.PUBLIC_BASE_URL`.
* **Per-article Open Graph ships.** It is an explicit owner goal and the only honest way to
  deliver it on a client-rendered SPA is the crawler shell: `map $http_user_agent $is_crawler`
  in `nginx.conf.template`, routing crawler requests for `/wiki/<slug>` to a Django
  `TemplateView` that emits `og:*`, `twitter:*`, `<link rel=canonical>`, JSON-LD and a
  `<meta http-equiv="refresh">` back to the SPA. Humans never see it.

## 17. Extra endpoints (resolves critique #30, #21)

* `GET /api/articles/{slug}/info/` — page information: byte size, word count, revision count,
  contributor count, watcher count, created/updated, protection.
* `GET /api/articles/{slug}/backlinks/` — what links here.
* `POST` / `DELETE /api/articles/{slug}/watch/` and `GET /api/watchlist/`.
* `GET /api/users/{username}/contributions/`.

## 18. Housekeeping

* `Revision` declares `objects = RevisionQuerySet.as_manager()` (critique #13).
* `pyproject.toml` `[tool.coverage.run] omit` gains `"*/_seed_data/*"` (critique #17).
* `buttonVariants` moves to `frontend/src/components/ui/buttonVariants.ts` (critique #10).
* Content licence CC BY 4.0 is scoped to
  `backend/apps/articles/management/commands/_seed_data/**`, declared in its `__init__.py`
  (critique #29).
* `requirements.txt` relaxes DRF to `>=3.16,<3.18` so the declared range matches what is
  actually installed and tested.
* `settings.py` default database becomes an **absolute** path:
  `f"sqlite:///{BASE_DIR / 'db.sqlite3'}"`. Today `sqlite:///db.sqlite3` is CWD-relative, so
  running `manage.py` from `backend/` silently creates a second, empty database — confirmed
  in this session.
* `scroll-behavior: smooth` is **removed** (it fights focus management and hurts the
  footnote jump); footnote and TOC navigation scroll programmatically with
  `behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"`.
* Nine throttle scopes exist and all nine are env-overridable:
  `anon, user, search, suggest, preview, diff, write, login, register`.
* `manage.py seed_e2e` ships, creating 1 category and exactly these slugs:
  `e2e-read-me`, `e2e-edit-me`, `e2e-talk-me`, each with 2 revisions, no superuser.

---

## 19. The seed corpus contract — FROZEN

Content authors write against this and nothing else. The backend must conform to it.

Layout: `backend/apps/articles/management/commands/_seed_data/<domain>.py`, each exporting
`ARTICLES: list[SeedArticle]`. `__init__.py` aggregates them and carries the CC BY 4.0 header.

```python
SeedArticle = {
    "title": str,                 # exact title from the taxonomy
    "category": str,              # exact primary category name from the taxonomy
    "categories": list[str],      # extra categories, may be []
    "short_description": str,     # <= 90 chars, no final period; the hover-preview tagline
    "summary": str,               # 1-2 sentences, <= 300 chars; card + search + meta description
    "content": str,               # Markdown body — see the markup rules below
    "tier": str,                  # "feature" | "standard" | "stub"
    "kind": str,                  # concept|person|place|work|period|discipline|disambiguation
    "infobox": dict | None,       # the §1 shape
    "image": {                    # or None
        "url": str,               # MUST be on upload.wikimedia.org or commons.wikimedia.org
        "alt": str,
        "caption": str,
        "credit": str,
        "license": str,           # e.g. "CC BY-SA 4.0", "Public domain"
        "source_url": str,
    } | None,
    "references": [
        {
            "key": str,           # short slug, unique within the article, e.g. "curie1903"
            "title": str,
            "url": str,
            "authors": str,
            "publisher": str,
            "published_on": str,  # free text, e.g. "1903" or "March 2019"
            "accessed_on": str,   # ISO date "YYYY-MM-DD"
            "identifier": str,    # "doi:10.1234/x", "ISBN 978-...", "arXiv:1234.5678", or ""
            "quote": str,         # may be ""
        },
    ],
    "see_also": list[str],        # titles in the corpus
    "aliases": list[str],         # redirect sources pointing at this article
    "is_stub": bool,
    "is_disambiguation": bool,
    "tags": list[str],
}
```

### Markup rules inside `content`

* **No `# H1`.** The page renders the title; a body H1 duplicates it. Start at `##`.
* Internal links: `[[Exact Article Title]]` or `[[Exact Article Title|display text]]`.
  Every target must be a title in **`taxonomy.json`** — that is the link universe, not the set
  of articles that happen to exist. A target outside the taxonomy is a build failure.

### RED LINKS (amended 2026-09-27 — read this carefully)

The corpus ships with **63 of the 120 planned articles**. Authoring of the remaining 57 was
deliberately stopped by the owner and will resume later. This is not a defect to work around:

* A `[[link]]` to a planned-but-unwritten title is a **red link**, exactly as on Wikipedia.
  `validate_corpus` must ACCEPT it. It fails only on a target that is in neither the corpus
  nor `taxonomy.json`.
* The seed records those as `ArticleLink` rows with `to_article = NULL` and `to_title` set, so
  "what links here" and the red-link count both work the day the article is written.
* The renderer gives a red link the `.is-redlink` treatment and points it at
  `/new?title=<Title>`, so a reader can start the missing article in one click.
* `see_also` entries pointing at unwritten titles are kept and rendered as red links too.
* Nothing may assume the corpus is exactly 120 articles. Counts come from the data.
* Footnotes: `[^refkey]` inline, where `refkey` matches a `references[].key`. Every
  reference should be cited at least once; every marker must resolve.
* The **first sentence is bold and restates the title**: `**Photosynthesis** is the process…`
* Sections in encyclopedic order. End feature and standard articles with `## See also`
  (rendered from `see_also`, so do not hand-write the list) — the body ends before it.
  Do not hand-write a `## References` section either; it is rendered from `references`.
* Tables, blockquotes and fenced code are fine. No raw HTML — it will be stripped.
* Write in neutral, encyclopedic, third-person English. No second person, no "we", no
  marketing voice, no emoji.
* Everything must be factually accurate. Prefer settled, well-documented material. Any
  claim carrying a `[^ref]` must actually be supported by that source.

### Revision history

The seed **synthesizes** history; authors do not write it. Each article gets between 2 and 9
revisions with plausible edit summaries, derived deterministically from the title so reseeding
is idempotent. No `Date.now()`-style nondeterminism anywhere in the seed.
