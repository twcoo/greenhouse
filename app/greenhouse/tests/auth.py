from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from loguru import logger
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class AuthRegisterTests(APITestCase):
    def setUp(self):
        self.existing_username = "tommyM"
        self.existing_username_password = "DearMaria12"
        self.url = reverse("register")

        User.objects.create_user(
            username=self.existing_username, password=self.existing_username_password
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
        self.assertEqual(None, response.data["message"])

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
            "A user with that username already exists.", response.data["message"]
        )
        self.assertEqual(None, response.data["data"])

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
        self.assertEqual(None, response.data["data"])
