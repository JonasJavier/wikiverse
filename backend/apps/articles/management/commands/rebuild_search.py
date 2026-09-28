"""``manage.py rebuild_search`` — repopulate ``Article.search_vector``.

The vector is maintained by a PostgreSQL ``BEFORE INSERT OR UPDATE OF`` trigger
installed by ``articles.0004_search_infrastructure``, not by Python, so nothing
in the application can bypass it. Three things still can:

* a ``COPY`` or ``INSERT`` issued before the trigger existed,
* ``articles.0005``-era rows restored from a dump taken on a database whose text
  search configuration differed,
* a change to ``settings.SEARCH_CONFIG`` — the stored lexemes were produced by
  the *old* configuration and are now subtly wrong.

This command fixes all three by touching every row so the trigger re-fires. It
writes ``title = title``: a no-op to the data, and the trigger's ``UPDATE OF``
list names ``title``, so the vector is rebuilt from all four weighted columns.

On SQLite there is no vector — :meth:`ArticleQuerySet.search` takes the
``icontains`` path — so the command reports that and exits 0. A repair command
that fails on the development database would not get run.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import connection

from apps.articles.models import Article
from apps.articles.querysets import is_postgres, search_config

#: Rows per statement. Large enough to be fast, small enough that the command
#: does not hold one enormous transaction over the whole table.
BATCH = 500


class Command(BaseCommand):
    help = "Rebuild Article.search_vector on PostgreSQL. No-op on SQLite."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--batch",
            type=int,
            default=BATCH,
            help=f"Rows per UPDATE statement (default {BATCH}).",
        )

    def handle(self, *args, **options) -> None:
        if not is_postgres():
            self.stdout.write(
                self.style.WARNING(
                    f"Database vendor is {connection.vendor!r}, which has no tsvector; "
                    "search uses the icontains fallback. Nothing to rebuild."
                )
            )
            return

        table = Article._meta.db_table
        total = Article.objects.count()
        if not total:
            self.stdout.write("No articles.")
            return

        batch = max(1, options["batch"])
        done = 0
        after = 0
        with connection.cursor() as cursor:
            while True:
                # Re-fire the trigger without changing the data. The keyset walk
                # over the primary key keeps every statement bounded, so this is
                # safe to run against a live database.
                cursor.execute(
                    f"""
                    UPDATE {table} SET title = title
                    WHERE id IN (
                        SELECT id FROM {table} WHERE id > %s ORDER BY id LIMIT %s
                    )
                    RETURNING id
                    """,
                    [after, batch],
                )
                ids = [row[0] for row in cursor.fetchall()]
                if not ids:
                    break
                after = max(ids)
                done += len(ids)
                self.stdout.write(f"  {done}/{total}", ending="\r")

        empty = Article.objects.filter(search_vector__isnull=True).count()
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Rebuilt {done} search vector(s) with configuration "
                f"{search_config()!r}; {empty} row(s) still NULL."
            )
        )
