"""Backfill the byte/word columns and the denormalised counters.

Pure data migration: reversible as a no-op and ``elidable`` so a future squash
drops it. Tolerant of an empty table (a fresh deploy runs it against zero rows)
and batched so the 12 legacy articles and a 10^5-row table both behave.

The ``Revision`` pass walks each article's history in chronological order,
because ``byte_delta``, ``parent`` and ``is_page_creation`` are all defined
relative to the previous revision and cannot be computed row-at-a-time.
"""

from django.db import migrations
from django.db.models import Count

from apps.articles.markup import count_words

BATCH = 200


def _chunks(items, size=BATCH):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _backfill_article_sizes(Article) -> None:
    pending = []
    for article in Article.objects.all().only("id", "content").iterator(chunk_size=BATCH):
        content = article.content or ""
        article.byte_size = len(content.encode("utf-8"))
        article.word_count = count_words(content)
        pending.append(article)
    for batch in _chunks(pending):
        Article.objects.bulk_update(batch, ["byte_size", "word_count"], batch_size=BATCH)


def _backfill_revisions(Revision) -> None:
    article_ids = list(Revision.objects.values_list("article_id", flat=True).distinct())
    for article_id in article_ids:
        previous_size = 0
        previous_id = None
        pending = []
        revisions = (
            Revision.objects.filter(article_id=article_id)
            .select_related("editor")
            .order_by("created_at", "id")
        )
        for index, revision in enumerate(revisions):
            size = len((revision.content or "").encode("utf-8"))
            revision.byte_size = size
            revision.byte_delta = size - previous_size
            revision.parent_id = previous_id
            revision.is_page_creation = index == 0
            revision.is_bot = bool(getattr(revision.editor, "is_bot", False))
            previous_size, previous_id = size, revision.pk
            pending.append(revision)
        for batch in _chunks(pending):
            Revision.objects.bulk_update(
                batch,
                ["byte_size", "byte_delta", "parent_id", "is_page_creation", "is_bot"],
                batch_size=BATCH,
            )


def _backfill_counters(Article, Revision) -> None:
    totals = dict(Revision.objects.values_list("article_id").annotate(total=Count("id")))
    contributors = dict(
        Revision.objects.exclude(editor__isnull=True)
        .values_list("article_id")
        .annotate(total=Count("editor_id", distinct=True))
    )
    pending = []
    for article in Article.objects.all().only("id").iterator(chunk_size=BATCH):
        article.revision_total = totals.get(article.pk, 0)
        article.contributor_total = contributors.get(article.pk, 0)
        pending.append(article)
    for batch in _chunks(pending):
        Article.objects.bulk_update(
            batch, ["revision_total", "contributor_total"], batch_size=BATCH
        )


def forwards(apps, schema_editor) -> None:
    Article = apps.get_model("articles", "Article")
    Revision = apps.get_model("articles", "Revision")
    _backfill_article_sizes(Article)
    _backfill_revisions(Revision)
    _backfill_counters(Article, Revision)


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0004_search_infrastructure"),
        ("accounts", "0002_user_counters"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop, elidable=True),
    ]
