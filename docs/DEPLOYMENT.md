# Deployment

The live site is <https://wikiverse.jonasjavier.dev>, hosted on Railway. Every push to `main`
builds and deploys both services from this repository.

## Topology

```
browser ──TLS──▶ Frontend (nginx) ──┬── /            SPA (static, hashed assets)
                                    ├── /wiki/<slug>  SPA for people, Open Graph shell for link-preview bots
                                    └── /api /admin /static /robots.txt /sitemap.xml
                                          │
                                          ▼
                                   Backend (gunicorn + Django) ──▶ PostgreSQL
                                                               └──▶ Redis
```

| Service | Built from | Notes |
| --- | --- | --- |
| Frontend | `frontend/Dockerfile`, target `prod` | nginx renders `nginx.conf.template` at start with `BACKEND_ORIGIN` / `BACKEND_HOST` |
| Backend | `backend/Dockerfile` | `entrypoint.sh` waits for Postgres, migrates, collects static, then starts gunicorn |
| PostgreSQL | Railway template | `pg_trgm`, `unaccent`, `btree_gin` are created by migration `articles.0003` |
| Redis | Railway template | cache, throttling counters, main-page and suggest caches |

The backend is also reachable on its own `*.up.railway.app` host. That is why security headers
and the CSP are emitted by Django as well as by nginx, and why the login throttles key on the
username and not only on the client address.

Both web services sleep when idle, so the first request after a quiet period takes a few
seconds.

## Configuration

Variable **names** only; values live in the Railway dashboard and nowhere else.

**Backend**

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret. Required. |
| `DATABASE_URL` | Reference to the Postgres service. |
| `REDIS_URL` | Reference to the Redis service. |
| `DEBUG` | `false` in production. |
| `ALLOWED_HOSTS` | The custom domain, the backend's Railway host and `healthcheck.railway.app`. |
| `CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS` | The public origins of the frontend. |
| `DJANGO_SEED` | Leave `false`; seed explicitly (below). `true` reseeds on every boot. |
| `DJANGO_COLLECTSTATIC` | `true`. |
| `WEB_CONCURRENCY` | gunicorn workers. |
| `PUBLIC_BASE_URL`, `PUBLIC_SITE_DOMAIN` | Optional; default to the live domain. Used for sitemap, feeds and Open Graph URLs. |
| `SENTRY_DSN` | Optional; error reporting is a no-op without it. |
| `DJANGO_ADMIN_USERNAME`, `DJANGO_ADMIN_EMAIL`, `DJANGO_ADMIN_PASSWORD` | Read by `ensure_admin` only. |
| `THROTTLE_*`, `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS` | Optional overrides. |

**Frontend**

| Variable | Purpose |
| --- | --- |
| `VITE_API_URL` | Build-time. `/api`, so the SPA calls its own origin and the strict `connect-src 'self'` holds. |
| `BACKEND_ORIGIN`, `BACKEND_HOST` | Runtime, read by nginx. Default to the current backend host in the Dockerfile; set them if the backend service is renamed. |

## Releasing

1. Merge to `main`. CI runs the backend (ruff, migrations check, OpenAPI check, pytest on
   PostgreSQL), the frontend (types, lint, unit tests, build) and the Playwright journeys.
2. Railway builds both images and deploys them; migrations run as the backend boots.
3. Verify content, not just health — a green health check once hid an empty database:

   ```bash
   curl -s https://wikiverse.jonasjavier.dev/api/health/
   curl -s https://wikiverse.jonasjavier.dev/api/stats/
   ```

## Seeding production

Production content is seeded once, by hand, rather than on boot:

```bash
railway ssh --project <project-id> --environment production --service Backend \
  python manage.py seed --epoch today
```

`--epoch today` ends the synthesised edit history on the day of seeding, so Recent changes has
entries in its default seven-day window. The command is idempotent and refuses to overwrite
content it did not create.

## Admin account

The seed never creates a superuser. Set `DJANGO_ADMIN_USERNAME`, `DJANGO_ADMIN_EMAIL` and
`DJANGO_ADMIN_PASSWORD` on the Backend service, then run `python manage.py ensure_admin` the
same way as the seed. Without `DJANGO_ADMIN_PASSWORD` it generates one and prints it once to
the terminal that ran it.
