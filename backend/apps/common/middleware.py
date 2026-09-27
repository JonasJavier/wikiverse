"""Response-level security headers, emitted by Django itself.

The backend is publicly reachable on its own Railway host, so headers added
only by the frontend's nginx would protect exactly one of the two live paths.
This middleware closes the second one.

Everything is driven from settings (and therefore from the environment), and
the paths that legitimately need inline script -- the Django admin and the
interactive API docs -- are exempt from the Content-Security-Policy while
still receiving every other header.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

if TYPE_CHECKING:  # pragma: no cover - import-time cost is not worth it
    from collections.abc import Callable, Iterable

    from django.http import HttpRequest, HttpResponse

__all__ = [
    "DEFAULT_CONTENT_SECURITY_POLICY",
    "DEFAULT_CSP_EXEMPT_PREFIXES",
    "DEFAULT_PERMISSIONS_POLICY",
    "SecurityHeadersMiddleware",
]

#: DECISIONS section 7.3. Kept as a module constant so ``settings.py`` and the
#: tests can both reference the canonical policy.
DEFAULT_CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "img-src 'self' https://upload.wikimedia.org https://commons.wikimedia.org data:; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self' https://fonts.gstatic.com; "
    "connect-src 'self' https://*.sentry.io; "
    "frame-ancestors 'none'; "
    "base-uri 'self'"
)

DEFAULT_PERMISSIONS_POLICY = (
    "accelerometer=(), autoplay=(), camera=(), display-capture=(), "
    "encrypted-media=(), fullscreen=(self), geolocation=(), gyroscope=(), "
    "magnetometer=(), microphone=(), midi=(), payment=(), usb=(), "
    "xr-spatial-tracking=()"
)

#: Prefixes that need inline script to function at all.
DEFAULT_CSP_EXEMPT_PREFIXES: tuple[str, ...] = ("/admin/", "/api/docs/", "/api/redoc/")


class SecurityHeadersMiddleware:
    """Attach the site security headers to every response.

    Header values are read once at instantiation. Django's own
    ``SecurityMiddleware`` uses ``headers.setdefault`` for ``Referrer-Policy``,
    ``Cross-Origin-Opener-Policy`` and ``X-Content-Type-Options``, so the values
    written here -- set further down the chain -- are the ones that survive.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.policy: str = getattr(
            settings, "CONTENT_SECURITY_POLICY", DEFAULT_CONTENT_SECURITY_POLICY
        )
        self.report_only: bool = bool(
            getattr(settings, "CONTENT_SECURITY_POLICY_REPORT_ONLY", False)
        )
        self.exempt_prefixes: tuple[str, ...] = tuple(
            getattr(settings, "CSP_EXEMPT_PREFIXES", DEFAULT_CSP_EXEMPT_PREFIXES)
        )
        self.referrer_policy: str = getattr(
            settings, "SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin"
        )
        self.permissions_policy: str = getattr(
            settings, "PERMISSIONS_POLICY", DEFAULT_PERMISSIONS_POLICY
        )
        self.coop: str = getattr(settings, "SECURE_CROSS_ORIGIN_OPENER_POLICY", "same-origin")

    @property
    def csp_header(self) -> str:
        if self.report_only:
            return "Content-Security-Policy-Report-Only"
        return "Content-Security-Policy"

    def csp_exempt(self, path: str) -> bool:
        return any(path.startswith(prefix) for prefix in self.exempt_prefixes)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        self.apply(request, response)
        return response

    def apply(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Write the headers onto ``response``. Existing values are respected."""
        if self.policy and not self.csp_exempt(request.path):
            self._set(response, self.csp_header, self.policy)

        self._set(response, "Referrer-Policy", self.referrer_policy)
        self._set(response, "X-Content-Type-Options", "nosniff")
        self._set(response, "Permissions-Policy", self.permissions_policy)
        self._set(response, "Cross-Origin-Opener-Policy", self.coop)
        return response

    @staticmethod
    def _set(response: HttpResponse, header: str, value: str) -> None:
        if value and header not in response.headers:
            response.headers[header] = value


def iter_default_headers() -> Iterable[tuple[str, str]]:
    """The static header set, for documentation and tests."""
    return (
        ("Content-Security-Policy", DEFAULT_CONTENT_SECURITY_POLICY),
        ("Referrer-Policy", "strict-origin-when-cross-origin"),
        ("X-Content-Type-Options", "nosniff"),
        ("Permissions-Policy", DEFAULT_PERMISSIONS_POLICY),
        ("Cross-Origin-Opener-Policy", "same-origin"),
    )
