## What and why

<!-- What changes, and what problem it solves. The diff shows what; explain why. -->

## Gates

- [ ] `ruff check .` and `ruff format --check .`
- [ ] `pytest -q`
- [ ] `python manage.py makemigrations --check --dry-run`
- [ ] `python manage.py spectacular --fail-on-warn`
- [ ] `npx tsc -b`, `npm run lint`, `npm run build`

## If this touches a contract

`docs/DECISIONS.md` is where the backend and frontend agree on field names, URL paths and
query parameters. Changing one side without the other is the failure mode this repo has
already hit once.

- [ ] Not applicable
- [ ] `docs/DECISIONS.md` updated in this PR

## Notes for the reviewer

<!-- Anything unverified, deliberately left out, or worth arguing about. -->
