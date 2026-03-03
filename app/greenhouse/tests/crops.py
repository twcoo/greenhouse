import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from ..models import Crop
from .commons.factories import CropFactory, UserFactory
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin
from .commons.utils import ImageUploadAPITestCase

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


class CropListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("crop-list-create")
        self.another_user = UserFactory(username="shimmer2")
        self.another_user_crops = CropFactory.create_batch(
            12, user=self.another_user
        )

    def test_list_empty_crops(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, crops, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(crops, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=crops, another_user_data=self.another_user_crops
        )

    def test_list_populated_crops(self):
        self.authenticate()

        CropFactory.create_batch(3, user=self.user)

        response = self.client.get(self.url)

        response_status, data, crops, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(crops), 3)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=crops, another_user_data=self.another_user_crops
        )

    def test_list_pagination(self):
        self.authenticate()
        CropFactory.create_batch(15, user=self.user)

        response = self.client.get(self.url, {"page_size": 10})

        response_status, data, crops, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(crops), 10)
        self.assertEqual(data["count"], 15)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=crops, another_user_data=self.another_user_crops
        )


class CropCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        del data["id"]
        self.assertEqual(data, self.tomato_payload)
        self.assertTrue(
            Crop.objects.filter(name=self.tomato_payload["name"]).exists()
        )
        crop = Crop.objects.get(name=self.tomato_payload["name"])
        self.assertEqual(crop.user_id, self.user.id)
        self.assertIsNone(message)

    def test_create_crop_missing_required_field(self):
        self.authenticate()

        payload = {"name": "Tomato"}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
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

        CropFactory(name="Tomato", user=self.user)

        response = self.client.post(
            self.url, self.tomato_payload, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"name": ["A crop with this name already exists."]},
        )

    def test_create_crop_duplicate_scientific_name(self):
        self.authenticate()

        CropFactory(scientific_name="Solanum lycopersicum", user=self.user)

        response = self.client.post(
            self.url, self.tomato_payload, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, INVALID_FIELD_TYPE_MESSAGE)

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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.url = reverse("crop-detail", args=[self.crop.id])
        self.url_not_found = reverse("crop-detail", args=[2])

    def test_get_crop(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.crop.id,
                "name": self.crop.name,
                "scientific_name": self.crop.scientific_name,
                "category": self.crop.category,
                "sunlight_requirement": self.crop.sunlight_requirement,
                "min_days_to_harvest": self.crop.min_days_to_harvest,
                "max_days_to_harvest": self.crop.max_days_to_harvest,
            },
        )
        self.assertIsNone(message)

    def test_get_crop_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(
            data,
        )
        self.assertEqual(message, "Resource not found.")


class CropUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.url = reverse("crop-detail", args=[self.crop.id])
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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.crop.id,
                **self.payload,
            },
        )
        self.assertIsNone(message)

    def test_update_crop_not_found(self):
        self.authenticate()

        response = self.client.put(self.url_not_found, self.payload)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(
            data,
        )
        self.assertEqual(message, "Resource not found.")

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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, INVALID_FIELD_TYPE_MESSAGE)

    def test_validation_error_when_min_days_to_harvest_exceeds_max(self):
        self.authenticate()

        payload = self.payload

        payload["min_days_to_harvest"] = 1000

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropPartialUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(min_days_to_harvest=20, user=self.user)
        self.url = reverse("crop-detail", args=[self.crop.id])
        self.url_not_found = reverse("crop-detail", args=[2])
        self.payload = {
            "min_days_to_harvest": 50,
        }

    def test_partially_update_crop(self):
        self.authenticate()

        response = self.client.patch(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.crop.id,
                "name": self.crop.name,
                "scientific_name": self.crop.scientific_name,
                "category": self.crop.category,
                "sunlight_requirement": self.crop.sunlight_requirement,
                **self.payload,
                "max_days_to_harvest": self.crop.max_days_to_harvest,
            },
        )
        self.assertIsNone(message)

    def test_update_crop_not_found(self):
        self.authenticate()

        response = self.client.patch(self.url_not_found, self.payload)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(
            data,
        )
        self.assertEqual(message, "Resource not found.")

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

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, INVALID_FIELD_TYPE_MESSAGE)

    def test_validation_error_when_min_days_to_harvest_exceeds_max(self):
        self.authenticate()

        payload = self.payload

        payload = {"min_days_to_harvest": 1000}

        response = self.client.patch(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "max_days_to_harvest cannot be less than min_days_to_harvest."
                ],
            },
        )


class CropDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.url = reverse("crop-detail", args=[self.crop.id])
        self.url_not_found = reverse("crop-detail", args=[2])

    def test_delete_crop(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_delete_crop_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(
            data,
        )
        self.assertEqual(message, "Resource not found.")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class CropImageUploadApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, ImageUploadAPITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.url = reverse("crop-image-upload", args=[self.crop.id])
        self.upload_to = "crops"
        self.url_not_found = reverse("crop-detail", args=[2])
