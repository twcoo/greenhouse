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
        self.assertEqual(response.data["data"]["count"], 0)
        self.assertIsNone(response.data["data"]["next"])
        self.assertIsNone(response.data["data"]["previous"])
        self.assertIsNone(response.data["message"])

    def test_list_populated_crops(self):
        self.authenticate()

        CropFactory.create_batch(3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 3)
        self.assertIsNone(response.data["message"])

    def test_list_pagination(self):
        self.authenticate()
        CropFactory.create_batch(15)

        response = self.client.get(self.url, {"page_size": 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 10)
        self.assertEqual(response.data["data"]["count"], 15)
        self.assertIsNotNone(response.data["data"]["next"])
        self.assertIsNone(response.data["data"]["previous"])
        self.assertIsNone(response.data["message"])


class CropCreateApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")

    def test_create_crop_success(self):
        self.authenticate()

        payload = {
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
