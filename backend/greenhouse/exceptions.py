from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response.data = {"message": "Invalid token."}
        response.status_code = status.HTTP_401_UNAUTHORIZED

    if isinstance(exc, ValidationError) and response is not None:
        response.data = {"message": response.data}
        response.status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc, Http404):
        response.data = {"message": "Resource not found."}
        response.status_code = status.HTTP_404_NOT_FOUND

    return response
