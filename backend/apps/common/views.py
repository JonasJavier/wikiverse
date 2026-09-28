"""Operational endpoints.

``health_check`` is liveness and is wired to the platform health check, so it
stays deliberately dumb: no DRF, no throttling, no cache, no database. A
dependency outage must not turn into a failed deploy.

``readiness_check`` is the deeper probe, for humans and for the README. It is
wired to nothing in the platform config on purpose: keeping liveness and
readiness separate is the whole point.
"""

from __future__ import annotations

import logging
import uuid

from django.core.cache import cache
from django.db import connection
from django.http import HttpRequest, JsonResponse

logger = logging.getLogger(__name__)

__all__ = ["health_check", "readiness_check"]


def health_check(request):
    """Simple liveness probe.

    This endpoint intentionally avoids DRF, throttling, cache, Redis and
    database access so platform health checks can verify the web process itself.
    """
    return JsonResponse({"status": "ok"})


def _check_database() -> tuple[bool, str]:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as exc:  # pragma: no cover - exercised only with a dead DB
        logger.warning("readiness: database check failed: %s", exc)
        return False, "unavailable"
    return True, "ok"


def _check_cache() -> tuple[bool, str]:
    """Round-trip a value.

    ``IGNORE_EXCEPTIONS`` means django-redis swallows connection errors and
    ``get`` simply returns ``None``, so a write-then-read is the only reliable
    way to tell a working cache from a silently discarded one.
    """
    key = f"wikiverse:readiness:{uuid.uuid4().hex}"
    try:
        cache.set(key, "ok", 10)
        value = cache.get(key)
        cache.delete(key)
    except Exception as exc:  # pragma: no cover - exercised only with a dead cache
        logger.warning("readiness: cache check failed: %s", exc)
        return False, "unavailable"
    if value != "ok":
        logger.warning("readiness: cache round-trip returned %r", value)
        return False, "unavailable"
    return True, "ok"


def readiness_check(request: HttpRequest) -> JsonResponse:
    """Deep readiness probe: 200 when the database and cache both answer, else 503."""
    database_ok, database_status = _check_database()
    cache_ok, cache_status = _check_cache()
    ready = database_ok and cache_ok

    payload = {
        "status": "ready" if ready else "degraded",
        "checks": {"database": database_status, "cache": cache_status},
    }
    response = JsonResponse(payload, status=200 if ready else 503)
    response.headers["Cache-Control"] = "no-store"
    return response
