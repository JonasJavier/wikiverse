"""Who may do what (DECISIONS §15, plus the wiki-open editing model).

* restore is admin-only and must find soft-deleted rows;
* ``protection`` / ``is_published`` without the right to change them is a
  field-level **400**, never a 403;
* anonymous callers read and never write;
* protection levels gate edits by edit count and staff status.
"""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.articles.models import Article, TalkThread

pytestmark = pytest.mark.django_db


def detail(article: Article) -> str:
    return f"/api/articles/{article.slug}/"


# --------------------------------------------------------------------------- #
# Restore (§15)
# --------------------------------------------------------------------------- #
@pytest.fixture
def deleted_article(article, user):
    article.soft_delete(by=user)
    return article


def test_restore_is_admin_only_even_for_the_author(auth_client, deleted_article):
    response = auth_client.post(f"{detail(deleted_article)}restore/")
    assert response.status_code == 403
    deleted_article.refresh_from_db()
    assert deleted_article.is_deleted is True


def test_restore_rejects_anonymous(api_client, deleted_article):
    assert api_client.post(f"{detail(deleted_article)}restore/").status_code == 401


def test_staff_restore_finds_the_soft_deleted_row(staff_client, deleted_article, api_client):
    assert api_client.get(detail(deleted_article)).status_code == 404

    response = staff_client.post(f"{detail(deleted_article)}restore/")
    assert response.status_code == 200
    assert response.data["slug"] == deleted_article.slug
    deleted_article.refresh_from_db()
    assert deleted_article.is_deleted is False
    assert deleted_article.deleted_at is None
    assert deleted_article.deleted_by is None
    assert api_client.get(detail(deleted_article)).status_code == 200


def test_restore_of_an_unknown_slug_is_404(staff_client):
    assert staff_client.post("/api/articles/no-such-page/restore/").status_code == 404


# --------------------------------------------------------------------------- #
# Privileged fields are a field-level 400 (§15)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("field", "value"),
    [("protection", "full"), ("protection", "semi"), ("is_published", False)],
)
def test_privileged_field_without_rights_is_a_field_level_400(other_client, article, field, value):
    response = other_client.patch(
        detail(article), {field: value, "content": "An allowed body edit."}, format="json"
    )
    assert response.status_code == 400
    assert list(response.data) == [field]
    assert field in str(response.data[field][0])
    article.refresh_from_db()
    assert article.protection == Article.Protection.OPEN
    assert article.is_published is True
    assert article.revisions.count() == 0  # the whole edit was refused


def test_both_privileged_fields_are_named(other_client, article):
    response = other_client.patch(
        detail(article), {"protection": "full", "is_published": False}, format="json"
    )
    assert response.status_code == 400
    assert set(response.data) == {"protection", "is_published"}


def test_resubmitting_the_current_value_is_not_a_change(other_client, article):
    # Edit forms post the whole record; an unchanged status field is not a 400.
    response = other_client.patch(
        detail(article),
        {"protection": "open", "is_published": True, "content": "Edited by someone else."},
        format="json",
    )
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.content == "Edited by someone else."


def test_the_author_may_change_status_fields(auth_client, article):
    response = auth_client.patch(
        detail(article), {"protection": "semi", "is_published": False}, format="json"
    )
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.protection == Article.Protection.SEMI
    assert article.is_published is False


def test_staff_may_change_status_fields(staff_client, article):
    response = staff_client.patch(detail(article), {"protection": "full"}, format="json")
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.protection == Article.Protection.FULL


def test_put_is_a_partial_replace_with_the_same_gate(other_client, article):
    response = other_client.put(detail(article), {"protection": "full"}, format="json")
    assert response.status_code == 400
    assert list(response.data) == ["protection"]


# --------------------------------------------------------------------------- #
# Anonymous callers never write
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("method", "suffix", "payload"),
    [
        ("post", "", {"title": "Anon page", "content": "x"}),
        ("patch", "{slug}/", {"content": "defaced"}),
        ("put", "{slug}/", {"content": "defaced"}),
        ("delete", "{slug}/", None),
        ("post", "{slug}/revert/", {"revision": 1}),
        ("post", "{slug}/watch/", None),
        ("delete", "{slug}/watch/", None),
        ("post", "{slug}/talk/", {"title": "Anon thread", "body": "hello"}),
    ],
)
def test_anonymous_cannot_write(api_client, article, method, suffix, payload):
    url = "/api/articles/" + suffix.format(slug=article.slug)
    response = getattr(api_client, method)(url, payload, format="json")
    assert response.status_code == 401
    article.refresh_from_db()
    assert article.content.startswith("# Django")
    assert not article.is_deleted
    assert Article.objects.count() == 1


def test_anonymous_cannot_reply_in_a_thread(api_client, article, user):
    thread = TalkThread.objects.create(article=article, title="Existing", created_by=user)
    response = api_client.post(
        f"{detail(article)}talk/{thread.pk}/messages/", {"body": "hi"}, format="json"
    )
    assert response.status_code == 401


def test_anonymous_cannot_read_the_watchlist(api_client):
    assert api_client.get("/api/watchlist/").status_code == 401


# --------------------------------------------------------------------------- #
# Wiki-open editing and deletion
# --------------------------------------------------------------------------- #
def test_any_signed_in_user_may_edit_an_open_article(other_client, article, other_user):
    response = other_client.patch(detail(article), {"content": "Improved."}, format="json")
    assert response.status_code == 200
    article.refresh_from_db()
    assert article.last_editor == other_user
    assert article.author != other_user


def test_staff_may_delete_any_article(staff_client, article, staff_user):
    assert staff_client.delete(detail(article)).status_code == 204
    article.refresh_from_db()
    assert article.is_deleted is True
    assert article.deleted_by == staff_user
    # Soft delete: the row and its history survive.
    assert Article.objects.filter(pk=article.pk).exists()


# --------------------------------------------------------------------------- #
# Protection levels
# --------------------------------------------------------------------------- #
def _protect(article: Article, level: str) -> None:
    Article.objects.filter(pk=article.pk).update(protection=level)


def test_full_protection_blocks_everyone_but_staff(auth_client, staff_client, article):
    _protect(article, Article.Protection.FULL)
    # Not even the author.
    assert auth_client.patch(detail(article), {"content": "x"}, format="json").status_code == 403
    response = staff_client.patch(detail(article), {"content": "Staff edit."}, format="json")
    assert response.status_code == 200


def test_semi_protection_needs_established_editors(other_client, other_user, article):
    _protect(article, Article.Protection.SEMI)
    User.objects.filter(pk=other_user.pk).update(edit_count=Article.SEMI_PROTECT_MIN_EDITS - 1)
    blocked = other_client.patch(detail(article), {"content": "x"}, format="json")
    assert blocked.status_code == 403

    User.objects.filter(pk=other_user.pk).update(edit_count=Article.SEMI_PROTECT_MIN_EDITS)
    fresh = APIClient()
    fresh.force_authenticate(user=User.objects.get(pk=other_user.pk))
    allowed = fresh.patch(detail(article), {"content": "Established edit."}, format="json")
    assert allowed.status_code == 200


def test_protected_article_is_still_readable(api_client, article):
    _protect(article, Article.Protection.FULL)
    response = api_client.get(detail(article))
    assert response.status_code == 200
    assert response.data["protection"] == "full"


# --------------------------------------------------------------------------- #
# Drafts
# --------------------------------------------------------------------------- #
def test_drafts_are_visible_to_their_author_only(auth_client, other_client, article):
    Article.objects.filter(pk=article.pk).update(is_published=False)
    assert APIClient().get(detail(article)).status_code == 404
    assert other_client.get(detail(article)).status_code == 404
    assert auth_client.get(detail(article)).status_code == 200


def test_staff_see_soft_deleted_articles(staff_client, api_client, article, user):
    article.soft_delete(by=user)
    assert api_client.get(detail(article)).status_code == 404
    assert staff_client.get(detail(article)).status_code == 200
