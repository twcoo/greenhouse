from django.contrib.auth import login
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ..serializers import RegisterSerializer
from ..utils.api import CustomOpenAPIResponseSchema, CustomResponse


@extend_schema(
    auth=[],
    operation_id="Register",
    tags=["Authentication"],
    description="Allows new users to register by providing their details.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description="Success",
            response=CustomOpenAPIResponseSchema(
                response_data_properties={
                    "expiry": {
                        "type": "string(datetime)",
                        "description": "Token expiration timestamp in ISO 8601 UTC format. The token becomes invalid after this time.",
                    },
                    "token": {
                        "type": "string",
                        "description": "Authentication token used for API requests.",
                    },
                },
                response_data_required_properties=["access_token"],
            ).get_schema(),
            examples=[
                OpenApiExample(
                    name="Successful registration",
                    status_codes=["201"],
                    response_only=True,
                    value={
                        "status": "success",
                        "data": {
                            "expiry": "2026-01-20T06:46:33.891979Z",
                            "token": "a2f69c052c2b1a549dbdc458cbe34f5d0c9570919.......",
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
                    name="Username is already registered",
                    status_codes=["400"],
                    response_only=True,
                    value={
                        "status": "error",
                        "data": None,
                        "message": {
                            "username": [
                                "A user with that username already exists."
                            ]
                        },
                    },
                ),
                OpenApiExample(
                    name="Username and password are required",
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
    },
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
                    "username": user.username,
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
