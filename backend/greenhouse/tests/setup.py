from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.factories import UserFactory
from .commons.mixins import ResponseUtilsMixin

User = get_user_model()


class SetupAdminTests(ResponseUtilsMixin, APITestCase):
    def setUp(self):
        self.url = reverse("setup_admin")

    def test_register_success(self):
        response = self.client.post(
            self.url,
            {
                "username": "joelM",
                "password": "MightyThinIce12",
                "password2": "MightyThinIce12",
            },
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIn("token", data)
        self.assertIn("expiry", data)
        self.assertIn("user", data)
        self.assertIsNone(message)

    def test_existing_admin_user_error(self):
        UserFactory()

        response = self.client.post(
            self.url,
            {
                "username": "newAdminUser",
                "password": "newAdminUserPassword",
                "password2": "newAdminUserPassword",
            },
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_status,
            "error",
        )
        self.assertIsNone(data)
        self.assertEqual(
            {
                "non_field_errors": [
                    "Admin user already exists. Setup cannot be run again."
                ]
            },
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
        self.assertEqual(
            response_status,
            "error",
        )
        self.assertIsNone(data)
        self.assertEqual(
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
                "password2": ["This field is required."],
            },
            message,
        )

    def test_register_confirm_password_error(self):
        response = self.client.post(
            self.url,
            {
                "username": "joelM",
                "password": "MightyThinIce12",
                "password2": "MightyThinIce",
            },
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            {"password2": ["Passwords do not match."]},
            message,
        )
