from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from ..models import Crop
from .commons.factories import CropFactory
from .commons.mixins import RequiredAuthTestsMixin

INVALID_FIELD_TYPE_MESSAGE = {
    "name": [
        ErrorDetail(string="Name must be a valid string.", code="invalid")
    ],
    "scientific_name": [
        ErrorDetail(
            string="Scientific name must be a valid string.",
            code="invalid",
        )
    ],
    "category": [
        ErrorDetail(
            string='"INVALID_VALUE" is not a valid choice.',
            code="invalid_choice",
        )
    ],
    "sunlight_requirement": [
        ErrorDetail(
            string='"INVALID_VALUE" is not a valid choice.',
            code="invalid_choice",
        )
    ],
}


class CropListApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")

    def test_list_empty_crops(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["data"]["results"], [])
        self.assertEqual(response_json["data"]["count"], 0)
        self.assertIsNone(response_json["data"]["next"])
        self.assertIsNone(response_json["data"]["previous"])
        self.assertIsNone(response_json["message"])

    def test_list_populated_crops(self):
        self.authenticate()

        CropFactory.create_batch(3)

        response = self.client.get(self.url)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json["data"]["results"]), 3)
        self.assertIsNone(response_json["message"])

    def test_list_pagination(self):
        self.authenticate()
        CropFactory.create_batch(15)

        response = self.client.get(self.url, {"page_size": 10})

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json["data"]["results"]), 10)
        self.assertEqual(response_json["data"]["count"], 15)
        self.assertIsNotNone(response_json["data"]["next"])
        self.assertIsNone(response_json["data"]["previous"])
        self.assertIsNone(response_json["message"])


class CropCreateApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")
        self.tomato_payload = {
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        }

    def test_create_crop_success(self):
        self.authenticate()

        response = self.client.post(
            self.url, self.tomato_payload, format="json"
        )

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["status"], "success")

        data = response_json["data"]
        self.assertIsNotNone(data["id"])
        del data["id"]
        self.assertEqual(response_json["data"], self.tomato_payload)

        self.assertIsNone(response_json["message"])

        self.assertTrue(Crop.objects.filter(name="Tomato").exists())

    def test_create_crop_missing_required_field(self):
        self.authenticate()

        payload = {"name": "Tomato"}

        response = self.client.post(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {
                "scientific_name": ["This field is required."],
                "category": ["This field is required."],
                "sunlight_requirement": ["This field is required."],
                "min_days_to_harvest": ["This field is required."],
                "max_days_to_harvest": ["This field is required."],
            },
        )

    def test_create_crop_duplicate_name(self):
        self.authenticate()

        CropFactory(name="Tomato")

        response = self.client.post(
            self.url, self.tomato_payload, format="json"
        )

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {"name": ["A crop with this name already exists."]},
        )

    def test_create_crop_duplicate_scientific_name(self):
        self.authenticate()

        CropFactory(scientific_name="Solanum lycopersicum")

        response = self.client.post(
            self.url, self.tomato_payload, format="json"
        )

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {
                "scientific_name": [
                    "A crop with this scientific name already exists."
                ]
            },
        )

    def test_create_crop_invalid_field_values(self):
        self.authenticate()

        payload = {
            "name": 1,
            "scientific_name": 1,
            "category": "INVALID_VALUE",
            "sunlight_requirement": "INVALID_VALUE",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        }

        response = self.client.post(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(response_json["message"], INVALID_FIELD_TYPE_MESSAGE)

    def test_validation_error_when_min_days_to_harvest_exceeds_max(self):
        self.authenticate()
        payload = {
            "name": "Lettuce",
            "scientific_name": "Lactuca sativa",
            "category": "VEGETABLE",
            "sunlight_requirement": "PART SUN",
            "min_days_to_harvest": 20,
            "max_days_to_harvest": 10,
        }

        response = self.client.post(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropGetApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory()
        self.url = reverse("crop-detail", args=[self.crop.id])  # type: ignore[attr-defined]
        self.url_not_found = reverse("crop-detail", args=[2])

    def test_get_crop(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json["data"],
            {
                "id": self.crop.id,  # type: ignore[attr-defined]
                "name": self.crop.name,
                "scientific_name": self.crop.scientific_name,
                "category": self.crop.category,
                "sunlight_requirement": self.crop.sunlight_requirement,
                "min_days_to_harvest": self.crop.min_days_to_harvest,
                "max_days_to_harvest": self.crop.max_days_to_harvest,
            },
        )
        self.assertIsNone(response_json["message"])

    def test_get_crop_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(
            response_json["data"],
        )
        self.assertEqual(response_json["message"], "Resource not found.")


class CropUpdateApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory()
        self.url = reverse("crop-detail", args=[self.crop.id])  # type: ignore[attr-defined]
        self.url_not_found = reverse("crop-detail", args=[2])
        self.payload = {
            "name": "Cucumber",
            "scientific_name": "Cucumis sativus",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 50,
            "max_days_to_harvest": 70,
        }

    def test_update_crop(self):
        self.authenticate()

        response = self.client.put(self.url, self.payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json["data"],
            {
                "id": self.crop.id,  # type: ignore[attr-defined]
                **self.payload,
            },
        )
        self.assertIsNone(response_json["message"])

    def test_update_crop_not_found(self):
        self.authenticate()

        response = self.client.put(self.url_not_found, self.payload)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(
            response_json["data"],
        )
        self.assertEqual(response_json["message"], "Resource not found.")

    def test_update_crop_invalid_field_values(self):
        self.authenticate()

        payload = {
            "name": 1,
            "scientific_name": 1,
            "category": "INVALID_VALUE",
            "sunlight_requirement": "INVALID_VALUE",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        }

        response = self.client.put(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(response_json["message"], INVALID_FIELD_TYPE_MESSAGE)

    def test_validation_error_when_min_days_to_harvest_exceeds_max(self):
        self.authenticate()

        payload = self.payload

        payload["min_days_to_harvest"] = 1000

        response = self.client.put(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropPartialUpdateApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(min_days_to_harvest=20)
        self.url = reverse("crop-detail", args=[self.crop.id])  # type: ignore[attr-defined]
        self.url_not_found = reverse("crop-detail", args=[2])
        self.payload = {
            "min_days_to_harvest": 50,
        }

    def test_partially_update_crop(self):
        self.authenticate()

        response = self.client.patch(self.url, self.payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json["data"],
            {
                "id": self.crop.id,  # type: ignore[attr-defined]
                "name": self.crop.name,
                "scientific_name": self.crop.scientific_name,
                "category": self.crop.category,
                "sunlight_requirement": self.crop.sunlight_requirement,
                **self.payload,
                "max_days_to_harvest": self.crop.max_days_to_harvest,
            },
        )
        self.assertIsNone(response_json["message"])

    def test_update_crop_not_found(self):
        self.authenticate()

        response = self.client.patch(self.url_not_found, self.payload)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(
            response_json["data"],
        )
        self.assertEqual(response_json["message"], "Resource not found.")

    def test_update_crop_invalid_field_values(self):
        self.authenticate()

        payload = {
            "name": 1,
            "scientific_name": 1,
            "category": "INVALID_VALUE",
            "sunlight_requirement": "INVALID_VALUE",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        }

        response = self.client.patch(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(response_json["message"], INVALID_FIELD_TYPE_MESSAGE)

    def test_validation_error_when_min_days_to_harvest_exceeds_max(self):
        self.authenticate()

        payload = self.payload

        payload = {"min_days_to_harvest": 1000}

        response = self.client.patch(self.url, payload, format="json")

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["status"], "error")
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropDeleteApiViewTests(RequiredAuthTestsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory()
        self.url = reverse("crop-detail", args=[self.crop.id])  # type: ignore[attr-defined]
        self.url_not_found = reverse("crop-detail", args=[2])

    def test_delete_crop(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_delete_crop_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(
            response_json["data"],
        )
        self.assertEqual(response_json["message"], "Resource not found.")
