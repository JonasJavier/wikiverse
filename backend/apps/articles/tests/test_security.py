"""Content security: response headers (DECISIONS §7.3) and the lead-image
host allowlist (§7.4).

The CSP string below is copied character for character from DECISIONS §7.3,
not imported from the middleware, so a drift in either place fails here.
"""

from __future__ import annotations

import pytest

from apps.articles.models import Article

pytestmark = pytest.mark.django_db

#: DECISIONS §7.3, verbatim.
EXPECTED_CSP = (
    "default-src 'self'; "
    "img-src 'self' https://upload.wikimedia.org https://commons.wikimedia.org data:; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self' https://fonts.gstatic.com; "
    "connect-src 'self' https://*.sentry.io; "
    "frame-ancestors 'none'; "
    "base-uri 'self'"
)

ALLOWED_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"


# --------------------------------------------------------------------------- #
# Security headers, emitted by Django itself
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        "/api/health/",
        "/api/articles/",
        "/api/search/?q=x",
        "/api/articles/no-such-article/",  # 404s carry the headers too
        "/api/auth/me/",  # and so do 401s
        "/robots.txt",
    ],
)
def test_security_headers_on_backend_responses(api_client, settings, path):
    response = api_client.get(path)
    assert response.headers["Content-Security-Policy"] == EXPECTED_CSP
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    # Env-overridable (SECURE_REFERRER_POLICY); asserted against the setting.
    assert response.headers["Referrer-Policy"] == settings.SECURE_REFERRER_POLICY
    assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
    assert "camera=()" in response.headers["Permissions-Policy"]
    assert "geolocation=()" in response.headers["Permissions-Policy"]
    assert response.headers["X-Frame-Options"] == "DENY"


def test_csp_is_enforcing_not_report_only(api_client):
    response = api_client.get("/api/health/")
    assert "Content-Security-Policy-Report-Only" not in response.headers


def test_admin_is_exempt_from_csp_but_keeps_other_headers(client):
    # The Django admin needs inline script; it gets every header except CSP.
    # The anonymous redirect exercises the middleware without rendering the
    # admin's static-heavy templates.
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "Content-Security-Policy" not in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
    assert "Permissions-Policy" in response.headers


def test_csp_setting_keeps_its_closing_quote(settings):
    # Regression: settings.py once ran the policy through a helper that stripped
    # quote characters from both ends, turning the final 'self' into 'self and
    # silently changing the base-uri directive.
    assert settings.CONTENT_SECURITY_POLICY == EXPECTED_CSP
    assert settings.CONTENT_SECURITY_POLICY.endswith("base-uri 'self'")


def test_csp_header_on_write_responses(auth_client, category):
    response = auth_client.post(
        "/api/articles/",
        {"title": "Header check", "content": "Body.", "category": category.slug},
        format="json",
    )
    assert response.status_code == 201
    assert response.headers["Content-Security-Policy"] == EXPECTED_CSP


# --------------------------------------------------------------------------- #
# lead_image_url host allowlist (ArticleWriteSerializer)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "url",
    [
        "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
        "https://commons.wikimedia.org/wiki/Special:FilePath/Example.jpg",
        "https://UPLOAD.WIKIMEDIA.ORG/wikipedia/commons/a/a9/Example.jpg",
    ],
)
def test_lead_image_on_allowlisted_host_is_accepted(auth_client, url):
    response = auth_client.post(
        "/api/articles/",
        {"title": "Allowed image", "content": "Body.", "lead_image_url": url},
        format="json",
    )
    assert response.status_code == 201, response.data
    assert Article.objects.get(slug=response.data["slug"]).lead_image_url == url


@pytest.mark.parametrize(
    "url",
    [
        "https://evil.example.com/pixel.png",
        "http://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",  # not https
        "https://upload.wikimedia.org.evil.example/x.jpg",  # suffix trick
        "https://evilupload.wikimedia.org/x.jpg",
        "https://user@upload.wikimedia.org/x.jpg",  # userinfo in the netloc
        "https://upload.wikimedia.org:8443/x.jpg",  # non-default port
        "//upload.wikimedia.org/x.jpg",  # scheme-relative
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
    ],
)
def test_lead_image_off_allowlist_is_rejected_on_create(auth_client, url):
    response = auth_client.post(
        "/api/articles/",
        {"title": "Rejected image", "content": "Body.", "lead_image_url": url},
        format="json",
    )
    assert response.status_code == 400
    assert "lead_image_url" in response.data
    assert not Article.objects.filter(title="Rejected image").exists()


def test_lead_image_off_allowlist_is_rejected_on_edit(auth_client, article):
    response = auth_client.patch(
        f"/api/articles/{article.slug}/",
        {"lead_image_url": "https://images.example.net/tracker.gif"},
        format="json",
    )
    assert response.status_code == 400
    assert list(response.data) == ["lead_image_url"]
    article.refresh_from_db()
    assert article.lead_image_url == ""
    assert article.revisions.count() == 0


def test_lead_image_can_be_cleared(auth_client, article):
    Article.objects.filter(pk=article.pk).update(lead_image_url=ALLOWED_IMAGE)
    response = auth_client.patch(
        f"/api/articles/{article.slug}/", {"lead_image_url": ""}, format="json"
    )
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.lead_image_url == ""


def test_lead_image_allowlist_follows_settings(auth_client, settings):
    settings.LEAD_IMAGE_ALLOWED_HOSTS = ["images.example.org"]
    rejected = auth_client.post(
        "/api/articles/",
        {"title": "Wikimedia now refused", "content": "Body.", "lead_image_url": ALLOWED_IMAGE},
        format="json",
    )
    assert rejected.status_code == 400
    accepted = auth_client.post(
        "/api/articles/",
        {
            "title": "Custom host",
            "content": "Body.",
            "lead_image_url": "https://images.example.org/a.jpg",
        },
        format="json",
    )
    assert accepted.status_code == 201


# --------------------------------------------------------------------------- #
# Stored content is returned as data, never rendered server-side
# --------------------------------------------------------------------------- #
def test_article_body_html_is_stored_verbatim_as_json_text(auth_client, api_client):
    body = '**Bold** <script>alert("x")</script>'
    created = auth_client.post(
        "/api/articles/", {"title": "Raw body", "content": body}, format="json"
    )
    assert created.status_code == 201
    response = api_client.get(f"/api/articles/{created.data['slug']}/")
    assert response["Content-Type"].startswith("application/json")
    # The frontend renders with skipHtml; the API must not pre-render or mangle.
    assert response.data["content"] == body
