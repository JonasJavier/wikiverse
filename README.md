<div align="center">

# Wikiverse

**An open encyclopedia, built from scratch — revision history, diffs, talk pages, watchlists,
citations, red links and full-text search, without MediaWiki.**

[**wikiverse.jonasjavier.dev**](https://wikiverse.jonasjavier.dev) ·
[API reference](https://wikiverse.jonasjavier.dev/api/docs/) ·
[Design decisions](docs/DECISIONS.md)

[![CI](https://github.com/JonasJavier/wikiverse/actions/workflows/ci.yml/badge.svg)](https://github.com/JonasJavier/wikiverse/actions/workflows/ci.yml)
![Django 5.2](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-full--text-4169E1?logo=postgresql&logoColor=white)
![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey)
![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)

</div>

---

Wikiverse began as the wiki assignment of Harvard's *CS50's Web Programming with Python and
JavaScript* and was later rebuilt as a full-stack product. It is a working model of the
machinery that makes a wiki a wiki: every save is an immutable revision, any two revisions can
be diffed word by word, every article has a talk page, and links to articles nobody has written
yet show up red and open the editor with the title filled in.

It ships with a 63-article general encyclopedia — about 75,000 words across mathematics,
physics, astronomy, chemistry, the life sciences, medicine, the Earth sciences, geography and
computing — with infoboxes, 428 references to published sources and a synthesised edit history
of 338 revisions.

<p align="center">
  <img src="docs/screenshots/article.png" alt="The Entropy article: table of contents on the left, the lead section beside an infobox, and the Tools rail on the right" width="100%">
</p>

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/main-page.png" alt="The main page with the featured article, Did you know and On this day panels"></td>
    <td width="50%"><img src="docs/screenshots/article-dark.png" alt="The Black hole article in the dark theme, with its lead image and licence credit"></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/history.png" alt="A revision history with byte deltas and edit summaries"></td>
    <td><img src="docs/screenshots/search.png" alt="Full-text search results with highlighted snippets"></td>
  </tr>
</table>

## Features

**Reading**
- Article pages in the shape of a reference work: lead section, infobox, lead image with
  licence credit, numbered footnotes that link both ways, references, *See also* and a
  category bar.
- Wikilinks with **hover previews**. Links to planned but unwritten articles render as
  **red links** — 134 of them — exactly as on Wikipedia.
- A sticky table of contents with scroll-spy, a Tools rail (what links here, page
  information, permanent link) and a print stylesheet.
- A main page with a featured article, *Did you know…*, *On this day*, the category tree and
  the latest changes.

**Editing and history**
- Markdown editor with live preview, a structured infobox editor and a reference editor that
  flags dangling and unused citations. Drafts survive a reload.
- Full revision history with byte deltas, minor and bot flags and edit summaries. Pick any two
  revisions for a **server-computed word-level diff**, side by side or inline.
- Page protection levels, soft delete with staff-only restore, and a revert endpoint that
  restores any earlier revision as a new one.

**Community**
- Talk pages with threads and replies.
- **Recent changes**: edits and talk posts in one feed, filterable by type, contributor,
  category, period, minor and bot edits, with every filter in the URL — and an RSS feed.
- Watchlists and per-user contribution histories.

**Search**
- PostgreSQL full-text search with weighted ranking (title, then description, then body),
  highlighted snippets, category and date filters, and *did you mean* suggestions.
- A typeahead combobox with **trigram typo tolerance**. On SQLite everything degrades to
  substring matching, chosen at runtime.

**Sharing and discoverability**
- `sitemap.xml`, `robots.txt`, canonical URLs and per-page metadata.
- **Per-article Open Graph cards on a client-rendered SPA**: nginx routes link-preview bots to a
  Django view that emits `og:*`, Twitter and JSON-LD tags, while people get the SPA.

**Security**
- No user content ever reaches the DOM as HTML. There is no `dangerouslySetInnerHTML` anywhere
  — search highlighting included, which is built from marker tokens rather than markup.
- A strict Content Security Policy emitted by Django *and* nginx, self-hosted fonts, an
  allowlist for remote images, rotating and revocable JWT refresh tokens, and login throttles
  that spoofing `X-Forwarded-For` cannot reset. See [SECURITY.md](SECURITY.md).

## Architecture

```
                 ┌─────────────────────────── Frontend service ───────────────────────────┐
browser ──TLS──▶ │ nginx ─ /             React 19 SPA (Vite, TypeScript, Tailwind CSS v4)  │
                 │       ─ /wiki/<slug>  the SPA for people, an Open Graph page for bots   │
                 │       ─ /api /admin /sitemap.xml /robots.txt ─────────┐                 │
                 └───────────────────────────────────────────────────────│─────────────────┘
                                                                         ▼
                                     Backend service: gunicorn · Django 5.2 · DRF
                                            │                          │
                                     PostgreSQL 16+                  Redis
                         tsvector + GIN · pg_trgm · unaccent    cache · throttles
```

```
backend/
  apps/articles/     models, API, search, diff engine, markup parser, seed corpus
  apps/accounts/     custom user, JWT auth, profiles
  apps/common/       security middleware, SEO views, sitemaps, throttling, pagination
  config/            12-factor settings
frontend/
  src/pages/         one component per route
  src/components/    article apparatus, history and diff, community, editor, layout, UI
  src/api/           TanStack Query hooks, one module per domain
  e2e/               Playwright journeys
docs/                the API/UI contract, development and deployment guides
```

Three decisions worth knowing about, all recorded in [docs/DECISIONS.md](docs/DECISIONS.md):

- **The search vector is maintained by a PostgreSQL trigger**, weighted across title,
  description and body, so no code path can forget to update it.
- **Diffs are computed on the server** in two stages: lines, then words inside changed lines.
  The same opcode stream feeds the diff page and the byte deltas in every feed.
- **The seed is deterministic.** Edit histories derive from a hash of each title, so seeding
  twice produces identical data.

## Quick start

Docker is the only prerequisite.

```bash
git clone https://github.com/JonasJavier/wikiverse.git
cd wikiverse
docker compose up --build
```

This starts PostgreSQL, Redis, the API with hot reload and the Vite dev server, applies the
migrations and seeds the corpus.

| | URL |
| --- | --- |
| Encyclopedia | http://localhost:5173 |
| API | http://localhost:8000/api/ |
| Interactive API docs | http://localhost:8000/api/docs/ |
| Django admin | http://localhost:8000/admin/ (create the account with `manage.py ensure_admin`) |

If a port is taken, set `POSTGRES_PORT`, `REDIS_PORT`, `BACKEND_PORT` or `FRONTEND_PORT` in
`.env`, copied from `.env.example`. To work without Docker, see
[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md). For a production-like stack behind nginx, run
`docker compose -f docker-compose.prod.yml up --build -d`.

## Quality gates

CI runs every one of these on each pull request, with the backend suite on PostgreSQL.

```bash
# Backend
cd backend
ruff check . && ruff format --check .
python manage.py makemigrations --check --dry-run
python manage.py spectacular --fail-on-warn --file schema.yml
pytest -q

# Frontend
cd frontend
npx tsc -b
npm run lint            # zero warnings allowed
npm test                # Vitest and Testing Library
npm run build
npm run test:e2e        # Playwright: read, search, history and diff, edit, talk
```

## API

Thirty-six endpoints, all described by an OpenAPI schema with no warnings. A selection:

| Endpoint | |
| --- | --- |
| `GET /api/articles/{slug}/` | Article with infobox, references, categories and link targets |
| `GET /api/articles/{slug}/revisions/` | Revision history |
| `GET /api/articles/{slug}/diff/?from=&to=` | Word-level diff between two revisions |
| `GET /api/articles/{slug}/backlinks/`, `/info/`, `/preview/` | What links here, page information, hover card |
| `GET` `POST /api/articles/{slug}/talk/` | Talk threads |
| `GET /api/search/?q=`, `/api/search/suggest/?q=` | Full-text search and typeahead |
| `GET /api/changes/`, `/api/feeds/changes.rss` | Recent changes as JSON and RSS |
| `GET /api/watchlist/`, `POST` `DELETE /api/articles/{slug}/watch/` | Watchlist |
| `GET /api/main-page/` | Featured article, *Did you know*, *On this day*, statistics |
| `POST /api/auth/register/`, `login/`, `refresh/`, `logout/` | JWT auth with refresh rotation and revocation |

The full reference lives at [`/api/docs/`](https://wikiverse.jonasjavier.dev/api/docs/).

## Deployment

The live site runs on Railway as two Docker services with managed PostgreSQL and Redis, and
deploys on every push to `main`. Configuration, seeding and the release checklist are in
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The 57 planned articles that are still red links are
listed in [docs/content-plan.json](docs/content-plan.json); writing one is a self-contained
contribution.

## Licence

The code is released under the [MIT licence](LICENSE). The article text of the seed corpus is
licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); images come from
Wikimedia Commons under the licences named in their credit lines.

Wikiverse is an independent project and is not affiliated with Wikipedia or the Wikimedia
Foundation.
