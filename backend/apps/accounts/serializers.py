"""Account serializers.

There are deliberately **two** user shapes, and the difference is the point:

* :class:`UserSerializer` is the caller's own record (``/api/auth/me/``, and the
  ``user`` object embedded in a login response). It carries ``email`` and
  ``is_staff``.
* :class:`PublicUserSerializer` is anybody's profile. It carries neither. A
  single serializer used for both is how an email address ends up on a public
  profile page, and ``is_staff`` on a public profile hands an attacker a list of
  accounts worth phishing.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class PublicUserSerializer(serializers.ModelSerializer):
    """Anyone's profile. No ``email``, no ``is_staff`` — ever.

    ``article_count`` prefers the view's annotation and falls back to the model
    property, so this serializer is safe on a bare instance as well as on an
    annotated queryset. The annotation cannot be *called* ``article_count``:
    ``User.article_count`` is a read-only property, and Django assigns annotations
    with ``setattr``, so an annotation of that name raises
    ``AttributeError: property 'article_count' ... has no setter`` while building
    the row.
    """

    article_count = serializers.SerializerMethodField()
    edit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "bio",
            "avatar",
            "is_bot",
            "article_count",
            "edit_count",
            "date_joined",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.IntegerField())
    def get_article_count(self, obj) -> int:
        annotated = getattr(obj, "annotated_article_count", None)
        return obj.article_count if annotated is None else annotated


class UserSerializer(serializers.ModelSerializer):
    """The caller's own record.

    ``is_staff`` is read-only and lives here only (critique #22): the article page
    shows Delete when ``user.is_staff`` or the user is the author, so the client
    needs the flag for itself — and for nobody else.
    """

    article_count = serializers.IntegerField(read_only=True)
    edit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "is_staff",
            "is_bot",
            "article_count",
            "edit_count",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "email",
            "is_staff",
            "is_bot",
            "date_joined",
            "article_count",
            "edit_count",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm", "bio")

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login response with the user embedded, so the client needs one round trip."""

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user, context=self.context).data
        return data


class LoginResponseSerializer(serializers.Serializer):
    """Schema-only: the shape :class:`CustomTokenObtainPairSerializer` returns."""

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)


class LogoutSerializer(serializers.Serializer):
    """``POST /api/auth/logout/`` — blacklist the refresh token (DECISIONS §7.2).

    Clearing the client's storage is not logging out: with
    ``ROTATE_REFRESH_TOKENS`` on, a refresh token that is merely forgotten stays
    valid for its whole two-day lifetime, so a copy taken from storage still
    mints access tokens. Blacklisting is what actually ends the session.
    """

    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value: str) -> str:
        try:
            self.token = RefreshToken(value)
        except TokenError as exc:
            raise serializers.ValidationError("That refresh token is not valid.") from exc
        return value

    def save(self, **kwargs) -> None:
        self.token.blacklist()
