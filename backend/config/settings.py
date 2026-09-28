"""
Django settings for the Wikiverse project.

Configuration is driven entirely by environment variables (12-factor style)
via ``django-environ`` so the same code runs locally, in Docker and in
production without edits. See ``.env.example`` at the repo root.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import environ

# Safe to import from settings: the module pulls in nothing but ``django.conf``
# and the standard library at import time.
from apps.common.middleware import (
    DEFAULT_CONTENT_SECURITY_POLICY,
    DEFAULT_CSP_EXEMPT_PREFIXES,
    DEFAULT_PERMISSIONS_POLICY,
)

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-dev-key-change-me"),
    ALLOWED_HOSTS=(str, "*"),
    CORS_ALLOWED_ORIGINS=(
        str,
        "http://localhost:5173,http://127.0.0.1:5173",
    ),
    CSRF_TRUSTED_ORIGINS=(str, ""),
    # Absolute by construction: ``sqlite:///db.sqlite3`` is CWD-relative, so
    # running manage.py from backend/ used to create a second, empty database.
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
    REDIS_URL=(str, ""),
    DJANGO_LOG_LEVEL=(str, "INFO"),
    SEARCH_CONFIG=(str, "wikiverse_english"),
    SEARCH_SUGGEST_TTL=(int, 60),
    PUBLIC_BASE_URL=(str, "https://wikiverse.jonasjavier.dev"),
    PUBLIC_SITE_DOMAIN=(str, "wikiverse.jonasjavier.dev"),
    SENTRY_DSN=(str, ""),
)

# Read a .env file if present (handy for non-Docker local runs).
environ.Env.read_env(BASE_DIR.parent / ".env")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def clean_env_value(value: str) -> str:
    """Normalize values copied from dashboards or .env files."""
    return value.strip().strip('"').strip("'")


def unwrap_env_value(value: str) -> str:
    """Strip whitespace and one pair of quotes that wrap the *whole* value.

    For values that legitimately end in a quote character: a CSP ends in
    ``base-uri 'self'``, and :func:`clean_env_value` would eat that closing quote.
    """
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def env_csv(name: str, default: str = "") -> list[str]:
    """Read comma-separated env vars safely."""
    raw_value = clean_env_value(env(name, default=default))
    return [clean_env_value(item) for item in raw_value.split(",") if clean_env_value(item)]


# --------------------------------------------------------------------------- #
# Core
# --------------------------------------------------------------------------- #
SECRET_KEY = clean_env_value(env("SECRET_KEY"))
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env_csv("ALLOWED_HOSTS", "*")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sitemaps",
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    # Local
    "apps.common",
    "apps.accounts",
    "apps.articles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Above WhiteNoise so static assets and admin pages carry the headers too.
    "apps.common.middleware.SecurityHeadersMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"].setdefault("CONN_MAX_AGE", 60)
# Persistent connections plus a liveness check: without this, a connection
# dropped by the platform while the service slept surfaces as a 500 on wake.
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

if "postgresql" in DATABASES["default"].get("ENGINE", ""):
    # psycopg-only option; sqlite3.connect() would reject it.
    DATABASES["default"].setdefault("OPTIONS", {}).setdefault(
        "connect_timeout", env.int("DB_CONNECT_TIMEOUT", default=5)
    )

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"


# --------------------------------------------------------------------------- #
# Cache
# --------------------------------------------------------------------------- #
REDIS_URL = clean_env_value(env("REDIS_URL", default=""))

if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
            },
            "KEY_PREFIX": "wikiverse",
        }
    }
else:
    # Safe fallback. This prevents Redis misconfiguration from taking down
    # API docs, throttling, health checks, or normal reads.
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "wikiverse-fallback-cache",
        }
    }

DJANGO_REDIS_IGNORE_EXCEPTIONS = True


# --------------------------------------------------------------------------- #
# Auth / passwords
# --------------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------- #
# Internationalization
# --------------------------------------------------------------------------- #
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------- #
# Static & media
# --------------------------------------------------------------------------- #
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}


# --------------------------------------------------------------------------- #
# Django REST Framework
# --------------------------------------------------------------------------- #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.DefaultPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    # Railway's edge is the only hop that rewrites X-Forwarded-For in front of
    # the backend service, so DRF must take the last-but-one entry.
    "NUM_PROXIES": env.int("NUM_PROXIES", default=1),
    # All nine scopes (DECISIONS 18); every one is env-overridable.
    "DEFAULT_THROTTLE_RATES": {
        "anon": clean_env_value(env("THROTTLE_ANON", default="100/min")),
        "user": clean_env_value(env("THROTTLE_USER", default="1000/min")),
        "search": clean_env_value(env("THROTTLE_SEARCH", default="60/min")),
        "suggest": clean_env_value(env("THROTTLE_SUGGEST", default="120/min")),
        "preview": clean_env_value(env("THROTTLE_PREVIEW", default="240/min")),
        "diff": clean_env_value(env("THROTTLE_DIFF", default="60/min")),
        "write": clean_env_value(env("THROTTLE_WRITE", default="60/min")),
        "login": clean_env_value(env("THROTTLE_LOGIN", default="10/min")),
        "register": clean_env_value(env("THROTTLE_REGISTER", default="5/hour")),
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_MINUTES", default=30)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_DAYS", default=2)),
    "ROTATE_REFRESH_TOKENS": True,
    # With rotation on, the superseded refresh token must be revoked; otherwise
    # a stolen refresh token stays usable for its whole lifetime.
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Wikiverse API",
    "DESCRIPTION": (
        "A modern, open encyclopedia API — articles, revisions, "
        "categories, full-text search and JWT auth."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {"persistAuthorization": True},
}


# --------------------------------------------------------------------------- #
# CORS / CSRF
# --------------------------------------------------------------------------- #
CORS_ALLOWED_ORIGINS = env_csv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env_csv("CSRF_TRUSTED_ORIGINS", "")


# --------------------------------------------------------------------------- #
# Public site identity
#
# nginx rewrites the Host header to the Railway domain, so absolute URLs in
# sitemaps, feeds and Open Graph tags must come from configuration, never from
# the incoming request.
# --------------------------------------------------------------------------- #
PUBLIC_BASE_URL = clean_env_value(env("PUBLIC_BASE_URL")).rstrip("/")
PUBLIC_SITE_DOMAIN = clean_env_value(env("PUBLIC_SITE_DOMAIN"))


# --------------------------------------------------------------------------- #
# Full-text search
# --------------------------------------------------------------------------- #
# Created by migration articles.0004_search_infrastructure; the name always
# resolves on PostgreSQL, with or without the unaccent extension. Ignored on
# SQLite, which uses the icontains fallback path.
SEARCH_CONFIG = clean_env_value(env("SEARCH_CONFIG"))
SEARCH_SUGGEST_TTL = env.int("SEARCH_SUGGEST_TTL")


# --------------------------------------------------------------------------- #
# Remote media allowlist
#
# Must stay in step with the img-src directive of CONTENT_SECURITY_POLICY
# below: a lead image the CSP would block is a broken image.
# --------------------------------------------------------------------------- #
LEAD_IMAGE_ALLOWED_HOSTS = env_csv(
    "LEAD_IMAGE_ALLOWED_HOSTS",
    "upload.wikimedia.org,commons.wikimedia.org",
)


# --------------------------------------------------------------------------- #
# Security headers (apps.common.middleware.SecurityHeadersMiddleware)
#
# Emitted by Django, not only by the frontend's nginx: the backend is publicly
# reachable on its own Railway host, so an nginx-only header would cover just
# one of the two live paths.
# --------------------------------------------------------------------------- #
CONTENT_SECURITY_POLICY = unwrap_env_value(
    env("CONTENT_SECURITY_POLICY", default=DEFAULT_CONTENT_SECURITY_POLICY)
)
CONTENT_SECURITY_POLICY_REPORT_ONLY = env.bool(
    "CONTENT_SECURITY_POLICY_REPORT_ONLY",
    default=False,
)
# The admin and the interactive API docs genuinely need inline script.
CSP_EXEMPT_PREFIXES = env_csv(
    "CSP_EXEMPT_PREFIXES",
    ",".join(DEFAULT_CSP_EXEMPT_PREFIXES),
)
PERMISSIONS_POLICY = clean_env_value(env("PERMISSIONS_POLICY", default=DEFAULT_PERMISSIONS_POLICY))
# Read by both Django's SecurityMiddleware and ours; ours writes first and wins.
SECURE_REFERRER_POLICY = clean_env_value(
    env("SECURE_REFERRER_POLICY", default="strict-origin-when-cross-origin")
)
SECURE_CROSS_ORIGIN_OPENER_POLICY = clean_env_value(
    env("SECURE_CROSS_ORIGIN_OPENER_POLICY", default="same-origin")
)
SECURE_CONTENT_TYPE_NOSNIFF = True


# --------------------------------------------------------------------------- #
# Security
# --------------------------------------------------------------------------- #
if not DEBUG:
    # Railway already terminates HTTPS at the edge. Keep this false until the
    # backend, frontend, custom domains, and health checks are fully stable.
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)

    # If SECURE_SSL_REDIRECT is enabled later, never redirect health checks.
    SECURE_REDIRECT_EXEMPT = [r"^api/health/$"]

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Do not enable HSTS preload too early. It is intentionally conservative.
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        default=False,
    )
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)

    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": clean_env_value(env("DJANGO_LOG_LEVEL", default="INFO")),
    },
}


# --------------------------------------------------------------------------- #
# Error tracking (optional)
#
# A complete no-op unless SENTRY_DSN is set, and a no-op even then if the
# package is not installed: local dev, pytest and CI must never initialise it.
# send_default_pii stays False so usernames, emails, IPs and article bodies
# never leave the service.
# --------------------------------------------------------------------------- #
SENTRY_DSN = clean_env_value(env("SENTRY_DSN"))

if SENTRY_DSN:
    try:
        import sentry_sdk
    except ImportError:  # pragma: no cover - optional dependency
        import logging as _logging

        _logging.getLogger(__name__).warning(
            "SENTRY_DSN is set but sentry-sdk is not installed; skipping init."
        )
    else:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=clean_env_value(env("SENTRY_ENVIRONMENT", default="production")),
            release=clean_env_value(env("SENTRY_RELEASE", default="")) or None,
            send_default_pii=False,
            traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.05),
            profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE", default=0.0),
        )
