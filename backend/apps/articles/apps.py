"""App config for the wiki, plus the deploy-time search configuration check."""

from __future__ import annotations

import logging

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Tags, register
from django.core.checks import Warning as CheckWarning

logger = logging.getLogger(__name__)

#: The migration that creates the text search configuration. The check stays
#: silent until it has been applied, otherwise the very first `migrate` against
#: a fresh PostgreSQL database would warn about a config it is about to create.
SEARCH_MIGRATION = "0004_search_infrastructure"


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.articles"
    verbose_name = "Articles"

    def ready(self) -> None:
        register(Tags.database)(check_search_config)


def check_search_config(app_configs, databases=None, **kwargs):
    """Assert that ``settings.SEARCH_CONFIG`` resolves in ``pg_ts_config``.

    A missing text search configuration does not raise at startup — it raises on
    the first search query, in production, as a 500. This turns it into a line
    in the deploy log instead.

    Deliberately a ``Warning`` and not an ``Error``: ``migrate`` runs database
    checks *before* applying migrations, so an ``Error`` here would make the
    migration that creates the configuration unrunnable. Runs only against
    PostgreSQL, and never fails when the database is unreachable — checks run at
    deploy time, where an unreachable database is a different alarm.
    """
    from django.db import connections
    from django.db.utils import DatabaseError

    from .querysets import DEFAULT_SEARCH_CONFIG

    errors = []
    config = getattr(settings, "SEARCH_CONFIG", None) or DEFAULT_SEARCH_CONFIG
    for alias in databases or []:
        connection = connections[alias]
        if connection.vendor != "postgresql":
            continue
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM django_migrations WHERE app = 'articles' AND name = %s LIMIT 1",
                    [SEARCH_MIGRATION],
                )
                if cursor.fetchone() is None:
                    continue
                cursor.execute(
                    "SELECT 1 FROM pg_ts_config WHERE cfgname = %s LIMIT 1",
                    [config],
                )
                found = cursor.fetchone()
        except DatabaseError as exc:  # pragma: no cover - deploy-time safety net
            logger.warning("Could not verify SEARCH_CONFIG on %r: %s", alias, exc)
            continue
        except Exception as exc:  # pragma: no cover - never block a deploy
            logger.warning("Unexpected error verifying SEARCH_CONFIG on %r: %s", alias, exc)
            continue
        if found is None:
            errors.append(
                CheckWarning(
                    f"Text search configuration {config!r} does not exist in this database.",
                    hint=(
                        "Run `manage.py migrate articles` to create it, or set SEARCH_CONFIG "
                        "to a configuration that exists (e.g. 'english'). Until then every "
                        "full-text query will fail."
                    ),
                    id="articles.W001",
                )
            )
    return errors
