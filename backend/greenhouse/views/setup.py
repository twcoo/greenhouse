from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from knox.models import AuthToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..openapi.examples import SETUP_ADMIN_REQUEST_EXAMPLE
from ..openapi.responses import (SETUP_ADMIN_CREATED_RESPONSE,
                                 SETUP_ADMIN_VALIDATION_RESPONSE,
                                 SETUP_STATUS_OK_RESPONSE,
                                 SETUP_STATUS_VALIDATION_RESPONSE)
from ..serializers import RegisterSerializer

User = get_user_model()


@extend_schema(
    auth=[],
    operation_id="Setup Admin",
    tags=["Setup"],
    description="Allows creation of the first admin user.",
    request=RegisterSerializer,
    examples=[SETUP_ADMIN_REQUEST_EXAMPLE],
    responses={
        201: SETUP_ADMIN_CREATED_RESPONSE,
        400: SETUP_ADMIN_VALIDATION_RESPONSE,
    },
)
class SetupAdminView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token_instance, token = AuthToken.objects.create(user)

            return Response(
                {
                    "expiry": token_instance.expiry,
                    "token": token,
                    "user": {"username": user.username},
                },
                status=status.HTTP_201_CREATED,
            )

        errors = serializer.errors

        return Response({"message": errors}, status.HTTP_400_BAD_REQUEST)


@extend_schema(
    auth=[],
    operation_id="Setup Status",
    tags=["Setup"],
    description="Checks whether the initial setup is required.",
    responses={
        200: SETUP_STATUS_OK_RESPONSE,
        400: SETUP_STATUS_VALIDATION_RESPONSE,
    },
)
class SetupStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        admin_user_exists = User.objects.filter(
            is_superuser=True, is_staff=False
        ).exists()

        if not admin_user_exists:
            return Response({"message": "Setup required."}, status.HTTP_400_BAD_REQUEST)

        return Response({"message": "ok"}, status.HTTP_200_OK)
