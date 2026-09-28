"""Account endpoints.

``login`` and ``register`` carry :class:`~apps.common.throttling.LoginThrottle`
and :class:`~apps.common.throttling.RegisterThrottle`, which key on the submitted
username *as well as* the client IP. The backend is reachable at its own
``*.up.railway.app`` host, so an attacker can rotate ``X-Forwarded-For`` freely;
an IP-only bucket would reset on every request (DECISIONS §7.5).
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common.throttling import LoginThrottle, RegisterThrottle

from .serializers import (
    CustomTokenObtainPairSerializer,
    LoginResponseSerializer,
    LogoutSerializer,
    PublicUserSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


@extend_schema(tags=["auth"])
class RegisterView(generics.CreateAPIView):
    """Create an account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]


@extend_schema(tags=["auth"], responses=LoginResponseSerializer)
class LoginView(TokenObtainPairView):
    """Obtain an access/refresh pair, with the user object embedded."""

    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginThrottle]


@extend_schema(tags=["auth"], request=LogoutSerializer, responses={204: None})
class LogoutView(APIView):
    """Blacklist a refresh token.

    ``AllowAny`` on purpose: the refresh token *is* the credential being revoked,
    and requiring a live access token would mean a user whose access token had
    already expired could never revoke their refresh token.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["auth"])
class MeView(generics.RetrieveUpdateAPIView):
    """Read or update the caller's own profile. The only place ``email`` is served."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["auth"], responses=PublicUserSerializer)
class PublicProfileView(generics.RetrieveAPIView):
    """Anyone's public profile, by username.

    ``article_count`` is annotated rather than read from the model property: the
    property runs one ``COUNT`` per instance, and the filter on
    ``is_published``/``is_deleted`` is what stops a profile leaking the existence
    of somebody's drafts. The annotation is deliberately *not* called
    ``article_count`` — that name is a property with no setter, so Django would
    raise while assigning it to the row.
    """

    serializer_class = PublicUserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "username"

    def get_queryset(self):
        return User.objects.annotate(
            annotated_article_count=Count(
                "articles",
                filter=Q(articles__is_published=True, articles__is_deleted=False),
                distinct=True,
            )
        )
