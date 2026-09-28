# Contributing to Wikiverse

Thanks for looking. This is a personal portfolio project, so the bar for merging is "does it
make the project better and does it keep every gate green" rather than a formal process.

## Getting it running

Docker is the only prerequisite:

```bash
git clone https://github.com/JonasJavier/wikiverse.git
cd wikiverse
docker compose up --build
```

If a port is already taken on your machine, override it rather than editing the compose file —
`POSTGRES_PORT`, `REDIS_PORT`, `BACKEND_PORT` and `FRONTEND_PORT` all read from `.env`. This
matters more than it sounds: when a published port is already in use, Docker does not fail
loudly. The container starts, the other service keeps answering, and you get a confusing
authentication error instead of a bind error.

Running without Docker is documented in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## The gates

Everything below must pass before a pull request is merged. CI runs all of it.

```bash
# Backend
cd backend
ruff check . && ruff format --check .
pytest -q
python manage.py makemigrations --check --dry-run
python manage.py spectacular --fail-on-warn --file /dev/null
python manage.py seed --check

# Frontend
cd frontend
npx tsc -b
npm run lint      # runs with --max-warnings=0
npm test          # Vitest
npm run build
npm run test:e2e  # Playwright; starts its own backend and frontend
```

Two of these catch mistakes that are easy to make and hard to spot:
`makemigrations --check` fails when a model change has no migration, and `spectacular
--fail-on-warn` fails when an endpoint is not describable, which is usually a sign the
serializer is doing something surprising.

## Rules that are not negotiable

These exist because breaking them has real consequences, not because of taste:

- **No `dangerouslySetInnerHTML`, anywhere.** Article bodies, talk messages, infobox values and
  search snippets are all user-authored. Search snippets arrive as strings containing marker
  tokens; split on the tokens and build React elements.
- **`react-markdown` without `rehype-raw`, with `skipHtml`.** Same reason.
- **Everything must work on SQLite and PostgreSQL.** Full-text search, trigram matching and
  `SearchHeadline` are PostgreSQL-only; select the path at runtime with
  `connection.vendor == "postgresql"`, never at import time. The test suite runs on SQLite
  locally and on PostgreSQL in CI; PostgreSQL-only tests skip themselves on SQLite.
- **No secrets in source.** Everything reads from the environment with a safe default.
- **Design tokens live in `frontend/src/index.css`.** There is no `tailwind.config.js` and
  there should not be one — this project uses Tailwind v4's CSS-first configuration. Do not
  hardcode a colour.

[docs/DECISIONS.md](docs/DECISIONS.md) is the normative contract for anything where the backend
and the frontend have to agree: field names, URL paths, query parameters, anchor id formats.
If you are changing one side of a contract, change that file in the same pull request.

## Adding articles to the seed corpus

The encyclopedia ships with 63 of a planned 120 articles. The remaining titles already exist in
[docs/content-plan.json](docs/content-plan.json) and are what the red links throughout the site
point at, so adding one is a self-contained contribution.

Articles live in `backend/apps/articles/management/commands/_seed_data/` as Python modules that
export an `ARTICLES` list. The exact shape is section 19 of `docs/DECISIONS.md`, and
`manage.py seed --check` validates the whole corpus against it — dangling footnotes, infoboxes
that do not match the schema, links outside the plan and uncited references are all build
failures.

Two things the validator cannot check, which matter more than the ones it can:

- **Everything must be factually correct.** Dates, quantities, attributions. If you are not
  sure, leave the claim out.
- **Citations must be real.** A plausible-looking DOI or ISBN that does not resolve is worse
  than no citation, because it looks like diligence. If you cannot verify a source, drop it.

The corpus is licensed CC BY 4.0, separately from the MIT-licensed code.

## Commits and pull requests

Conventional-ish prefixes (`feat:`, `fix:`, `docs:`, `chore:`, `content:`) and a message that
explains *why*, since the diff already shows *what*. Keep a pull request to one concern.
