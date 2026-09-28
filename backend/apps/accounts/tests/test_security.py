"""Account security: credential throttles (DECISIONS §7.5), logout (§7.2), the
legacy ``admin`` revocation and ``ensure_admin`` (§8).
"""

from __future__ import annotations

import datetime as dt
import importlib
import re

import pytest
from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.common.throttling import LoginThrottle, RegisterThrottle

pytestmark = pytest.mark.django_db

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
REGISTER_URL = "/api/auth/register/"
LOGOUT_URL = "/api/auth/logout/"
REFRESH_URL = "/api/auth/refresh/"


def forwarded(ip: str) -> dict[str, str]:
    """The spoofable header a client can set on the directly reachable backend."""
    return {"HTTP_X_FORWARDED_FOR": ip}


# --------------------------------------------------------------------------- #
# Throttles keyed on the submitted username as well as the IP (§7.5)
# --------------------------------------------------------------------------- #
@pytest.fixture
def tight_login_throttle(monkeypatch):
    monkeypatch.setattr(LoginThrottle, "rate", "3/min", raising=False)


@pytest.fixture
def tight_register_throttle(monkeypatch):
    monkeypatch.setattr(RegisterThrottle, "rate", "2/min", raising=False)


def test_login_throttle_survives_a_rotating_forwarded_for(api_client, user, tight_login_throttle):
    for attempt in range(3):
        response = api_client.post(
            LOGIN_URL,
            {"username": "tester", "password": "wrong"},
            **forwarded(f"203.0.113.{attempt}"),
        )
        assert response.status_code == 401
    # A fresh "IP" does not reset the per-username bucket.
    response = api_client.post(
        LOGIN_URL, {"username": "tester", "password": "wrong"}, **forwarded("198.51.100.7")
    )
    assert response.status_code == 429


def test_login_throttle_blocks_even_the_right_password_once_exhausted(
    api_client, user, tight_login_throttle
):
    for attempt in range(3):
        api_client.post(
            LOGIN_URL,
            {"username": "tester", "password": "wrong"},
            **forwarded(f"203.0.113.{attempt}"),
        )
    response = api_client.post(
        LOGIN_URL, {"username": "tester", "password": "testpass123"}, **forwarded("192.0.2.1")
    )
    assert response.status_code == 429
    assert "access" not in response.data


def test_login_throttle_username_bucket_is_case_insensitive(api_client, user, tight_login_throttle):
    for attempt, name in enumerate(["tester", "TESTER", " Tester "]):
        api_client.post(
            LOGIN_URL, {"username": name, "password": "wrong"}, **forwarded(f"203.0.113.{attempt}")
        )
    response = api_client.post(
        LOGIN_URL, {"username": "tEsTeR", "password": "wrong"}, **forwarded("203.0.113.50")
    )
    assert response.status_code == 429


def test_login_throttle_still_has_a_per_ip_bucket(api_client, user, tight_login_throttle):
    for attempt in range(3):
        api_client.post(
            LOGIN_URL,
            {"username": f"someone{attempt}", "password": "wrong"},
            **forwarded("203.0.113.9"),
        )
    response = api_client.post(
        LOGIN_URL, {"username": "tester", "password": "testpass123"}, **forwarded("203.0.113.9")
    )
    assert response.status_code == 429


def test_login_throttle_does_not_punish_other_accounts(
    api_client, user, other_user, tight_login_throttle
):
    for attempt in range(3):
        api_client.post(
            LOGIN_URL,
            {"username": "tester", "password": "wrong"},
            **forwarded(f"203.0.113.{attempt}"),
        )
    response = api_client.post(
        LOGIN_URL, {"username": "other", "password": "testpass123"}, **forwarded("192.0.2.200")
    )
    assert response.status_code == 200


def test_register_throttle_keys_on_the_username(api_client, tight_register_throttle):
    payload = {
        "username": "newbie",
        "email": "newbie@example.com",
        "password": "Sup3rSecret!",
        "password_confirm": "Sup3rSecret!",
    }
    first = api_client.post(REGISTER_URL, payload, **forwarded("203.0.113.1"))
    assert first.status_code == 201
    second = api_client.post(
        REGISTER_URL, {**payload, "email": "b@example.com"}, **forwarded("203.0.113.2")
    )
    assert second.status_code == 400  # username taken
    third = api_client.post(
        REGISTER_URL, {**payload, "email": "c@example.com"}, **forwarded("203.0.113.3")
    )
    assert third.status_code == 429


def test_all_nine_throttle_scopes_are_configured(settings):
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]
    assert set(rates) == {
        "anon",
        "user",
        "search",
        "suggest",
        "preview",
        "diff",
        "write",
        "login",
        "register",
    }
    assert all(rates.values())
    assert settings.REST_FRAMEWORK["NUM_PROXIES"] == 1


# --------------------------------------------------------------------------- #
# Logout blacklists the refresh token (§7.1, §7.2)
# --------------------------------------------------------------------------- #
@pytest.fixture
def tokens(api_client, user) -> dict:
    response = api_client.post(LOGIN_URL, {"username": "tester", "password": "testpass123"})
    assert response.status_code == 200
    return response.data


def test_logout_blacklists_the_refresh_token(api_client, tokens):
    response = api_client.post(LOGOUT_URL, {"refresh": tokens["refresh"]})
    assert response.status_code == 204
    assert BlacklistedToken.objects.count() == 1

    refreshed = api_client.post(REFRESH_URL, {"refresh": tokens["refresh"]})
    assert refreshed.status_code == 401


def test_logout_needs_no_access_token(tokens):
    # A user whose access token has expired must still be able to revoke.
    from rest_framework.test import APIClient

    assert APIClient().post(LOGOUT_URL, {"refresh": tokens["refresh"]}).status_code == 204


def test_logout_twice_is_rejected(api_client, tokens):
    assert api_client.post(LOGOUT_URL, {"refresh": tokens["refresh"]}).status_code == 204
    again = api_client.post(LOGOUT_URL, {"refresh": tokens["refresh"]})
    assert again.status_code == 400
    assert "refresh" in again.data


@pytest.mark.parametrize("payload", [{}, {"refresh": ""}, {"refresh": "not-a-jwt"}])
def test_logout_rejects_garbage(api_client, payload):
    response = api_client.post(LOGOUT_URL, payload)
    assert response.status_code == 400
    assert "refresh" in response.data


def test_logout_rejects_an_access_token(api_client, tokens):
    response = api_client.post(LOGOUT_URL, {"refresh": tokens["access"]})
    assert response.status_code == 400


def test_rotation_blacklists_the_superseded_refresh_token(api_client, tokens):
    rotated = api_client.post(REFRESH_URL, {"refresh": tokens["refresh"]})
    assert rotated.status_code == 200
    assert rotated.data["refresh"] != tokens["refresh"]
    replay = api_client.post(REFRESH_URL, {"refresh": tokens["refresh"]})
    assert replay.status_code == 401


def test_jwt_lifetimes(settings):
    jwt = settings.SIMPLE_JWT
    assert jwt["BLACKLIST_AFTER_ROTATION"] is True
    assert jwt["ROTATE_REFRESH_TOKENS"] is True
    assert jwt["REFRESH_TOKEN_LIFETIME"] == dt.timedelta(days=2)
    assert "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS


# --------------------------------------------------------------------------- #
# Profiles never leak email or staff status
# --------------------------------------------------------------------------- #
def test_public_profile_hides_email_and_staff(api_client, staff_user):
    response = api_client.get(f"/api/auth/users/{staff_user.username}/")
    assert response.status_code == 200
    assert "email" not in response.data
    assert "is_staff" not in response.data


def test_me_cannot_promote_itself(auth_client, user):
    response = auth_client.patch("/api/auth/me/", {"is_staff": True, "bio": "hi"}, format="json")
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_staff is False
    assert user.bio == "hi"


# --------------------------------------------------------------------------- #
# accounts.0003_revoke_legacy_admin (§8)
# --------------------------------------------------------------------------- #
revoke = importlib.import_module("apps.accounts.migrations.0003_revoke_legacy_admin")


def _backdate(user, when: dt.datetime) -> None:
    User.objects.filter(pk=user.pk).update(date_joined=when)


def test_revoke_migration_is_applied():
    applied = MigrationRecorder(connection).applied_migrations()
    assert ("accounts", "0003_revoke_legacy_admin") in applied


def test_revoke_takes_the_legacy_admin_out_of_service():
    admin = User.objects.create_superuser("admin", "admin@example.com", "adminpass123")
    _backdate(admin, revoke.CUTOVER - dt.timedelta(days=30))

    revoke.forwards(django_apps, None)

    admin.refresh_from_db()
    assert admin.has_usable_password() is False
    assert admin.check_password("adminpass123") is False
    assert admin.is_staff is False
    assert admin.is_superuser is False
    # The row survives: legacy articles are attributed to it.
    assert User.objects.filter(username="admin").exists()


def test_revoke_leaves_an_admin_created_after_the_cutover_alone():
    admin = User.objects.create_superuser("admin", "admin@example.com", "fresh-Secret-9")
    _backdate(admin, revoke.CUTOVER + dt.timedelta(days=1))

    revoke.forwards(django_apps, None)

    admin.refresh_from_db()
    assert admin.is_superuser is True
    assert admin.check_password("fresh-Secret-9")


def test_revoke_only_touches_the_admin_username():
    other = User.objects.create_superuser("root", "root@example.com", "Root-Secret-9")
    _backdate(other, revoke.CUTOVER - dt.timedelta(days=30))

    revoke.forwards(django_apps, None)

    other.refresh_from_db()
    assert other.is_superuser is True
    assert other.check_password("Root-Secret-9")


# --------------------------------------------------------------------------- #
# manage.py ensure_admin (§8)
# --------------------------------------------------------------------------- #
@pytest.fixture
def admin_env(monkeypatch):
    for name in ("DJANGO_ADMIN_USERNAME", "DJANGO_ADMIN_EMAIL", "DJANGO_ADMIN_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_ensure_admin_uses_the_environment_and_never_echoes_the_password(admin_env, capsys):
    admin_env.setenv("DJANGO_ADMIN_USERNAME", "curator")
    admin_env.setenv("DJANGO_ADMIN_EMAIL", "curator@example.org")
    admin_env.setenv("DJANGO_ADMIN_PASSWORD", "Env-Supplied-Secret-42")

    call_command("ensure_admin")

    output = capsys.readouterr().out
    assert "Env-Supplied-Secret-42" not in output
    admin = User.objects.get(username="curator")
    assert admin.is_superuser and admin.is_staff and admin.is_active
    assert admin.email == "curator@example.org"
    assert admin.check_password("Env-Supplied-Secret-42")


def test_ensure_admin_generates_and_prints_a_password_once(admin_env, capsys):
    call_command("ensure_admin")

    output = capsys.readouterr().out
    admin = User.objects.get(username="admin")
    assert admin.is_superuser
    printed = re.findall(r"^\s{4}(\S{24})\s*$", output, flags=re.M)
    assert len(printed) == 1
    assert admin.check_password(printed[0])


def test_ensure_admin_is_idempotent_and_promotes_an_existing_account(admin_env, user):
    admin_env.setenv("DJANGO_ADMIN_USERNAME", user.username)
    admin_env.setenv("DJANGO_ADMIN_PASSWORD", "Rotated-Secret-77")

    call_command("ensure_admin")
    call_command("ensure_admin")

    assert User.objects.filter(username=user.username).count() == 1
    user.refresh_from_db()
    assert user.is_superuser and user.is_staff
    assert user.check_password("Rotated-Secret-77")


def test_ensure_admin_no_password_change_keeps_the_existing_password(admin_env, user):
    admin_env.setenv("DJANGO_ADMIN_USERNAME", user.username)
    admin_env.setenv("DJANGO_ADMIN_PASSWORD", "Would-Replace-It-1")

    call_command("ensure_admin", "--no-password-change")

    user.refresh_from_db()
    assert user.is_superuser
    assert user.check_password("testpass123")


def test_ensure_admin_restores_a_revoked_legacy_admin(admin_env):
    legacy = User.objects.create_superuser("admin", "admin@example.com", "adminpass123")
    _backdate(legacy, timezone.make_aware(dt.datetime(2025, 1, 1)))
    revoke.forwards(django_apps, None)
    admin_env.setenv("DJANGO_ADMIN_PASSWORD", "New-Admin-Secret-5")

    call_command("ensure_admin")

    legacy.refresh_from_db()
    assert legacy.is_superuser
    assert legacy.check_password("New-Admin-Secret-5")
    assert not legacy.check_password("adminpass123")
