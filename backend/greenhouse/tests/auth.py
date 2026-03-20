from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.mixins import ResponseUtilsMixin

User = get_user_model()


class AuthLoginTests(ResponseUtilsMixin, APITestCase):
    def setUp(self):
        self.username = "jesse"
        self.password = "IAmAlive12"

        User.objects.create_user(username=self.username, password=self.password)

        self.url = reverse("login")

    def test_login_success(self):
        response = self.client.post(
            self.url,
            {"username": self.username, "password": self.password},
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertIsNone(data)
        self.assertEqual(message, "Login successful")

    def test_login_error(self):
        response = self.client.post(
            self.url,
            {"username": "invalid_username", "password": "invalid_password"},
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            "Unable to log in with provided credentials.",
            message,
        )

    def test_required_fields_error(self):
        response = self.client.post(
            self.url,
            {
                "invalid_field_1": None,
                "invalid_field_2": None,
            },
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
            },
            message,
        )


class AuthLogoutTests(ResponseUtilsMixin, APITestCase):
    def setUp(self):
        self.username = "ellieW"
        self.password = "IAmAloneNow"

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.logout_url = reverse("logout")

        self.token_instance, self.token = AuthToken.objects.create(self.user)

    def authenticate(self):
        self.client.cookies["token"] = self.token

    def test_logout_success(self):
        self.authenticate()

        response = self.client.post(self.logout_url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("success", response_status)
        self.assertIsNone(data)
        self.assertEqual("Logged out successfully.", message)

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            "No credentials provided.",
            message,
        )

    def test_logout_with_invalid_token(self):
        self.client.cookies["token"] = "Invalid token"

        response = self.client.post(self.logout_url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual("Invalid token.", message)

    def test_token_is_invalidated_after_logout(self):
        self.authenticate()

        self.client.post(self.logout_url)

        response = self.client.post(self.logout_url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual("Invalid token.", message)
