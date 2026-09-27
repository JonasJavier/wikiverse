"""Permission classes for the wiki.

The editing model is deliberately **wiki-open**: any signed-in user may edit any
unprotected article, whoever wrote it. What is *not* open:

* anonymous users read everything and write nothing — there is no CAPTCHA, no
  abuse filter and no IP blocklist here, so an unauthenticated write path would
  be a defacement surface with no recovery kit;
* deletion is author-or-staff, because a soft delete hides other people's
  revisions too;
* ``protection`` and ``is_published`` are gated in the **serializer**, at field
  level, returning 400 — not here. A non-author editor *is* allowed to edit the
  article; they are only not allowed to change its status, and an object-level
  403 would say the wrong thing (DECISIONS §15).
"""

from __future__ import annotations

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Article, TalkMessage, TalkThread

__all__ = [
    "CanEditArticle",
    "CanPostToTalk",
    "IsAuthorOrStaffOrReadOnly",
    "IsMessageAuthorOrStaff",
    "IsThreadOwnerOrStaff",
]


class CanEditArticle(permissions.BasePermission):
    """Wiki-open editing, with protection levels and author-only deletion."""

    message = "You do not have permission to edit this article."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        if request.method == "DELETE":
            # A soft delete hides every contributor's work on the page, not just
            # the requester's, so it stays with the page's creator and staff.
            self.message = "Only the article's author or staff may delete it."
            return obj.author_id == user.id
        if obj.protection == Article.Protection.FULL:
            self.message = "This article is fully protected; only staff may edit it."
            return False
        if (
            obj.protection == Article.Protection.SEMI
            and (user.edit_count or 0) < Article.SEMI_PROTECT_MIN_EDITS
        ):
            self.message = (
                "This article is semi-protected. Make a few edits elsewhere first "
                f"({Article.SEMI_PROTECT_MIN_EDITS} are needed)."
            )
            return False
        return True


class IsAuthorOrStaffOrReadOnly(CanEditArticle):
    """Historical name for :class:`CanEditArticle`, kept so imports do not break."""


class CanPostToTalk(permissions.BasePermission):
    """Signed-in users may post, unless the thread is locked. Staff always may."""

    message = "You must be signed in to post to a talk page."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def allows_thread(self, request: Request, thread: TalkThread) -> bool:
        """Whether ``request`` may add to ``thread``. Called from the view.

        Not ``has_object_permission``: the object being created is a message and
        the lock lives on its parent thread, which DRF's object-permission hook
        never sees.
        """
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        return not thread.is_locked


class IsThreadOwnerOrStaff(permissions.BasePermission):
    """Renaming or resolving a thread is for its creator; locking is staff-only."""

    message = "Only the thread's author or staff may change it."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: APIView, obj: TalkThread) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        return obj.created_by_id == user.id


class IsMessageAuthorOrStaff(permissions.BasePermission):
    """Own message only, and an already-deleted message is closed to non-staff."""

    message = "Only the message's author or staff may change it."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: APIView, obj: TalkMessage) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        if obj.is_deleted:
            self.message = "This message has been deleted."
            return False
        return obj.author_id == user.id
