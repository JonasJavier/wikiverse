# Running Wikiverse without Docker

Docker (`docker compose up --build`) is the supported path and needs nothing else installed.
This page is for working on one side at a time with native tooling, which is faster for tight
edit–test loops.

## Prerequisites

- Python 3.12 or newer (CI and the production image use 3.13)
- Node.js 22
- Optionally PostgreSQL 16+ and Redis 7+. Without them the backend falls back to SQLite and an
  in-process cache, and search degrades from full-text ranking to a plain `icontains` match.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python manage.py migrate
python manage.py seed                # 63 articles, ~340 revisions, talk threads, watchlists
DEBUG=true python manage.py runserver
```

With no `DATABASE_URL` the database is `backend/db.sqlite3` — an absolute path, so running
`manage.py` from any directory reaches the same file. To use PostgreSQL instead:

```bash
export DATABASE_URL=postgres://wikiverse:wikiverse@localhost:5432/wikiverse
export REDIS_URL=redis://localhost:6379/0     # optional
```

Settings also read a `.env` file at the repository root. Copy `.env.example`; never commit the
result. If the file holds values for another project, the backend will quietly connect to that
project's database — check it first when something behaves unexpectedly.

### Useful management commands

| Command | What it does |
| --- | --- |
| `seed` | Validate the corpus and seed it. Idempotent: running it twice changes nothing. |
| `seed --check` | Validate the corpus only; writes nothing. |
| `seed --epoch today` | Date the synthesised history so it ends today (default: a fixed date). |
| `seed --flush --force` | Delete every article, revision and talk thread, then reseed. |
| `seed_e2e` | Three small fixture articles for the Playwright suite. |
| `ensure_admin` | Create or update the superuser from `DJANGO_ADMIN_USERNAME` / `DJANGO_ADMIN_EMAIL` / `DJANGO_ADMIN_PASSWORD`; prints a generated password once if none is set. |
| `rebuild_search` | Recompute every article's search vector (PostgreSQL only). |
| `rebuild_links` | Re-derive the wikilink graph, including red links. |
| `rebuild_counts` | Recompute denormalised counters. |

The seed never creates a superuser.

## Frontend

```bash
cd frontend
npm ci
npm run dev          # http://localhost:5173, talks to http://localhost:8000/api
```

Point it at another backend with `VITE_API_URL`, e.g.
`VITE_API_URL=http://localhost:8010/api npm run dev`. The backend's `CORS_ALLOWED_ORIGINS`
must then include the dev server's origin.

## Tests

```bash
# Backend — SQLite by default; set DATABASE_URL to run against PostgreSQL
cd backend && pytest -q

# Frontend unit tests (Vitest + Testing Library)
cd frontend && npm test

# End-to-end (Playwright) — starts its own backend and frontend
cd frontend && npx playwright install chromium && npm run test:e2e
```

Tests that exercise PostgreSQL-only behaviour — the search trigger, trigram typo tolerance —
skip themselves on SQLite and run in CI, which uses PostgreSQL.
