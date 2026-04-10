from typing import Optional

from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from ..openapi.examples import AUTH_LOGIN_REQUEST_EXAMPLE
from ..openapi.parameters import CSRFTOKEN_PARAM
from ..openapi.responses import (AUTH_LOGIN_RESPONSE,
                                 AUTH_LOGIN_UNAUTHORIZED_RESPONSE,
                                 AUTH_LOGIN_VALIDATION_RESPONSE,
                                 AUTH_LOGOUT_RESPONSE,
                                 AUTH_LOGOUT_UNAUTHORIZED_RESPONSE)
from ..serializers import KnoxLoginRequestSerializer
from ..utils.api import CustomAuthentication
from ..utils.cookie import get_token_max_age


@extend_schema(
    auth=[],
    operation_id="Login",
    tags=["Authentication"],
    description="Allows users to login by providing their details.",
    request=KnoxLoginRequestSerializer,
    examples=[AUTH_LOGIN_REQUEST_EXAMPLE],
    responses={
        200: AUTH_LOGIN_RESPONSE,
        400: AUTH_LOGIN_VALIDATION_RESPONSE,
        401: AUTH_LOGIN_UNAUTHORIZED_RESPONSE,
    },
)
class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request: Request, format: Optional[str] = None) -> Response:
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            knox_response = super().post(request, format=format)

            token = knox_response.data["token"]

            response = Response(
                {
                    "user": {"username": user.username},
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="token",
                value=token,
                httponly=True,
                max_age=get_token_max_age(),
            )

            return response

        non_field = serializer.errors.get("non_field_errors", [])

        if any(err.code == "authorization" for err in non_field):
            return Response(
                {"message": "Unable to log in with provided credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {"message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    operation_id="Logout",
    tags=["Authentication"],
    description="Allows users to logout by providing their token.",
    parameters=CSRFTOKEN_PARAM,
    responses={
        200: AUTH_LOGOUT_RESPONSE,
        401: AUTH_LOGOUT_UNAUTHORIZED_RESPONSE,
    },
)
@method_decorator(csrf_protect, name="dispatch")
class LogoutView(KnoxLogoutView):
    authentication_classes = [CustomAuthentication]

    def get_post_response(self, request: Request) -> Response:
        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )
