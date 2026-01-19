from django.contrib.auth import login
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import RegisterSerializer
from ..utils.api import CustomOpenAPIResponseSchema, CustomResponse


@extend_schema(
    auth=[],
    operation_id="Register",
    tags=["Authentication"],
    description="Allows new users to register by providing their details.",
    request=RegisterSerializer,
    responses={200: OpenApiResponse(description="Success")},
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token_instance, token = AuthToken.objects.create(user)

            return CustomResponse(
                response_data={
                    "expiry": token_instance.expiry,
                    "token": token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return CustomResponse(
            response_status="error",
            response_message=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    auth=[],
    operation_id="Login",
    tags=["Authentication"],
    description="Allows new users to login by providing their details.",
    request=AuthTokenSerializer,
)
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse(
                response_status="error",
                response_message=serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = serializer.validated_data["user"]
        login(request, user)

        response = super().post(request, format=format)

        response.data.update(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }
        )

        return CustomResponse(
            response_data=response.data,
            status=status.HTTP_200_OK,
        )
