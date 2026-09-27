"""Throttle classes for the nine Wikiverse scopes.

The rates themselves live in ``REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`` and
are all environment-overridable (see ``config/settings.py``); this module only
declares *how* each scope is keyed.

Two keying strategies are used:

``IdentityRateThrottle``
    One bucket per authenticated user, or per client IP for anonymous callers.
    Used for the read-heavy scopes and for writes.

``CredentialRateThrottle``
    Two buckets checked together -- one per client IP and one per *submitted*
    credential. Rotating ``X-Forwarded-For`` on the directly reachable backend
    host moves the IP bucket but not the credential bucket, so login and
    register attempts against a single account stay capped (DECISIONS 7.5).
"""

from __future__ import annotations

import hashlib

from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, UserRateThrottle

__all__ = [
    "AnonBurstThrottle",
    "CredentialRateThrottle",
    "DiffThrottle",
    "IdentityRateThrottle",
    "LoginThrottle",
    "PreviewThrottle",
    "RegisterThrottle",
    "SearchThrottle",
    "SuggestThrottle",
    "THROTTLE_SCOPES",
    "UserBurstThrottle",
    "WriteThrottle",
]

#: Every scope that must exist in ``DEFAULT_THROTTLE_RATES``.
THROTTLE_SCOPES: tuple[str, ...] = (
    "anon",
    "user",
    "search",
    "suggest",
    "preview",
    "diff",
    "write",
    "login",
    "register",
)

#: Longest credential value folded into a throttle key.
MAX_CREDENTIAL_LENGTH = 150


def _digest(value: str) -> str:
    """Stable, short, non-reversible key fragment for a credential."""
    return hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()[:32]


class IdentityRateThrottle(SimpleRateThrottle):
    """Per-user when authenticated, per-IP otherwise."""

    scope = ""

    def get_cache_key(self, request, view) -> str | None:
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            ident = f"u{user.pk}"
        else:
            ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class SearchThrottle(IdentityRateThrottle):
    """``GET /api/search/``."""

    scope = "search"


class SuggestThrottle(IdentityRateThrottle):
    """``GET /api/search/suggest/`` -- keystroke rate."""

    scope = "suggest"


class PreviewThrottle(IdentityRateThrottle):
    """``GET /api/articles/{slug}/preview/`` -- hover cards."""

    scope = "preview"


class DiffThrottle(IdentityRateThrottle):
    """``GET /api/articles/{slug}/diff/`` -- the only CPU-bound read."""

    scope = "diff"


class WriteThrottle(IdentityRateThrottle):
    """Any unsafe method on the content endpoints."""

    scope = "write"

    def allow_request(self, request, view) -> bool:
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return super().allow_request(request, view)


class AnonBurstThrottle(AnonRateThrottle):
    """The DRF default anonymous throttle, named so the scope is greppable."""

    scope = "anon"


class UserBurstThrottle(UserRateThrottle):
    """The DRF default authenticated throttle, named for symmetry."""

    scope = "user"


class CredentialRateThrottle(SimpleRateThrottle):
    """Rate-limit on the client IP *and* on the submitted credential.

    ``SimpleRateThrottle`` supports a single bucket, so the sliding-window
    algorithm is re-implemented here over a list of keys. A request is allowed
    only when every bucket has room; the timestamp is then recorded in all of
    them.
    """

    scope = ""
    credential_fields: tuple[str, ...] = ("username", "email")

    def get_credential(self, request) -> str | None:
        """The submitted account identifier, or ``None`` when unreadable."""
        try:
            data = request.data
        except AttributeError:  # not a DRF request -- IP-only limiting
            return None
        except Exception:  # unparseable body -- IP-only limiting
            return None
        if not hasattr(data, "get"):
            return None
        for field in self.credential_fields:
            value = data.get(field)
            if isinstance(value, str) and value.strip():
                return value.strip()[:MAX_CREDENTIAL_LENGTH].casefold()
        return None

    def get_cache_keys(self, request, view) -> list[str]:
        keys = [self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}]
        credential = self.get_credential(request)
        if credential:
            keys.append(
                self.cache_format % {"scope": f"{self.scope}-id", "ident": _digest(credential)}
            )
        return keys

    def get_cache_key(self, request, view) -> str | None:  # pragma: no cover - unused
        # Present for API compatibility; ``allow_request`` uses get_cache_keys().
        return self.get_cache_keys(request, view)[0]

    def allow_request(self, request, view) -> bool:
        if self.rate is None:
            return True

        self.now = self.timer()
        histories: list[tuple[str, list[float]]] = []

        for key in self.get_cache_keys(request, view):
            history = list(self.cache.get(key, []))
            while history and history[-1] <= self.now - self.duration:
                history.pop()
            if len(history) >= self.num_requests:
                self.key, self.history = key, history
                return self.throttle_failure()
            histories.append((key, history))

        for key, history in histories:
            history.insert(0, self.now)
            self.cache.set(key, history, self.duration)

        self.key, self.history = histories[0]
        return True


class LoginThrottle(CredentialRateThrottle):
    """``POST /api/auth/login/``."""

    scope = "login"


class RegisterThrottle(CredentialRateThrottle):
    """``POST /api/auth/register/``."""

    scope = "register"
