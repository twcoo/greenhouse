from enum import Enum

from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework import exceptions


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"


class CustomAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("token")

        if not token:
            msg = _("No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)

        user, auth_token = self.authenticate_credentials(token.encode("utf-8"))

        return (user, auth_token)
