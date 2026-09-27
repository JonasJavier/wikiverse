"""Full-text search: text search configuration, stored vector, index, trigger.

Order matters:

1. the ``wikiverse_english`` text search configuration is created **always**, so
   ``settings.SEARCH_CONFIG`` always resolves (with the ``unaccent`` mapping when
   that extension exists, as a plain copy of ``pg_catalog.english`` when it does
   not);
2. then the ``search_vector`` column, which the trigger writes to;
3. then the GIN index — a plain btree index on SQLite, because that schema
   editor's ``CREATE INDEX`` template has no ``USING`` clause, which is what
   keeps the migration graph identical on both backends;
4. then the trigger, which weights ``title`` A, ``short_description`` and
   ``summary`` B and ``content`` C and fires on
   ``INSERT OR UPDATE OF title, short_description, summary, content``.

Leaving ``short_description`` out of either the weighting or the ``UPDATE OF``
list is the specific bug this migration is written to prevent: the column would
be searchable but never refreshed, so editing a gloss would silently stop
matching it.
"""

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations

from apps.articles.migrations._pgsql import (
    create_text_search_config,
    drop_text_search_config,
    install_search_trigger,
    remove_search_trigger,
)


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0003_postgres_extensions"),
    ]

    operations = [
        migrations.RunPython(create_text_search_config, drop_text_search_config),
        migrations.AddField(
            model_name="article",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
        migrations.AddIndex(
            model_name="article",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="article_search_gin"
            ),
        ),
        migrations.RunPython(install_search_trigger, remove_search_trigger),
    ]
