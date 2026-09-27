"""``manage.py rebuild_counts`` — re-derive every denormalised counter.

The counters exist because the alternative is an aggregate per row on a paginated
list. They are maintained incrementally by the write paths, which means any path
that skips the maintenance leaves them wrong: the admin, a data migration, a
restored dump, a crash between two writes.

Every counter has exactly one definition, and it is the model method — not a query
repeated here. ``Article.recount()``, ``TalkThread.touch()`` and
``User.recount_edits()`` are the definitions, so this command calls them and can
never disagree with the incremental path about what a counter *means*.

Repaired here:

* ``Article.revision_total``, ``contributor_total``, ``watcher_total``,
  ``backlink_total``
* ``Article.byte_size`` / ``word_count`` — derived in ``Article.save()``
* ``TalkThread.message_count``, ``participant_count``, ``last_message_at``
* ``User.edit_count``

``--dry-run`` reports the drift without writing, which is the form to put in a
monitoring job.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.articles.models import Article, TalkThread
from apps.common.utils import count_words

User = get_user_model()

#: ``Article`` counters this command repairs, in report order.
ARTICLE_COUNTERS = (
    "revision_total",
    "contributor_total",
    "watcher_total",
    "backlink_total",
)


class Command(BaseCommand):
    help = "Re-derive Article, TalkThread and User counters from the underlying rows."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report drift without writing anything.",
        )

    def handle(self, *args, **options) -> None:
        dry_run = options["dry_run"]
        drift: dict[str, int] = dict.fromkeys(
            (*ARTICLE_COUNTERS, "byte_size", "word_count", "thread_totals", "edit_count"), 0
        )

        with transaction.atomic():
            for article in Article.objects.all().iterator(chunk_size=200):
                before = {name: getattr(article, name) for name in ARTICLE_COUNTERS}
                # recount() *is* the definition of each counter; save=False so a
                # dry run cannot write.
                after = article.recount(save=False)
                for name in ARTICLE_COUNTERS:
                    if before[name] != after[name]:
                        drift[name] += 1

                content = article.content or ""
                size = len(content.encode("utf-8"))
                words = count_words(content)
                if article.byte_size != size:
                    drift["byte_size"] += 1
                if article.word_count != words:
                    drift["word_count"] += 1

                if not dry_run:
                    # ``Article.save`` re-derives byte_size and word_count itself,
                    # and ``update_fields`` keeps ``updated_at`` off the wire:
                    # repairing a counter must not reorder the whole encyclopedia.
                    article.save(update_fields=list(ARTICLE_COUNTERS))

            for thread in TalkThread.objects.all().iterator(chunk_size=200):
                before = (thread.message_count, thread.participant_count, thread.last_message_at)
                thread.touch(save=False)
                after = (thread.message_count, thread.participant_count, thread.last_message_at)
                if before != after:
                    drift["thread_totals"] += 1
                if not dry_run:
                    thread.save(
                        update_fields=[
                            "message_count",
                            "participant_count",
                            "last_message_at",
                            "updated_at",
                        ]
                    )

            for user in User.objects.all().iterator(chunk_size=200):
                before_edits = user.edit_count
                user.recount_edits(save=False)
                if before_edits != user.edit_count:
                    drift["edit_count"] += 1
                if not dry_run:
                    user.save(update_fields=["edit_count"])

            if dry_run:
                transaction.set_rollback(True)

        verb = "would repair" if dry_run else "repaired"
        total = sum(drift.values())
        self.stdout.write(self.style.MIGRATE_HEADING(f"rebuild_counts: {verb} {total} row(s)"))
        width = max(len(name) for name in drift)
        for name, count in drift.items():
            self.stdout.write(f"  {name.ljust(width)}  {count:>6}")
        if total == 0:
            self.stdout.write(self.style.SUCCESS("Every counter already agreed with the data."))
