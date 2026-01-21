from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler

from .utils.api import CustomResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return CustomResponse(
            response_status="error",
            response_message="Authentication credentials were not provided.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, AuthenticationFailed):
        return CustomResponse(
            response_status="error",
            response_message="Unable to log in with provided credentials.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
