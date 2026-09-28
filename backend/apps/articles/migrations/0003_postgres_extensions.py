"""PostgreSQL extensions for fuzzy search and accent folding.

Both operations are no-ops on SQLite (``CreateExtension.database_forwards``
early-returns on a non-PostgreSQL vendor) and both survive a role without the
rights to create an extension: the failure is logged inside a savepoint and the
deploy continues without fuzzy matching. See ``_pgsql.SafeExtension``.
"""

from django.db import migrations

from apps.articles.migrations._pgsql import SafeTrigramExtension, SafeUnaccentExtension


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0002_article_apparatus"),
    ]

    operations = [
        SafeTrigramExtension(),
        SafeUnaccentExtension(),
    ]
