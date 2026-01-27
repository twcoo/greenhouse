from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (AuthenticationFailed, NotAuthenticated,
                                       ValidationError)
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

    if isinstance(exc, ValidationError) and response is not None:
        errors = exc.detail

        if any("already exists." in str(msg) for msg in errors.values()):
            return CustomResponse(
                response_status="error",
                status=status.HTTP_409_CONFLICT,
                response_message=response.data,
            )

        return CustomResponse(
            response_status="error",
            status=status.HTTP_400_BAD_REQUEST,
            response_message=response.data,
        )

    if isinstance(exc, Http404):
        return CustomResponse(
            response_status="error",
            status=status.HTTP_404_NOT_FOUND,
            response_message="Resource not found.",
        )

    return response
