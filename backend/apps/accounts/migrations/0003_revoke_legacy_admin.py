"""Revoke the legacy ``admin`` account.

The pre-cutover deployment created a superuser named ``admin`` with a password
that was committed to the repository, so that password is in git history for
good and cannot be un-published. This migration takes the account out of
service: unusable password, no staff flag, no superuser flag. It does **not**
delete the row, because the 12 legacy articles are attributed to it and deleting
the user would rewrite their authorship.

Recovery is ``manage.py ensure_admin``, which creates or updates a superuser
from ``DJANGO_ADMIN_USERNAME`` / ``DJANGO_ADMIN_EMAIL`` /
``DJANGO_ADMIN_PASSWORD`` and prints a generated password once when that last
variable is absent.

Only accounts that existed *before* the cutover are touched, so running the
migration after ``ensure_admin`` has created a fresh superuser is harmless.
"""

import datetime

from django.contrib.auth.hashers import make_password
from django.db import migrations

#: Anything created after this instant belongs to the new deployment.
CUTOVER = datetime.datetime(2026, 9, 26, tzinfo=datetime.timezone.utc)

LEGACY_USERNAME = "admin"


def forwards(apps, schema_editor) -> None:
    User = apps.get_model("accounts", "User")
    legacy = User.objects.filter(
        username=LEGACY_USERNAME,
        is_superuser=True,
        date_joined__lt=CUTOVER,
    )
    for user in legacy:
        # A historical model has no set_unusable_password(); make_password(None)
        # is exactly what that method stores.
        user.password = make_password(None)
        user.is_staff = False
        user.is_superuser = False
        user.save(update_fields=["password", "is_staff", "is_superuser"])


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_counters"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop, elidable=False),
    ]
