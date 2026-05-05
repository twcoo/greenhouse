import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.factories import (PlantingDailyObservationFactory,
                                PlantingFactory, UserFactory)
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin
from .commons.utils import CreateTestImageMixin


class PlantingDailyObservationListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.url = reverse(
            "planting-daily-observation-list-create",
            args=[self.planting.id],
        )

    def test_list_empty_observations(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, entries, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(entries, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(message)

    def test_list_populated_observations(self):
        self.authenticate()

        PlantingDailyObservationFactory(
            planting=self.planting, health_status="GOOD"
        )
        PlantingDailyObservationFactory(
            planting=self.planting, health_status="FAIR"
        )

        response = self.client.get(self.url)

        response_status, data, entries, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(entries), 2)
        self.assertEqual(data["count"], 2)
        self.assertIsNone(message)

    def test_list_returns_most_recent_first(self):
        self.authenticate()

        first = PlantingDailyObservationFactory(
            planting=self.planting, health_status="GOOD"
        )
        second = PlantingDailyObservationFactory(
            planting=self.planting, health_status="FAIR"
        )

        response = self.client.get(self.url)

        _, _, entries, _ = self.get_response_data_many(response)

        self.assertEqual(entries[0]["id"], second.id)
        self.assertEqual(entries[1]["id"], first.id)

    def test_list_does_not_return_other_planting_observations(self):
        self.authenticate()

        other_planting = PlantingFactory(user=self.user)
        PlantingDailyObservationFactory(planting=other_planting)
        PlantingDailyObservationFactory(planting=self.planting)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 1)

    def test_list_does_not_return_other_user_observations(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_list_user")
        other_planting = PlantingFactory(user=other_user)
        PlantingDailyObservationFactory(planting=other_planting)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 0)

    def test_list_planting_not_found(self):
        self.authenticate()

        url = reverse("planting-daily-observation-list-create", args=[9999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_other_user_planting_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_404_user")
        other_planting = PlantingFactory(user=other_user)
        url = reverse(
            "planting-daily-observation-list-create",
            args=[other_planting.id],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PlantingDailyObservationCreateApiViewTests(
    CreateTestImageMixin,
    RequiredAuthTestsMixin,
    ResponseUtilsMixin,
    APITestCase,
):
    http_method = "POST"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.url = reverse(
            "planting-daily-observation-list-create",
            args=[self.planting.id],
        )

    def test_create_observation_minimal_fields(self):
        self.authenticate()

        data = {"health_status": "GOOD"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["health_status"], "GOOD")
        self.assertIsNone(message)

    def test_create_observation_all_fields(self):
        self.authenticate()

        data = {
            "health_status": "FAIR",
            "pest_pressure": "LOW",
            "disease_symptoms": False,
            "height_cm": "15.50",
            "leaf_count": 10,
            "temperature_c": "22.5",
            "humidity_percent": "70.00",
            "light_hours": "12.00",
            "soil_moisture_percent": "60.00",
            "soil_ph": "6.8",
            "ec_ms_cm": "1.50",
            "notes": "Some notes.",
        }
        response = self.client.post(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["health_status"], "FAIR")
        self.assertEqual(response_data["leaf_count"], 10)
        self.assertEqual(response_data["notes"], "Some notes.")
        self.assertIsNone(message)

    def test_create_observation_invalid_health_status(self):
        self.authenticate()

        data = {"health_status": "UNKNOWN"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"health_status": ['"UNKNOWN" is not a valid choice.']},
        )

    def test_create_observation_image_unsupported_extension(self):
        self.authenticate()

        image = self.create_test_image(name="obs_gif", extension="gif")
        response = self.client.post(
            self.url,
            {"health_status": "GOOD", "image": image},
            format="multipart",
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {
                "image": [
                    "Unsupported file extension. Please upload a "
                    ".jpg or .png image."
                ]
            },
        )

    def test_create_observation_image_too_large(self):
        self.authenticate()

        image = self.create_test_image(name="obs_large", target_mb=3)
        response = self.client.post(
            self.url,
            {"health_status": "GOOD", "image": image},
            format="multipart",
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"image": ["File too large. Size should not exceed 2.0MB."]},
        )

    def test_create_observation_other_user_planting_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_create_user")
        other_planting = PlantingFactory(user=other_user)
        url = reverse(
            "planting-daily-observation-list-create",
            args=[other_planting.id],
        )

        response = self.client.post(
            url, {"health_status": "GOOD"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlantingDailyObservationDetailApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "PUT"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.observation = PlantingDailyObservationFactory(
            planting=self.planting, health_status="GOOD", notes="Initial."
        )
        self.url = reverse(
            "planting-daily-observation-detail",
            args=[self.planting.id, self.observation.id],
        )

    def test_update_observation_success(self):
        self.authenticate()

        data = {"health_status": "FAIR", "notes": "Updated notes."}
        response = self.client.put(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["health_status"], "FAIR")
        self.assertEqual(response_data["notes"], "Updated notes.")
        self.assertIsNone(message)

    def test_update_observation_invalid_health_status(self):
        self.authenticate()

        data = {"health_status": "UNKNOWN"}
        response = self.client.put(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_other_user_observation_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_update_user")
        other_planting = PlantingFactory(user=other_user)
        other_obs = PlantingDailyObservationFactory(planting=other_planting)
        url = reverse(
            "planting-daily-observation-detail",
            args=[other_planting.id, other_obs.id],
        )

        response = self.client.put(
            url, {"health_status": "GOOD"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_observation_wrong_planting_returns_404(self):
        self.authenticate()

        other_planting = PlantingFactory(user=self.user)
        url = reverse(
            "planting-daily-observation-detail",
            args=[other_planting.id, self.observation.id],
        )

        response = self.client.put(
            url, {"health_status": "GOOD"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_observation_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-daily-observation-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.put(
            url, {"health_status": "GOOD"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_observation_success(self):
        self.authenticate()

        data = {"notes": "Partially updated."}
        response = self.client.patch(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["notes"], "Partially updated.")
        self.assertEqual(response_data["health_status"], "GOOD")
        self.assertIsNone(message)

    def test_partial_update_observation_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-daily-observation-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.patch(url, {"notes": "x"}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_other_user_observation_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_patch_user")
        other_planting = PlantingFactory(user=other_user)
        other_obs = PlantingDailyObservationFactory(planting=other_planting)
        url = reverse(
            "planting-daily-observation-detail",
            args=[other_planting.id, other_obs.id],
        )

        response = self.client.patch(url, {"notes": "x"}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_observation_wrong_planting_returns_404(self):
        self.authenticate()

        other_planting = PlantingFactory(user=self.user)
        url = reverse(
            "planting-daily-observation-detail",
            args=[other_planting.id, self.observation.id],
        )

        response = self.client.patch(url, {"notes": "x"}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_observation_success(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_observation_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_obs_delete_user")
        other_planting = PlantingFactory(user=other_user)
        other_obs = PlantingDailyObservationFactory(planting=other_planting)
        url = reverse(
            "planting-daily-observation-detail",
            args=[other_planting.id, other_obs.id],
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_observation_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-daily-observation-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
