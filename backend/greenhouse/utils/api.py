from enum import Enum

from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework.exceptions import NotAuthenticated


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"


class CustomAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("token")

        if not token:
            msg = _("No credentials provided.")
            raise NotAuthenticated(msg)

        # Encode token since authenticate_credentials decodes it
        # I don't want to reimplement the method just to remove the decode
        # https://github.com/jazzband/django-rest-knox/blob/develop/knox/auth.py
        token = token.encode("utf-8")

        user, auth_token = self.authenticate_credentials(token)

        return (user, auth_token)
