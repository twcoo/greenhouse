from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CropListApiViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("crop-list-create")

    def test_required_auth_header(self):
        response = self.client.get(
            self.url,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertEqual(
            response.data["message"],
            "Authentication credentials were not provided.",
        )

    def test_required_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token Invalid Token")

        response = self.client.get(
            self.url,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertEqual(response.data["message"], "Invalid token.")
