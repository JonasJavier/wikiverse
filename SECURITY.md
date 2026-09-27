# Security Policy

Wikiverse is a portfolio project, not a hosted service with customers. It is still built and
reviewed as if it were one, and the notes below describe what is actually true of it rather
than what sounds reassuring.

## Reporting a vulnerability

Open a [private security advisory](https://github.com/JonasJavier/wikiverse/security/advisories/new)
on the repository. Please do not open a public issue for anything exploitable.

Include what you did, what happened, and what you expected. A proof of concept against a local
`docker compose up` is ideal — please do not test against the live site at
`wikiverse.jonasjavier.dev`.

Expect a first response within a week. There is no bounty.

## Known and accepted

**The original demo superuser password is burned.** Early revisions of this repository shipped
a seed that created an `admin` account with a hardcoded password, and that password was also
printed on the login page. Both are gone: the seed no longer creates a superuser at all
(`manage.py ensure_admin` does, from environment variables, generating a random password when
none is supplied), and a data migration disables any pre-existing `admin` superuser. But the
old password is permanently in the git history and must be treated as public. If you ever
deployed an early revision of this project, rotate that account.

**Anyone signed in can edit any unprotected article.** That is the wiki model, on purpose, and
it is the same trade-off Wikipedia makes. Deletion is restricted to the author or staff,
restoring a deleted article is staff-only, and every edit is recorded as an immutable revision
with its author, so nothing is lost and everything is attributable.

**Tokens live in `localStorage`.** This is a JWT SPA without a backend session, so the access
and refresh tokens are reachable by any script running on the origin. The mitigations are that
refresh tokens are rotated and blacklisted on use, refresh lifetime is two days rather than a
week, there is a real logout endpoint that revokes server-side, and the content security policy
below is strict enough that injecting a script is the hard part. A cookie-based session with
CSRF protection would be stronger; it is a deliberate trade for a stateless API.

## What the application does to defend itself

- **No HTML from user content ever reaches the DOM as markup.** `react-markdown` runs without
  `rehype-raw` and with `skipHtml`, and the codebase contains zero uses of
  `dangerouslySetInnerHTML` — including in search results, where highlighted snippets are
  parsed into React elements by splitting on marker tokens rather than by interpreting HTML.
  Server-side, PostgreSQL's `ts_headline` is asked for non-HTML delimiters, the result is
  HTML-escaped, and only then are the delimiters swapped for markup.
- **A content security policy is emitted by Django, not only by nginx.** The API is reachable
  on its own hostname as well as through the frontend proxy, so a header set only at the proxy
  would protect one of the two paths. Both send the same policy.
- **Remote image URLs are allowlisted.** An article's lead image must be hosted on Wikimedia;
  the same list backs the CSP's `img-src`, so an editor cannot point every reader's browser at
  an arbitrary host.
- **Rate limits do not trust `X-Forwarded-For`.** The login and registration throttles key on
  the submitted username as well as the client address, because the API can be reached without
  passing through the proxy that would otherwise normalise that header.
- **Secrets come from the environment.** Nothing is committed; `.env` is ignored and
  `.env.example` carries placeholders only.

## Supported versions

The `main` branch is the only supported version.
