"""PostgreSQL helpers shared by the search migrations.

Django's migration loader ignores modules whose name starts with an underscore,
so this file is importable from migrations without being one.

Everything here is written so that:

* it is a **no-op on SQLite** (checked with ``connection.vendor`` at run time,
  never at import time), and
* a **permission failure is logged, not raised** — ``CREATE EXTENSION`` needs
  rights the application role may not have, and a deploy must not die because an
  optional accent-folding extension is unavailable.
"""

from __future__ import annotations

import logging

from django.contrib.postgres.operations import CreateExtension
from django.db import ProgrammingError, transaction

logger = logging.getLogger(__name__)

TABLE = "articles_article"
FUNCTION = "articles_article_search_refresh"
TRIGGER = "articles_article_search_trg"

#: Always created, so ``settings.SEARCH_CONFIG`` always resolves.
CONFIG = "wikiverse_english"

#: The columns that feed the vector. Both lists must match: a column that is
#: weighted but missing from the UPDATE OF list produces an article that exists,
#: renders, and is invisible to search — with no error anywhere.
VECTOR_COLUMNS = ("title", "short_description", "summary", "content")

FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION {function}() RETURNS trigger
LANGUAGE plpgsql AS $body$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('{config}', coalesce(NEW.title, '')), 'A') ||
        setweight(to_tsvector('{config}', coalesce(NEW.short_description, '')), 'B') ||
        setweight(to_tsvector('{config}', coalesce(NEW.summary, '')), 'B') ||
        setweight(to_tsvector('{config}', coalesce(NEW.content, '')), 'C');
    RETURN NEW;
END
$body$;
"""

TRIGGER_SQL = """
DROP TRIGGER IF EXISTS {trigger} ON {table};
CREATE TRIGGER {trigger}
BEFORE INSERT OR UPDATE OF {columns} ON {table}
FOR EACH ROW EXECUTE FUNCTION {function}();
"""

UNACCENT_MAPPING_SQL = """
ALTER TEXT SEARCH CONFIGURATION {config}
    ALTER MAPPING FOR hword, hword_part, word WITH unaccent, english_stem;
"""

TRIGRAM_INDEXES = (
    ("article_title_trgm", "title"),
    ("article_short_description_trgm", "short_description"),
)


class SafeExtension(CreateExtension):
    """``CREATE EXTENSION`` that logs a permission failure instead of crashing.

    The base class already early-returns on non-PostgreSQL vendors. What it does
    not survive is a non-superuser role, which is exactly the situation on a
    managed database that was not provisioned with the extension.
    """

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != "postgresql":
            return
        try:
            with transaction.atomic(using=schema_editor.connection.alias):
                super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception as exc:  # noqa: BLE001 - an optional extension must not break deploys
            logger.warning(
                "Could not create the %r extension (%s). Fuzzy search and accent "
                "folding will be unavailable; everything else works.",
                self.name,
                exc,
            )

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if schema_editor.connection.vendor != "postgresql":
            return
        try:
            with transaction.atomic(using=schema_editor.connection.alias):
                super().database_backwards(app_label, schema_editor, from_state, to_state)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not drop the %r extension (%s).", self.name, exc)


class SafeTrigramExtension(SafeExtension):
    def __init__(self) -> None:
        self.name = "pg_trgm"


class SafeUnaccentExtension(SafeExtension):
    def __init__(self) -> None:
        self.name = "unaccent"


def _extension_exists(cursor, name: str) -> bool:
    cursor.execute("SELECT 1 FROM pg_extension WHERE extname = %s", [name])
    return cursor.fetchone() is not None


def _config_exists(cursor, name: str) -> bool:
    cursor.execute("SELECT 1 FROM pg_ts_config WHERE cfgname = %s", [name])
    return cursor.fetchone() is not None


def create_text_search_config(apps, schema_editor) -> None:
    """Create the ``wikiverse_english`` configuration. Always.

    With ``unaccent`` available it folds accents, so "Emile" finds "Émile".
    Without it, it is a plain copy of ``pg_catalog.english``. Either way the name
    exists, which is what makes ``settings.SEARCH_CONFIG`` unconditionally valid.
    """
    if schema_editor.connection.vendor != "postgresql":
        return
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        if _config_exists(cursor, CONFIG):
            return
    try:
        with transaction.atomic(using=connection.alias), connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TEXT SEARCH CONFIGURATION {CONFIG} ( COPY = pg_catalog.english )"
            )
    except Exception as exc:  # noqa: BLE001 - degrade to the stock config, never crash
        logger.warning(
            "Could not create the %r text search configuration (%s). Search will "
            "fall back to pg_catalog.english; set SEARCH_CONFIG=english.",
            CONFIG,
            exc,
        )
        return
    with connection.cursor() as cursor:
        has_unaccent = _extension_exists(cursor, "unaccent")
    if not has_unaccent:
        logger.warning(
            "The unaccent extension is unavailable: %r is a plain copy of "
            "pg_catalog.english and accents will not be folded.",
            CONFIG,
        )
        return
    try:
        with transaction.atomic(using=connection.alias), connection.cursor() as cursor:
            cursor.execute(UNACCENT_MAPPING_SQL.format(config=CONFIG))
    except ProgrammingError as exc:  # pragma: no cover - depends on server rights
        logger.warning("Could not add the unaccent mapping to %r: %s", CONFIG, exc)


def drop_text_search_config(apps, schema_editor) -> None:
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TEXT SEARCH CONFIGURATION IF EXISTS {CONFIG}")


def install_search_trigger(apps, schema_editor) -> None:
    """Install the vector trigger, the trigram indexes, and backfill.

    A trigger rather than Python: it fires for ``bulk_create``,
    ``queryset.update()``, the admin, ``loaddata``, raw SQL and psql sessions
    alike, so the vector cannot go stale through any write path. A stale vector
    means an article silently stops being findable, which is the worst bug class
    an encyclopedia has.
    """
    if schema_editor.connection.vendor != "postgresql":
        return
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        config = CONFIG if _config_exists(cursor, CONFIG) else "english"
        cursor.execute(FUNCTION_SQL.format(function=FUNCTION, config=config))
        cursor.execute(
            TRIGGER_SQL.format(
                trigger=TRIGGER,
                table=TABLE,
                columns=", ".join(VECTOR_COLUMNS),
                function=FUNCTION,
            )
        )
        # Touching a weighted column fires the trigger, so this is the cheapest
        # correct backfill. Batched by id so a large table does not take one
        # enormous lock.
        cursor.execute(f"SELECT COALESCE(MIN(id), 0), COALESCE(MAX(id), -1) FROM {TABLE}")
        low, high = cursor.fetchone()
        batch = 1000
        while low <= high:
            cursor.execute(
                f"UPDATE {TABLE} SET title = title WHERE id >= %s AND id < %s",
                [low, low + batch],
            )
            low += batch
        if _extension_exists(cursor, "pg_trgm"):
            for name, column in TRIGRAM_INDEXES:
                cursor.execute(
                    f"CREATE INDEX IF NOT EXISTS {name} ON {TABLE} "
                    f"USING gin ({column} gin_trgm_ops)"
                )
        else:
            logger.warning("pg_trgm is unavailable: skipping the trigram indexes.")


def remove_search_trigger(apps, schema_editor) -> None:
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TRIGGER IF EXISTS {TRIGGER} ON {TABLE}")
        cursor.execute(f"DROP FUNCTION IF EXISTS {FUNCTION}()")
        for name, _column in TRIGRAM_INDEXES:
            cursor.execute(f"DROP INDEX IF EXISTS {name}")
