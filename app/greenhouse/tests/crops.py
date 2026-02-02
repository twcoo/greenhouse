from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.mixins import RequiredAuthTestsMixin


class CropListApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")

    def test_get_crops(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
