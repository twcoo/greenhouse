from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthRegisterTests(APITestCase):
    def setUp(self):
        self.existing_username = "tommyM"
        self.existing_username_password = "DearMaria12"
        self.url = reverse("register")

        User.objects.create_user(
            username=self.existing_username,
            password=self.existing_username_password,
        )

    def test_register_success(self):
        response = self.client.post(
            self.url,
            {"username": "joelM", "password": "MightyThinIce12"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertIn("expiry", response.data["data"])
        self.assertEqual("success", response.data["status"])
        self.assertIsNone(response.data["message"])

    def test_existing_user_error(self):
        response = self.client.post(
            self.url,
            {
                "username": self.existing_username,
                "password": self.existing_username_password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual("error", response.data["status"])
        self.assertEqual(
            "A user with that username already exists.",
            response.data["message"],
        )
        self.assertIsNone(response.data["data"])

    def test_required_fields_error(self):
        response = self.client.post(
            self.url,
            {
                "invalid_field_1": None,
                "invalid_field_2": None,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
            },
            response.data["message"],
        )
        self.assertEqual("error", response.data["status"])
        self.assertIsNone(response.data["data"])


class AuthLoginTests(APITestCase):
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data["data"])
        self.assertIn("expiry", response.data["data"])
        self.assertEqual("success", response.data["status"])
        self.assertIsNone(response.data["message"])

    def test_login_error(self):
        response = self.client.post(
            self.url,
            {"username": "invalid_username", "password": "invalid_password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertEqual(
            "Unable to log in with provided credentials.",
            response.data["message"],
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
            },
            response.data["message"],
        )
        self.assertEqual("error", response.data["status"])
        self.assertIsNone(response.data["data"])


class AuthLogoutTests(APITestCase):
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
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_logout_success(self):
        self.authenticate()

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("success", response.data["status"])
        self.assertIsNone(response.data["data"])

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("error", response.data["status"])
        self.assertIsNone(response.data["data"])
        self.assertEqual(
            "Authentication credentials were not provided.",
            response.data["message"],
        )

    def test_logout_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken123")

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("error", response.data["status"])
        self.assertIsNone(response.data["data"])

    def test_token_is_invalidated_after_logout(self):
        self.authenticate()

        self.client.post(self.logout_url)

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertEqual(
            "Invalid token.",
            response.data["message"],
        )
