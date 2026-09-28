"""Talk pages (DECISIONS §12): threads, messages and the denormalised counters
``message_count``, ``participant_count`` and ``last_message_at``, which every
write path must keep in step via ``TalkThread.touch()``.
"""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from apps.articles.models import TalkMessage, TalkThread

pytestmark = pytest.mark.django_db

THREAD_FIELDS = [
    "id",
    "title",
    "created_by",
    "created_at",
    "updated_at",
    "last_message_at",
    "message_count",
    "participant_count",
    "is_resolved",
    "is_locked",
]

MESSAGE_FIELDS = [
    "id",
    "thread",
    "parent",
    "author",
    "body",
    "depth",
    "created_at",
    "edited_at",
    "is_deleted",
]


def talk_url(article) -> str:
    return f"/api/articles/{article.slug}/talk/"


def reply_url(article, thread_id: int) -> str:
    return f"/api/articles/{article.slug}/talk/{thread_id}/messages/"


@pytest.fixture
def thread(auth_client, article) -> dict:
    response = auth_client.post(
        talk_url(article),
        {"title": "Lead is too technical", "body": "Opening post."},
        format="json",
    )
    assert response.status_code == 201, response.data
    return response.data


def reload(thread_id: int) -> TalkThread:
    return TalkThread.objects.get(pk=thread_id)


# --------------------------------------------------------------------------- #
# Opening a thread
# --------------------------------------------------------------------------- #
def test_opening_a_thread_posts_its_first_message(thread, user):
    assert list(thread) == THREAD_FIELDS + ["article", "messages"]
    assert thread["message_count"] == 1
    assert thread["participant_count"] == 1
    assert thread["last_message_at"] is not None
    assert thread["created_by"]["username"] == user.username
    (message,) = thread["messages"]
    assert list(message) == MESSAGE_FIELDS
    assert message["body"] == "Opening post."
    assert message["depth"] == 0 and message["parent"] is None
    assert thread["article"]["slug"] == "django"


def test_thread_list_uses_denormalised_counts(api_client, thread, article):
    response = api_client.get(talk_url(article))
    assert response.status_code == 200
    assert response.data["count"] == 1
    row = response.data["results"][0]
    assert list(row) == THREAD_FIELDS
    assert row["message_count"] == 1


def test_duplicate_thread_title_is_a_field_level_400(auth_client, thread, article):
    response = auth_client.post(
        talk_url(article), {"title": "Lead is too technical", "body": "Again."}, format="json"
    )
    assert response.status_code == 400
    assert list(response.data) == ["title"]


@pytest.mark.parametrize(
    ("payload", "field"),
    [({"title": "ab", "body": "x"}, "title"), ({"title": "Valid title", "body": "   "}, "body")],
)
def test_thread_validation(auth_client, article, payload, field):
    response = auth_client.post(talk_url(article), payload, format="json")
    assert response.status_code == 400
    assert field in response.data


def test_resolved_filter(api_client, auth_client, article, thread):
    auth_client.post(talk_url(article), {"title": "Second topic", "body": "x"}, format="json")
    TalkThread.objects.filter(pk=thread["id"]).update(is_resolved=True)
    resolved = api_client.get(talk_url(article), {"resolved": "true"}).data["results"]
    assert [row["id"] for row in resolved] == [thread["id"]]
    open_rows = api_client.get(talk_url(article), {"resolved": "false"}).data["results"]
    assert [row["title"] for row in open_rows] == ["Second topic"]


# --------------------------------------------------------------------------- #
# Replies and counters
# --------------------------------------------------------------------------- #
def test_replies_update_every_counter(other_client, auth_client, article, thread):
    first = reload(thread["id"])
    response = other_client.post(
        reply_url(article, thread["id"]),
        {"body": "I agree.", "parent": thread["messages"][0]["id"]},
        format="json",
    )
    assert response.status_code == 201
    assert list(response.data) == MESSAGE_FIELDS
    assert response.data["depth"] == 1

    after = reload(thread["id"])
    assert after.message_count == 2
    assert after.participant_count == 2
    assert after.last_message_at >= first.last_message_at

    auth_client.post(reply_url(article, thread["id"]), {"body": "Thanks."}, format="json")
    after = reload(thread["id"])
    assert after.message_count == 3
    assert after.participant_count == 2  # same two people


def test_reply_depth_is_clamped_at_four(auth_client, article, thread):
    parent = thread["messages"][0]["id"]
    depths = []
    for _ in range(6):
        response = auth_client.post(
            reply_url(article, thread["id"]), {"body": "deeper", "parent": parent}, format="json"
        )
        assert response.status_code == 201
        parent = response.data["id"]
        depths.append(response.data["depth"])
    assert depths == [1, 2, 3, 4, 4, 4]


def test_reply_parent_from_another_thread_is_rejected(auth_client, article, thread):
    other = auth_client.post(
        talk_url(article), {"title": "Another thread", "body": "x"}, format="json"
    ).data
    response = auth_client.post(
        reply_url(article, thread["id"]),
        {"body": "cross-posted", "parent": other["messages"][0]["id"]},
        format="json",
    )
    assert response.status_code == 400
    assert "parent" in response.data


def test_reply_to_a_thread_of_another_article_is_404(auth_client, thread, user):
    from apps.articles.models import Article

    elsewhere = Article.objects.create(title="Elsewhere", content="x", author=user)
    response = auth_client.post(reply_url(elsewhere, thread["id"]), {"body": "x"}, format="json")
    assert response.status_code == 404


def test_editing_a_message_keeps_counters_and_marks_it_edited(auth_client, thread):
    message_id = thread["messages"][0]["id"]
    response = auth_client.patch(
        f"/api/talk/messages/{message_id}/", {"body": "Reworded opening."}, format="json"
    )
    assert response.status_code == 200
    assert response.data["body"] == "Reworded opening."
    assert response.data["edited_at"] is not None
    assert reload(thread["id"]).message_count == 1


def test_soft_deleting_a_message_recounts_the_thread(other_client, auth_client, article, thread):
    reply = other_client.post(
        reply_url(article, thread["id"]), {"body": "Off-topic."}, format="json"
    ).data
    assert reload(thread["id"]).participant_count == 2

    assert other_client.delete(f"/api/talk/messages/{reply['id']}/").status_code == 204
    after = reload(thread["id"])
    assert after.message_count == 1
    assert after.participant_count == 1
    assert TalkMessage.objects.filter(pk=reply["id"], is_deleted=True).exists()


def test_deleted_body_is_withheld_from_readers_but_not_staff(auth_client, staff_client, thread):
    message_id = thread["messages"][0]["id"]
    auth_client.delete(f"/api/talk/messages/{message_id}/")

    public = APIClient().get(f"/api/talk/threads/{thread['id']}/").data["messages"][0]
    assert public["is_deleted"] is True
    assert public["body"] is None
    moderated = staff_client.get(f"/api/talk/threads/{thread['id']}/").data["messages"][0]
    assert moderated["body"] == "Opening post."


def test_only_the_author_may_edit_or_delete_a_message(other_client, thread):
    message_id = thread["messages"][0]["id"]
    assert (
        other_client.patch(
            f"/api/talk/messages/{message_id}/", {"body": "hijack"}, format="json"
        ).status_code
        == 403
    )
    assert other_client.delete(f"/api/talk/messages/{message_id}/").status_code == 403


def test_a_deleted_message_is_closed_to_its_author(auth_client, thread):
    message_id = thread["messages"][0]["id"]
    auth_client.delete(f"/api/talk/messages/{message_id}/")
    response = auth_client.patch(
        f"/api/talk/messages/{message_id}/", {"body": "undo"}, format="json"
    )
    assert response.status_code == 403


# --------------------------------------------------------------------------- #
# Thread moderation
# --------------------------------------------------------------------------- #
def test_thread_detail(api_client, thread):
    response = api_client.get(f"/api/talk/threads/{thread['id']}/")
    assert response.status_code == 200
    assert list(response.data) == THREAD_FIELDS + ["article", "messages"]


def test_creator_may_resolve_and_rename(auth_client, thread):
    response = auth_client.patch(
        f"/api/talk/threads/{thread['id']}/",
        {"is_resolved": True, "title": "Lead is fixed"},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["is_resolved"] is True
    assert response.data["title"] == "Lead is fixed"


def test_non_staff_locking_is_a_field_level_400(auth_client, thread):
    response = auth_client.patch(
        f"/api/talk/threads/{thread['id']}/", {"is_locked": True}, format="json"
    )
    assert response.status_code == 400
    assert list(response.data) == ["is_locked"]
    assert reload(thread["id"]).is_locked is False


def test_other_users_cannot_change_a_thread(other_client, thread):
    response = other_client.patch(
        f"/api/talk/threads/{thread['id']}/", {"is_resolved": True}, format="json"
    )
    assert response.status_code == 403


def test_locked_thread_only_takes_staff_replies(staff_client, other_client, article, thread):
    assert (
        staff_client.patch(
            f"/api/talk/threads/{thread['id']}/", {"is_locked": True}, format="json"
        ).status_code
        == 200
    )
    blocked = other_client.post(reply_url(article, thread["id"]), {"body": "x"}, format="json")
    assert blocked.status_code == 400
    allowed = staff_client.post(
        reply_url(article, thread["id"]), {"body": "Closing note."}, format="json"
    )
    assert allowed.status_code == 201
    assert reload(thread["id"]).message_count == 2


# --------------------------------------------------------------------------- #
# The model method is the definition of the counters
# --------------------------------------------------------------------------- #
def test_touch_rederives_counters_from_rows(article, user, other_user):
    thread = TalkThread.objects.create(article=article, title="Direct")
    TalkMessage.objects.create(thread=thread, author=user, body="a")
    TalkMessage.objects.create(thread=thread, author=other_user, body="b")
    TalkMessage.objects.create(thread=thread, author=user, body="c", is_deleted=True)
    TalkThread.objects.filter(pk=thread.pk).update(message_count=99, participant_count=99)
    thread.refresh_from_db()

    thread.touch()

    thread.refresh_from_db()
    assert (thread.message_count, thread.participant_count) == (2, 2)
    latest = thread.messages.filter(is_deleted=False).order_by("-created_at").first()
    assert thread.last_message_at == latest.created_at


def test_talk_on_a_draft_is_hidden_from_readers(article, thread):
    from apps.articles.models import Article

    Article.objects.filter(pk=article.pk).update(is_published=False)
    reader = APIClient()
    assert reader.get(talk_url(article)).status_code == 404
    assert reader.get(f"/api/talk/threads/{thread['id']}/").status_code == 404
