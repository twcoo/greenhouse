from django.contrib.auth import get_user_model
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class RequiredAuthTestsMixin:
    url: str
    http_method: str = "GET"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="shimmer", password="ShimmerDontJump!"
        )
        self.token_instance, self.token = AuthToken.objects.create(self.user)

    def _request(self):
        return self.client.generic(method=self.http_method, path=self.url)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_required_auth_header(self):
        response = self._request()

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            "Authentication credentials were not provided.",
        )

    def test_required_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token Invalid Token")

        response = self._request()

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_json["data"])
        self.assertEqual(response_json["message"], "Invalid token.")
