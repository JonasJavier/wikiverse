# Changelog

All notable changes to Wikiverse. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [2.0.0] — 2026-09-27

The encyclopedia release: Wikiverse becomes a working model of a real wiki, with a full seed
corpus, and goes live at [wikiverse.jonasjavier.dev](https://wikiverse.jonasjavier.dev).

### Added
- **Encyclopedia corpus** of 63 articles (~75,000 words) across 16 categories, with infoboxes,
  428 references, lead images from Wikimedia Commons and a deterministic synthesised history of
  338 revisions. 134 red links point at the 57 planned articles.
- **Wiki apparatus**: infoboxes, numbered footnotes with back-links, reference lists, hatnotes,
  stub notices, *See also*, category bars, hover previews and red links.
- **History and diffs**: revision history with byte deltas and flags; server-side, two-stage,
  word-level diffs between any two revisions, side by side or inline.
- **Community**: talk pages with threaded replies, watchlists, per-user contributions, and a
  filterable Recent changes feed with RSS.
- **Search**: PostgreSQL full-text search with weighted ranking, safe highlighted snippets,
  trigram typo tolerance, *did you mean* and a typeahead.
- **Main page** with a featured article, *Did you know…*, *On this day* and site statistics.
- **Encyclopedia interface**: three-column layout with site navigation, table of contents and
  Tools rail; light, dark and system themes; self-hosted typefaces; print stylesheet.
- **SEO**: sitemap, robots.txt, canonical URLs and per-article Open Graph cards served to
  link-preview bots.
- **Operations**: `seed` (idempotent, `--check`, `--epoch`), `seed_e2e`, `ensure_admin` and
  commands to rebuild search vectors, the link graph and counters.
- **Tests**: 333 backend tests, 258 frontend unit tests and 17 Playwright journeys; CI gates for
  migrations, the OpenAPI schema and the corpus.
- **Documentation**: architecture, design decisions, development and deployment guides,
  security policy and contributing guide.

### Changed
- The interface was redesigned from a SaaS-style landing page into a reference work.
- API: flat search endpoints, cursor-paginated feeds, 36 endpoints with an OpenAPI schema that
  builds without warnings.

### Security
- Content Security Policy emitted by both nginx and Django.
- JWT refresh tokens rotate and are blacklisted on use and on logout.
- Login and registration throttles keyed on the username as well as the client address.
- Remote images restricted to Wikimedia hosts.
- The legacy demo superuser is disabled by migration, and the seed no longer creates one.

## [1.0.0] — 2026-06-17

The CS50W wiki rebuilt as a full-stack application: Django REST Framework and PostgreSQL behind
a React, Vite and TypeScript interface, with JWT authentication, revision snapshots, Markdown
editing, categories, Redis caching, Docker Compose and CI.

## [0.1.0] — 2024-04-22

The original Harvard CS50 Web Programming *Wiki* project.

[2.0.0]: https://github.com/JonasJavier/wikiverse/compare/1d7e233...b48231d
[1.0.0]: https://github.com/JonasJavier/wikiverse/commit/1d7e233
[0.1.0]: https://github.com/JonasJavier/wikiverse/commit/f742d43
