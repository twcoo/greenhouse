from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Planting
from .commons.factories import (CropFactory, PlantingFactory,
                                PlantingLocationAssignmentFactory,
                                PlantingLocationFactory, UserFactory,
                                VarietyFactory)
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin


class PlantingListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("planting-list-create")
        self.another_user = UserFactory(username="shimmer2")
        self.another_user_plantings = PlantingFactory.create_batch(
            12, user=self.another_user
        )

    def test_list_empty_plantings(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, plantings, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(plantings, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=plantings,
            another_user_data=self.another_user_plantings,
        )

    def test_list_populated_plantings(self):
        self.authenticate()

        PlantingFactory.create_batch(3, user=self.user)

        response = self.client.get(self.url)

        response_status, data, plantings, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(plantings), 3)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.assertIsNone(plantings[0]["current_location"])
        self.validate_no_cross_user_data_leakage(
            user_data=plantings,
            another_user_data=self.another_user_plantings,
        )

    def test_list_pagination(self):
        self.authenticate()

        PlantingFactory.create_batch(15, user=self.user)

        response = self.client.get(self.url, {"page_size": 10})

        response_status, data, plantings, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(plantings), 10)
        self.assertEqual(data["count"], 15)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=plantings,
            another_user_data=self.another_user_plantings,
        )

    def test_list_search_by_crop_name(self):
        self.authenticate()

        target_crop = CropFactory(user=self.user, name="Tomato")
        target_variety = VarietyFactory(crop=target_crop)
        PlantingFactory(
            user=self.user, crop=target_crop, variety=target_variety
        )

        other_crop = CropFactory(user=self.user, name="Pepper")
        other_variety = VarietyFactory(crop=other_crop)
        PlantingFactory(user=self.user, crop=other_crop, variety=other_variety)

        response = self.client.get(self.url, {"search": "Tomato"})

        response_status, _, plantings, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(plantings), 1)
        self.assertEqual(plantings[0]["crop_name"], "Tomato")

    def test_list_search_by_variety_name(self):
        self.authenticate()

        crop = CropFactory(user=self.user)
        target_variety = VarietyFactory(crop=crop, name="Sun Gold")
        PlantingFactory(user=self.user, crop=crop, variety=target_variety)

        other_variety = VarietyFactory(crop=crop, name="Cherokee Purple")
        PlantingFactory(user=self.user, crop=crop, variety=other_variety)

        response = self.client.get(self.url, {"search": "Sun Gold"})

        response_status, _, plantings, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(plantings), 1)
        self.assertEqual(plantings[0]["variety_name"], "Sun Gold")


class PlantingCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("planting-list-create")
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.payload = {
            "crop": self.crop.id,
            "variety": self.variety.id,
        }

    def test_create_planting_success(self):
        self.authenticate()

        response = self.client.post(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["crop"], self.crop.id)
        self.assertEqual(data["crop_name"], self.crop.name)
        self.assertEqual(data["variety"], self.variety.id)
        self.assertEqual(data["variety_name"], self.variety.name)
        self.assertIsNone(data["current_location"])
        self.assertIsNotNone(data["created_at"])
        self.assertTrue(
            Planting.objects.filter(
                crop=self.crop, variety=self.variety, user=self.user
            ).exists()
        )
        self.assertIsNone(message)

    def test_create_planting_missing_required_fields(self):
        self.authenticate()

        response = self.client.post(self.url, {}, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "crop": ["This field is required."],
                "variety": ["This field is required."],
            },
        )

    def test_create_planting_with_crop_not_owned_by_user(self):
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
            message,
            {
                "crop": [
                    f'Invalid pk "{another_crop.id}" - object does not exist.'
                ]
            },
        )

    def test_create_planting_with_variety_not_owned_by_user(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_crop = CropFactory(user=another_user)
        another_variety = VarietyFactory(crop=another_crop)

        payload = {**self.payload, "variety": another_variety.id}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "variety": [
                    f'Invalid pk "{another_variety.id}" - object does not exist.'
                ]
            },
        )

    def test_create_planting_variety_crop_mismatch(self):
        self.authenticate()

        other_crop = CropFactory(user=self.user)
        other_variety = VarietyFactory(crop=other_crop)

        payload = {"crop": self.crop.id, "variety": other_variety.id}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"variety": ["Variety does not belong to the selected crop."]},
        )


class PlantingGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        self.url = reverse("planting-detail", args=[self.planting.id])
        self.url_not_found = reverse("planting-detail", args=[9999])

    def test_get_planting(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.planting.id)
        self.assertEqual(data["crop"], self.crop.id)
        self.assertEqual(data["crop_name"], self.crop.name)
        self.assertEqual(data["variety"], self.variety.id)
        self.assertEqual(data["variety_name"], self.variety.name)
        self.assertIsNone(data["current_location"])
        self.assertIsNotNone(data["created_at"])
        self.assertIsNone(message)

    def test_get_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)

        url = reverse("planting-detail", args=[another_planting.id])

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_planting_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        self.url = reverse("planting-detail", args=[self.planting.id])
        self.url_not_found = reverse("planting-detail", args=[9999])

    def test_update_planting(self):
        self.authenticate()

        new_variety = VarietyFactory(crop=self.crop)
        payload = {"crop": self.crop.id, "variety": new_variety.id}

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.planting.id)
        self.assertEqual(data["crop"], self.crop.id)
        self.assertEqual(data["variety"], new_variety.id)
        self.assertEqual(data["variety_name"], new_variety.name)
        self.assertIsNone(message)

    def test_update_planting_not_found(self):
        self.authenticate()

        payload = {"crop": self.crop.id, "variety": self.variety.id}

        response = self.client.put(self.url_not_found, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)

        url = reverse("planting-detail", args=[another_planting.id])
        payload = {"crop": self.crop.id, "variety": self.variety.id}

        response = self.client.put(url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_planting_variety_crop_mismatch(self):
        self.authenticate()

        other_crop = CropFactory(user=self.user)
        other_variety = VarietyFactory(crop=other_crop)

        payload = {"crop": self.crop.id, "variety": other_variety.id}

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"variety": ["Variety does not belong to the selected crop."]},
        )


class PlantingPartialUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        self.url = reverse("planting-detail", args=[self.planting.id])
        self.url_not_found = reverse("planting-detail", args=[9999])

    def test_partially_update_planting(self):
        self.authenticate()

        new_variety = VarietyFactory(crop=self.crop)

        response = self.client.patch(
            self.url, {"variety": new_variety.id}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.planting.id)
        self.assertEqual(data["crop"], self.crop.id)
        self.assertEqual(data["variety"], new_variety.id)
        self.assertEqual(data["variety_name"], new_variety.name)
        self.assertIsNone(message)

    def test_partial_update_planting_variety_crop_mismatch(self):
        self.authenticate()

        other_crop = CropFactory(user=self.user)
        other_variety = VarietyFactory(crop=other_crop)

        response = self.client.patch(
            self.url, {"variety": other_variety.id}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"variety": ["Variety does not belong to the selected crop."]},
        )

    def test_partial_update_planting_not_found(self):
        self.authenticate()

        response = self.client.patch(
            self.url_not_found,
            {"variety": self.variety.id},
            format="json",
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_partial_update_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)

        url = reverse("planting-detail", args=[another_planting.id])

        response = self.client.patch(
            url, {"variety": self.variety.id}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)
        self.planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        self.url = reverse("planting-detail", args=[self.planting.id])
        self.url_not_found = reverse("planting-detail", args=[9999])

    def test_delete_planting(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(Planting.objects.filter(id=self.planting.id).exists())

    def test_delete_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)

        url = reverse("planting-detail", args=[another_planting.id])

        response = self.client.delete(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_delete_planting_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingCurrentLocationTests(ResponseUtilsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.url = reverse("planting-list-create")
        self.crop = CropFactory(user=self.user)
        self.variety = VarietyFactory(crop=self.crop)

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_current_location_is_null_with_no_assignment(self):
        self.authenticate()

        PlantingFactory(user=self.user, crop=self.crop, variety=self.variety)

        response = self.client.get(self.url)

        _, _, plantings, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(plantings[0]["current_location"])

    def test_current_location_returns_name_when_active_assignment(self):
        self.authenticate()

        planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        location = PlantingLocationFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=planting,
            planting_location=location,
            end_date=None,
        )

        response = self.client.get(self.url)

        _, _, plantings, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(plantings[0]["current_location"], location.name)

    def test_current_location_is_null_when_assignment_closed(self):
        self.authenticate()

        planting = PlantingFactory(
            user=self.user, crop=self.crop, variety=self.variety
        )
        location = PlantingLocationFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=planting,
            planting_location=location,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 6, 1),
        )

        response = self.client.get(self.url)

        _, _, plantings, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(plantings[0]["current_location"])
