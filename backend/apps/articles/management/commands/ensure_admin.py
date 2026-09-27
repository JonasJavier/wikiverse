"""``manage.py ensure_admin`` — the only thing that creates a superuser.

The seed deliberately does not (DECISIONS §8): the previous deployment's seed
created ``admin`` with a password committed to the repository, that password is
in git history for good, and ``accounts.0003_revoke_legacy_admin`` takes the
account out of service. This command is the replacement, and it reads everything
from the environment:

===========================  =========================================
``DJANGO_ADMIN_USERNAME``    defaults to ``admin``
``DJANGO_ADMIN_EMAIL``       defaults to ``<username>@<PUBLIC_SITE_DOMAIN>``
``DJANGO_ADMIN_PASSWORD``    generated and printed **once** when absent
===========================  =========================================

No password is hardcoded here and none is ever printed when it came from the
environment — printing an operator's own secret back into a deploy log is how it
ends up in a log aggregator.

Idempotent: run it on every boot. An existing account is promoted to staff and
superuser and, when a password is supplied, has it reset.
"""

from __future__ import annotations

import secrets
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

User = get_user_model()

#: Unambiguous alphabet: no O/0, l/1/I. A generated password gets read off a
#: terminal by a human exactly once, so ambiguity is a real cost.
ALPHABET = (
    "".join(c for c in string.ascii_letters if c not in "lIO")
    + "".join(c for c in string.digits if c not in "01")
    + "!@#$%^&*-_=+"
)

PASSWORD_LENGTH = 24


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """A cryptographically random password from :data:`ALPHABET`."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


class Command(BaseCommand):
    help = "Create or update the superuser from DJANGO_ADMIN_* environment variables."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--username",
            default=None,
            help="Override DJANGO_ADMIN_USERNAME.",
        )
        parser.add_argument(
            "--email",
            default=None,
            help="Override DJANGO_ADMIN_EMAIL.",
        )
        parser.add_argument(
            "--no-password-change",
            action="store_true",
            help="Create the account if missing, but never reset an existing password.",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        import os

        username = (
            options["username"] or os.environ.get("DJANGO_ADMIN_USERNAME") or "admin"
        ).strip()
        if not username:
            raise CommandError("DJANGO_ADMIN_USERNAME is empty.")
        domain = (getattr(settings, "PUBLIC_SITE_DOMAIN", "") or "wikiverse.local").strip()
        email = (
            options["email"] or os.environ.get("DJANGO_ADMIN_EMAIL") or f"{username}@{domain}"
        ).strip()

        supplied = os.environ.get("DJANGO_ADMIN_PASSWORD") or ""
        password = supplied or generate_password()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        change_password = created or not options["no_password_change"]
        if change_password:
            user.set_password(password)
        user.save()

        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} superuser {username!r} <{email}>."))
        if not change_password:
            self.stdout.write("Password left unchanged (--no-password-change).")
        elif supplied:
            # Never echo a secret the operator already has.
            self.stdout.write("Password set from DJANGO_ADMIN_PASSWORD.")
        else:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_ADMIN_PASSWORD was not set, so one was generated. "
                    "It is shown once and is not stored anywhere in plain text:"
                )
            )
            self.stdout.write(self.style.MIGRATE_HEADING(f"    {password}"))
            self.stdout.write(
                "Save it now, then set DJANGO_ADMIN_PASSWORD so future runs are silent."
            )
