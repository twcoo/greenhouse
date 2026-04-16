from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Variety
from .commons.factories import CropFactory, UserFactory, VarietyFactory
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin


class VarietyListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("variety-list-create")
        self.crop = CropFactory(user=self.user)
        self.another_user = UserFactory(username="shimmer2")
        self.another_user_crop = CropFactory(user=self.another_user)
        self.another_user_varieties = VarietyFactory.create_batch(
            12, crop=self.another_user_crop
        )

    def test_list_empty_varieties(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, varieties, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(varieties, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=varieties,
            another_user_data=self.another_user_varieties,
        )

    def test_list_populated_varieties(self):
        self.authenticate()

        VarietyFactory.create_batch(3, crop=self.crop)

        response = self.client.get(self.url)

        response_status, data, varieties, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(varieties), 3)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=varieties,
            another_user_data=self.another_user_varieties,
        )

    def test_list_pagination(self):
        self.authenticate()

        VarietyFactory.create_batch(15, crop=self.crop)

        response = self.client.get(self.url, {"page_size": 10})

        response_status, data, varieties, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(varieties), 10)
        self.assertEqual(data["count"], 15)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=varieties,
            another_user_data=self.another_user_varieties,
        )


class VarietyCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("variety-list-create")
        self.crop = CropFactory(user=self.user)
        self.payload = {
            "name": "Sun Gold",
            "crop": self.crop.id,
            "growth_habit": ["INDETERMINATE"],
        }

    def test_create_variety_success(self):
        self.authenticate()

        response = self.client.post(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], self.payload["name"])
        self.assertEqual(data["crop"], self.crop.id)
        self.assertEqual(data["growth_habit"], self.payload["growth_habit"])
        self.assertTrue(
            Variety.objects.filter(name=self.payload["name"]).exists()
        )
        self.assertIsNone(message)

    def test_create_variety_missing_required_fields(self):
        self.authenticate()

        response = self.client.post(self.url, {}, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "name": ["This field is required."],
                "crop": ["This field is required."],
                "growth_habit": ["This field is required."],
            },
        )

    def test_create_variety_invalid_growth_habit_choice(self):
        self.authenticate()

        payload = {**self.payload, "growth_habit": ["INVALID_VALUE"]}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"growth_habit": {"0": ['"INVALID_VALUE" is not a valid choice.']}},
        )

    def test_create_variety_with_crop_not_owned_by_user(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)

        payload = {**self.payload, "crop": another_crop.id}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message, {"crop": ['Invalid pk "118" - object does not exist.']}
        )


class VarietyGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.url = reverse("variety-detail", args=[self.variety.id])
        self.url_not_found = reverse("variety-detail", args=[9999])

    def test_get_variety(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.variety.id,
                "name": self.variety.name,
                "crop": self.crop.id,
                "growth_habit": self.variety.growth_habit,
            },
        )
        self.assertIsNone(message)

    def test_get_variety_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)
        another_variety = VarietyFactory(crop=another_crop)

        url = reverse("variety-detail", args=[another_variety.id])

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_variety_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class VarietyUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.url = reverse("variety-detail", args=[self.variety.id])
        self.url_not_found = reverse("variety-detail", args=[9999])
        self.payload = {
            "name": "Cherokee Purple",
            "crop": self.crop.id,
            "growth_habit": ["INDETERMINATE"],
        }

    def test_update_variety(self):
        self.authenticate()

        response = self.client.put(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.variety.id,
                **self.payload,
            },
        )
        self.assertIsNone(message)

    def test_update_variety_not_found(self):
        self.authenticate()

        response = self.client.put(
            self.url_not_found, self.payload, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_variety_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)
        another_variety = VarietyFactory(crop=another_crop)

        url = reverse("variety-detail", args=[another_variety.id])

        response = self.client.put(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_variety_invalid_growth_habit_choice(self):
        self.authenticate()

        payload = {**self.payload, "growth_habit": ["INVALID_VALUE"]}

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)

        self.assertEqual(
            message,
            {"growth_habit": {"0": ['"INVALID_VALUE" is not a valid choice.']}},
        )


class VarietyPartialUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(
            crop=self.crop, growth_habit=["INDETERMINATE"]
        )
        self.url = reverse("variety-detail", args=[self.variety.id])
        self.url_not_found = reverse("variety-detail", args=[9999])

    def test_partially_update_variety(self):
        self.authenticate()

        payload = {"growth_habit": ["DETERMINATE"]}

        response = self.client.patch(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.variety.id,
                "name": self.variety.name,
                "crop": self.crop.id,
                "growth_habit": ["DETERMINATE"],
            },
        )
        self.assertIsNone(message)

    def test_partial_update_variety_not_found(self):
        self.authenticate()

        response = self.client.patch(
            self.url_not_found,
            {"growth_habit": ["DETERMINATE"]},
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_partial_update_variety_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)
        another_variety = VarietyFactory(crop=another_crop)

        url = reverse("variety-detail", args=[another_variety.id])

        response = self.client.patch(
            url, {"growth_habit": ["DETERMINATE"]}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class VarietyDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.url = reverse("variety-detail", args=[self.variety.id])
        self.url_not_found = reverse("variety-detail", args=[9999])

    def test_delete_variety(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(Variety.objects.filter(id=self.variety.id).exists())

    def test_delete_variety_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)
        another_variety = VarietyFactory(crop=another_crop)

        url = reverse("variety-detail", args=[another_variety.id])

        response = self.client.delete(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_delete_variety_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")
