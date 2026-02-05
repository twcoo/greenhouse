from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.factories import CropFactory
from .commons.mixins import RequiredAuthTestsMixin


class CropListApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")

    def test_list_empty_crops(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["results"], [])
        self.assertEqual(response.data["message"], None)

    def test_list_populated_crops(self):
        self.authenticate()

        CropFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 3)
        self.assertEqual(response.data["message"], None)

    def test_list_pagination(self):
        self.authenticate()
        CropFactory.create_batch(15)

        response = self.client.get(self.url, {"page_size": 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 10)
        self.assertEqual(response.data["message"], None)
