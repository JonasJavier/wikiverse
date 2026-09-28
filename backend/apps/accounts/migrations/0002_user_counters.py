"""Add the denormalised edit counter and the bot flag, and backfill both.

``edit_count`` is denormalised because the history row, the diff header and the
semi-protection check all read it; a ``COUNT`` per row would be an N+1 on every
history page. It is incremented inside the revision-snapshot transaction and
repaired by ``manage.py rebuild_counts``.
"""

from django.db import migrations, models
from django.db.models import Count


def forwards(apps, schema_editor) -> None:
    User = apps.get_model("accounts", "User")
    Revision = apps.get_model("articles", "Revision")
    counts = dict(
        Revision.objects.exclude(editor__isnull=True)
        .values_list("editor_id")
        .annotate(total=Count("id"))
    )
    if not counts:
        return
    users = list(User.objects.filter(pk__in=counts).only("id"))
    for user in users:
        user.edit_count = counts.get(user.pk, 0)
    User.objects.bulk_update(users, ["edit_count"], batch_size=200)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        # The backfill reads articles.Revision.
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="edit_count",
            field=models.PositiveIntegerField(
                default=0,
                editable=False,
                help_text=(
                    "Denormalised revision count. Drives semi-protection and the history byline."
                ),
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="is_bot",
            field=models.BooleanField(
                default=False,
                help_text="Marks automated edits with the 'b' flag in Recent changes.",
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["-edit_count"], name="user_edit_count_desc"),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop, elidable=True),
    ]
