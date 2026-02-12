from typing import Optional

from django.contrib.auth import login
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from ..openapi.examples import AUTH_REGISTRATION_REQUEST_EXAMPLE
from ..openapi.responses import (AUTH_REGISTER_CONFLICT_RESPONSE,
                                 AUTH_REGISTER_VALIDATION_RESPONSE,
                                 AUTH_REGISTERED_RESPONSE)
from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import RegisterSerializer
from ..utils.api import CustomAuthentication, CustomResponse


@extend_schema(
    auth=[],
    operation_id="Register",
    tags=["Authentication"],
    description="Allows new users to register by providing their details.",
    request=RegisterSerializer,
    examples=[AUTH_REGISTRATION_REQUEST_EXAMPLE],
    responses={
        201: AUTH_REGISTERED_RESPONSE,
        400: AUTH_REGISTER_VALIDATION_RESPONSE,
        409: AUTH_REGISTER_CONFLICT_RESPONSE,
    },
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> CustomResponse:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token_instance, token = AuthToken.objects.create(user)

            return CustomResponse(
                response_data={
                    "expiry": token_instance.expiry,
                    "token": token,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )

        errors = serializer.errors

        if "username" in errors:
            if "already exists" in str(errors["username"][0]):
                return CustomResponse(
                    response_status="error",
                    response_message="A user with that username already exists.",
                    status=status.HTTP_409_CONFLICT,
                )

        return CustomResponse(
            response_status="error",
            response_message=errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    auth=[],
    operation_id="Login",
    tags=["Authentication"],
    description="Allows users to login by providing their details.",
    request=AuthTokenSerializer,
    responses={
        200: OpenApiResponse(
            description="Success",
            response=CustomOpenAPIResponseSchema().get_schema(),
            examples=[
                OpenApiExample(
                    name="Successful login",
                    status_codes=["200"],
                    response_only=True,
                    value={
                        "status": "success",
                        "data": {
                            "expiry": "2026-01-20T07:21:39.160819Z",
                            "token": "2d54d895a9aaa0d4bd9d8052579e280e6e0da24f2.......",
                        },
                        "message": None,
                    },
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=CustomOpenAPIResponseSchema().get_schema(),
            examples=[
                OpenApiExample(
                    name="Username and password fields are required",
                    status_codes=["400"],
                    response_only=True,
                    value={
                        "status": "error",
                        "data": None,
                        "message": {
                            "username": ["This field is required."],
                            "password": ["This field is required."],
                        },
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Unauthorized",
            response=CustomOpenAPIResponseSchema().get_schema(),
            examples=[
                OpenApiExample(
                    name="Invalid provided credentials",
                    status_codes=["401"],
                    response_only=True,
                    value={
                        "status": "error",
                        "data": None,
                        "message": "Unable to log in with provided credentials.",
                    },
                ),
            ],
        ),
    },
)
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(
        self, request: Request, format: Optional[str] = None
    ) -> CustomResponse:
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            response = super().post(request, format=format)

            return CustomResponse(
                response_data=response.data,
                status=status.HTTP_200_OK,
            )

        non_field = serializer.errors.get("non_field_errors", [])

        if any(err.code == "authorization" for err in non_field):
            return CustomResponse(
                response_status="error",
                response_message="Unable to log in with provided credentials.",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return CustomResponse(
            response_status="error",
            response_message=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    operation_id="Logout",
    tags=["Authentication"],
    description="Allows users to logout by providing their token.",
    responses={
        200: OpenApiResponse(
            description="Success",
            response=CustomOpenAPIResponseSchema().get_schema(),
            examples=[
                OpenApiExample(
                    name="Successful logout",
                    status_codes=["200"],
                    response_only=True,
                    value={
                        "status": "success",
                        "data": None,
                        "message": "Logged out successfully.",
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Unauthorized",
            response=CustomOpenAPIResponseSchema().get_schema(),
            examples=[
                OpenApiExample(
                    name="Invalid provided credentials",
                    status_codes=["401"],
                    response_only=True,
                    value={
                        "status": "error",
                        "data": None,
                        "message": "Unable to log in with provided credentials.",
                    },
                ),
            ],
        ),
    },
)
class LogoutView(KnoxLogoutView):
    authentication_classes = [CustomAuthentication]

    def get_post_response(self, request: Request) -> CustomResponse:
        return CustomResponse(
            response_message="Logged out successfully.",
            status=status.HTTP_200_OK,
        )
