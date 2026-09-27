"""``manage.py rebuild_links`` — re-extract every ``[[wikilink]]``.

``ArticleLink`` rows are written when an article is saved through the API and by
the seed. They go stale in two ways the write path cannot catch:

* An article is **renamed**, so links that pointed at the old title are now red
  and links that were red at the new title are now resolvable.
* A row was written by something that does not call
  :meth:`ArticleLink.rebuild_for` — a data migration, the admin, ``loaddata``, a
  restored dump.

This command rebuilds from the bodies, which are the source of truth. It runs the
same :meth:`ArticleLink.rebuild_for` the API uses, so it cannot drift from it, and
then resolves every remaining red link in one pass — that second pass matters,
because a link is only red once *all* articles exist.

Red links are kept, not deleted. A row with ``to_article = NULL`` and ``to_title``
set is what paints the link red, what ranks ``GET /api/wanted/`` and what makes
"what links here" work on the day the missing article is written (DECISIONS §19).
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.articles.models import Article, ArticleLink


class Command(BaseCommand):
    help = "Re-extract ArticleLink rows from article bodies and infoboxes."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--slug",
            action="append",
            default=[],
            help="Rebuild only this article's outgoing links. Repeatable.",
        )

    def handle(self, *args, **options) -> None:
        queryset = Article.objects.all().only("id", "slug", "title", "content", "infobox")
        if options["slug"]:
            queryset = queryset.filter(slug__in=options["slug"])
            missing = set(options["slug"]) - set(queryset.values_list("slug", flat=True))
            if missing:
                self.stderr.write(self.style.WARNING(f"Unknown slug(s): {sorted(missing)}"))

        articles = list(queryset)
        if not articles:
            self.stdout.write("No articles to process.")
            return

        with transaction.atomic():
            written = 0
            for article in articles:
                written += ArticleLink.rebuild_for(article)
            # Second pass: a link is red only if no article has that slug. Doing
            # this per article would paint links red purely because of iteration
            # order.
            resolved = 0
            for article in Article.objects.all().only("id", "slug"):
                resolved += ArticleLink.attach_target(article)

        total = ArticleLink.objects.count()
        red = ArticleLink.objects.filter(to_article__isnull=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Rebuilt links for {len(articles)} article(s): {written} extracted, "
                f"{resolved} late-resolved. Table now holds {total} link(s), "
                f"{red} of them red."
            )
        )
