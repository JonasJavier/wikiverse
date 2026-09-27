"""``manage.py prune_legacy_seed`` — retire the 12 pre-cutover demo articles.

The first deployment shipped a twelve-article demo about the project's own stack
(HTML, CSS, JavaScript, …) and four categories to hold it. That content is not
encyclopedia content, one of its slugs (``javascript``) collides with a real
corpus article, and it is what makes ``manage.py seed`` refuse to run
(DECISIONS §8). This command removes it *surgically*, so a deployment that already
carries real edits does not have to reach for ``seed --flush --force``.

Safety, because this deletes rows:

* Nothing happens without ``--force``; the default is a dry run that prints
  exactly what would go.
* An article is deleted **only** if its title and slug both match the legacy list
  *and* it has no revision tagged ``seed``. An article somebody has edited since —
  or that the new seed has already rewritten — is reported and skipped.
* A legacy category is deleted only once it holds no articles at all.
* The legacy ``admin`` user is **not** touched. ``accounts.0003`` already disabled
  the account, and deleting the row would rewrite the authorship of history that
  is being kept.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.articles.models import Article, Category, Revision
from apps.common.utils import wiki_slug

#: The twelve titles the pre-cutover seed created.
LEGACY_TITLES: tuple[str, ...] = (
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "Python",
    "Django",
    "React",
    "Vite",
    "Git",
    "PostgreSQL",
    "Redis",
    "REST API",
)

#: The four categories it created. Removed only when empty.
LEGACY_CATEGORIES: tuple[str, ...] = (
    "Web Development",
    "Programming Languages",
    "Tools & Infrastructure",
    "Databases",
)

SEED_TAG = "seed"


class Command(BaseCommand):
    help = "Remove the 12 legacy demo articles and their empty categories. Dry run by default."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Actually delete. Without it the command only reports.",
        )

    def handle(self, *args, **options) -> None:
        force = options["force"]
        legacy_slugs = {wiki_slug(title) for title in LEGACY_TITLES}

        candidates = list(
            Article.objects.filter(slug__in=legacy_slugs, title__in=LEGACY_TITLES).only(
                "id", "slug", "title"
            )
        )
        if not candidates:
            self.stdout.write(self.style.SUCCESS("No legacy demo articles found; nothing to do."))
            self._report_categories(force, touched=False)
            return

        # A revision tagged "seed" means the new seed owns this row, so it is not
        # legacy content whatever its title says. Evaluated in Python: SQLite has
        # no JSON `contains` lookup and this command must behave the same on both
        # databases.
        reseeded: set[int] = set()
        for article_id, tags in Revision.objects.filter(article__in=candidates).values_list(
            "article_id", "tags"
        ):
            if isinstance(tags, list) and SEED_TAG in tags:
                reseeded.add(article_id)

        doomed = [article for article in candidates if article.pk not in reseeded]
        skipped = [article for article in candidates if article.pk in reseeded]

        for article in skipped:
            self.stdout.write(
                self.style.WARNING(
                    f"  keeping  {article.slug}: it has seeded history, so it is not "
                    "legacy content."
                )
            )
        for article in doomed:
            self.stdout.write(f"  {'deleting' if force else 'would delete'}  {article.slug}")

        if not doomed:
            self.stdout.write(self.style.SUCCESS("Nothing left to prune."))
            self._report_categories(force, touched=False)
            return

        if not force:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: {len(doomed)} article(s) and their revisions, references, "
                    "links, talk threads and watches would be deleted (cascade). "
                    "Re-run with --force."
                )
            )
            self._report_categories(force, touched=False)
            return

        with transaction.atomic():
            deleted, per_model = Article.objects.filter(
                pk__in=[article.pk for article in doomed]
            ).delete()
            self._report_categories(force, touched=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Pruned {len(doomed)} legacy article(s); {deleted} row(s) removed in total "
                "("
                + ", ".join(f"{name.split('.')[-1]}={n}" for name, n in per_model.items())
                + ")."
            )
        )
        self.stdout.write(
            "`manage.py seed` will now run. The legacy `admin` account was left in place; "
            "`accounts.0003` already disabled it."
        )

    def _report_categories(self, force: bool, *, touched: bool) -> None:
        """Delete legacy categories that no longer hold anything."""
        for name in LEGACY_CATEGORIES:
            category = Category.objects.filter(name=name).first()
            if category is None:
                continue
            articles = category.articles.count() + category.secondary_articles.count()
            if articles:
                self.stdout.write(
                    self.style.WARNING(
                        f"  keeping category {name!r}: {articles} article(s) still use it."
                    )
                )
                continue
            if force and touched:
                category.delete()
                self.stdout.write(f"  deleted category {name!r} (empty)")
            else:
                self.stdout.write(f"  would delete category {name!r} (empty)")
