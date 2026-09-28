# Working on Wikiverse as an agent

Read this first. It tells you where each fact lives so you can find it without reading whole
files. Save tokens by being precise, not by skipping steps: locate code through the graph, then
read the exact source before you assert anything or edit it.

## 1. Find code through the knowledge graph

This repo is indexed with **codebase-memory-mcp**. Run `list_projects` and pick the project whose
`root_path` is this checkout. If its `head_sha` is not `git rev-parse HEAD`, re-index first with
`index_repository(mode="moderate")`.

| You need | Use |
| --- | --- |
| Where a function, class or component is defined | `search_graph(query=…)` or `search_graph(name_pattern=…)` |
| The source of one symbol | `get_code_snippet(qualified_name)`, not a whole-file read |
| Who calls what | `trace_path(function_name, mode="calls")` |
| A text pattern, grouped by function | `search_code(pattern, mode="compact")`; `mode="files"` for paths only |
| Structure and hotspots | `get_architecture(aspects=["overview"])` |

Graph `Route` nodes include URLs taken from tests. For the real API surface use the OpenAPI
schema (section 2).

## 2. Where facts live, and the cheap way to get them

| Fact | Cheapest reliable source |
| --- | --- |
| API endpoints (36 paths) | `python manage.py spectacular --format openapi-json` (prints to stdout), or `GET /api/schema/?format=json` on a running stack. List `paths` with a short script instead of reading the YAML. |
| Frontend routes | the route table in `frontend/src/App.tsx`: `grep -n "path:" frontend/src/App.tsx` |
| API ↔ UI contract (field names, URLs, literals) | `docs/DECISIONS.md`. Run `grep -n "^## " docs/DECISIONS.md` and read only the section you need. |
| How a subsystem works | `docs/ARCHITECTURE.md`, one section at a time (same `grep -n "^## "` approach) |
| Corpus counts (articles, modules, rules) | `python manage.py seed --check` (writes nothing) |
| Test totals | the latest CI run: `gh run view <id> --log \| grep -E "passed\|Tests "` |
| Exact dependency versions | `frontend/package-lock.json` through `node -e` (never read it whole); `pip freeze` in the backend environment |
| Settings and environment variables | `grep -n "env(" backend/config/settings.py` |
| Deploy topology | `docs/DEPLOYMENT.md` |

## 3. Never read these whole

| Path | Why | Instead |
| --- | --- | --- |
| `backend/apps/articles/management/commands/_seed_data/` | 2.5 MB of article text | `seed --check`, or a small Python script that imports `ARTICLES` and prints only the fields you need |
| `docs/content-plan.json` | about 2,100 lines | `python -c` / `jq` for the keys you need |
| `frontend/package-lock.json` | lockfile | `node -e` lookup per package |
| `backend/apps/articles/views.py` (1.7k lines), `serializers.py`, `models.py` (~900 each) | large | `get_code_snippet` for the symbol |
| `frontend/dist/`, `node_modules/`, `db.sqlite3`, `.venv/` | build output and dependencies | nothing to read |
| `.env` | holds secrets, and may point at another project's database | `.env.example` for variable names |

## 4. Working habits that save tokens without losing quality

- **One subagent at a time, and only for a real fan-out.** Do not run agents in parallel. Do not
  repeat a search a subagent is already doing.
- **Batch shell work.** One command that prints several facts beats several round trips.
  Trim output with `head`, `grep` or `wc -l`.
- **Verify pages with text first.** In a browser use `get_page_text`, `read_page` or a
  `javascript_tool` check before screenshots. Take screenshots at `scale: 0.5` unless you
  need detail.
- **Do not re-read a file you just edited.** The edit tool already fails if the change did not
  apply.
- **Keep counts in one place.** The README's numbers (articles, tests, endpoints) come from the
  commands above. Re-derive them when they matter; do not copy them from older documents.

## 5. Guardrails

- Other sessions may switch the branch of this checkout. For long runs, work in a `git worktree`
  or on a `git archive` export.
- Docker: `docker-compose.prod.yml` does not set `BACKEND_ORIGIN`, and the frontend image
  defaults it to the Railway backend. A local production-like stack therefore needs
  `BACKEND_ORIGIN=http://backend:8000` and `BACKEND_HOST=backend` on the `frontend` service, or
  its `/api` calls go to production.
- Never create a superuser from the seed. `ensure_admin` reads the credentials from the
  environment.
- Quality gates and non-negotiable rules are in `CONTRIBUTING.md`. The security model is in
  `SECURITY.md`.
