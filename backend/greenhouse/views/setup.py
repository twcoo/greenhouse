from drf_spectacular.utils import extend_schema
from knox.models import AuthToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..openapi.examples import SETUP_ADMIN_REQUEST_EXAMPLE
from ..openapi.responses import (SETUP_ADMIN_CREATED_RESPONSE,
                                 SETUP_ADMIN_VALIDATION_RESPONSE)
from ..serializers import RegisterSerializer
from ..utils.renderers import JSendRenderer


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
    renderer_classes = [JSendRenderer]

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
