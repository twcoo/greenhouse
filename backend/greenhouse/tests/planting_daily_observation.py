import tempfile
from datetime import date, timedelta

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import PlantingDailyObservation
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

    def test_list_ordered_by_observation_date_desc(self):
        self.authenticate()

        today = date.today()
        older = PlantingDailyObservationFactory(
            planting=self.planting,
            health_status="GOOD",
            observation_date=today - timedelta(days=2),
        )
        newer = PlantingDailyObservationFactory(
            planting=self.planting,
            health_status="FAIR",
            observation_date=today,
        )

        response = self.client.get(self.url)

        _, _, entries, _ = self.get_response_data_many(response)

        self.assertEqual(entries[0]["id"], newer.id)
        self.assertEqual(entries[1]["id"], older.id)

    def test_list_same_date_ordered_by_pk_desc(self):
        self.authenticate()

        today = date.today()
        first = PlantingDailyObservationFactory(
            planting=self.planting,
            observation_date=today,
        )
        second = PlantingDailyObservationFactory(
            planting=self.planting,
            observation_date=today,
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

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
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
            "watering_event": "WATERED",
            "pruned": True,
            "notes": "Some notes.",
        }
        response = self.client.post(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["health_status"], "FAIR")
        self.assertEqual(response_data["notes"], "Some notes.")
        self.assertEqual(response_data["watering_event"], "WATERED")
        self.assertEqual(response_data["pruned"], True)
        self.assertIsNone(message)

    def test_create_observation_without_watering_event_returns_400(self):
        self.authenticate()

        data = {"health_status": "GOOD"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIn("watering_event", message)

    def test_create_observation_with_watering_event_rained(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "RAINED"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["watering_event"], "RAINED")

    def test_create_observation_with_watering_event_skipped_wet(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["watering_event"], "SKIPPED_WET")

    def test_create_observation_invalid_watering_event(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SPRINKLER"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"watering_event": ['"SPRINKLER" is not a valid choice.']},
        )

    def test_create_observation_pruned_defaults_to_false(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertFalse(response_data["pruned"])
        self.assertIsNone(message)

    def test_create_observation_pruning_detail_defaults_to_empty(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["pruning_detail"], "")

    def test_create_observation_with_pruning_detail(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "pruned": True,
            "pruning_detail": "removed lower leaves",
        }
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response_data["pruned"])
        self.assertEqual(
            response_data["pruning_detail"], "removed lower leaves"
        )

    def test_create_observation_invalid_health_status(self):
        self.authenticate()

        data = {"health_status": "UNKNOWN", "watering_event": "SKIPPED_WET"}
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
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": image,
            },
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
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": image,
            },
            format="multipart",
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"image": ["File too large. Size should not exceed 2.0MB."]},
        )

    def test_create_observation_defaults_observation_date_to_today(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_data["observation_date"], date.today().isoformat()
        )

    def test_create_observation_with_past_date(self):
        self.authenticate()

        past_date = (date.today() - timedelta(days=3)).isoformat()
        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "observation_date": past_date,
        }
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["observation_date"], past_date)

    def test_create_observation_invalid_observation_date(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "observation_date": "not-a-date",
        }
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {
                "observation_date": [
                    "Date has wrong format. Use one of these"
                    " formats instead: YYYY-MM-DD."
                ]
            },
        )

    def test_create_observation_fertilizer_type_defaults_to_none(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["fertilizer_type"], "NONE")

    def test_create_observation_fertilizer_detail_defaults_to_empty(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["fertilizer_detail"], "")

    def test_create_observation_with_organic_fertilizer(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "fertilizer_type": "ORGANIC",
            "fertilizer_detail": "fermented swamp fertilizer",
        }
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["fertilizer_type"], "ORGANIC")
        self.assertEqual(
            response_data["fertilizer_detail"], "fermented swamp fertilizer"
        )

    def test_create_observation_with_synthetic_fertilizer(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "fertilizer_type": "SYNTHETIC",
        }
        response = self.client.post(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["fertilizer_type"], "SYNTHETIC")

    def test_create_observation_invalid_fertilizer_type(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "fertilizer_type": "BANANA",
        }
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"fertilizer_type": ['"BANANA" is not a valid choice.']},
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
            url,
            {"health_status": "GOOD", "watering_event": "SKIPPED_WET"},
            format="multipart",
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

        data = {
            "health_status": "FAIR",
            "notes": "Updated notes.",
            "watering_event": "WATERED",
        }
        response = self.client.put(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["health_status"], "FAIR")
        self.assertEqual(response_data["notes"], "Updated notes.")
        self.assertEqual(response_data["watering_event"], "WATERED")
        self.assertIsNone(message)

    def test_update_observation_watering_event_skipped_wet(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
        }
        response = self.client.put(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["watering_event"], "SKIPPED_WET")

    def test_partial_update_watering_event(self):
        self.authenticate()

        data = {"watering_event": "RAINED"}
        response = self.client.patch(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["watering_event"], "RAINED")
        self.assertEqual(response_data["health_status"], "GOOD")

    def test_update_observation_invalid_watering_event(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SPRINKLER"}
        response = self.client.put(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_observation_date(self):
        self.authenticate()

        past_date = (date.today() - timedelta(days=5)).isoformat()
        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "observation_date": past_date,
        }
        response = self.client.put(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["observation_date"], past_date)

    def test_partial_update_observation_date(self):
        self.authenticate()

        past_date = (date.today() - timedelta(days=2)).isoformat()
        data = {"observation_date": past_date}
        response = self.client.patch(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["observation_date"], past_date)
        self.assertEqual(response_data["health_status"], "GOOD")

    def test_update_observation_fertilizer_type_and_detail(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "fertilizer_type": "ORGANIC",
            "fertilizer_detail": "fish emulsion",
        }
        response = self.client.put(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["fertilizer_type"], "ORGANIC")
        self.assertEqual(response_data["fertilizer_detail"], "fish emulsion")

    def test_partial_update_pruned(self):
        self.authenticate()

        data = {"pruned": True}
        response = self.client.patch(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_data["pruned"])
        self.assertEqual(response_data["health_status"], "GOOD")

    def test_update_observation_pruning_detail(self):
        self.authenticate()

        data = {
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
            "fertilizer_type": "ORGANIC",
            "fertilizer_detail": "worm castings",
            "pruned": True,
            "pruning_detail": "topped the plant",
        }
        response = self.client.put(self.url, data, format="multipart")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["fertilizer_type"], "ORGANIC")
        self.assertEqual(response_data["fertilizer_detail"], "worm castings")
        self.assertEqual(response_data["pruning_detail"], "topped the plant")

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


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PlantingDailyObservationImageClearTests(
    CreateTestImageMixin,
    RequiredAuthTestsMixin,
    ResponseUtilsMixin,
    APITestCase,
):
    http_method = "PUT"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.observation = PlantingDailyObservationFactory(
            planting=self.planting, health_status="GOOD"
        )
        self.url = reverse(
            "planting-daily-observation-detail",
            args=[self.planting.id, self.observation.id],
        )

    def _attach_image(self):
        """Upload an image to the observation and return the updated instance."""
        self.authenticate()
        image = self.create_test_image(name="obs_img")
        self.client.put(
            self.url,
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": image,
            },
            format="multipart",
        )
        self.observation.refresh_from_db()

    def test_clear_image_sets_image_to_null_in_response(self):
        self._attach_image()
        self.assertTrue(self.observation.image)

        response = self.client.put(
            self.url,
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": "",
            },
            format="multipart",
        )

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertIsNone(response_data["image"])
        self.assertIsNone(message)

    def test_clear_image_deletes_file_from_storage(self):
        self._attach_image()
        image_path = self.observation.image.path
        self.assertTrue(self.observation.image.storage.exists(image_path))

        self.client.put(
            self.url,
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": "",
            },
            format="multipart",
        )

        self.assertFalse(self.observation.image.storage.exists(image_path))

    def test_update_without_image_key_preserves_existing_image(self):
        self._attach_image()
        original_image_name = self.observation.image.name

        self.client.put(
            self.url,
            {"health_status": "FAIR", "watering_event": "SKIPPED_WET"},
            format="multipart",
        )

        self.observation.refresh_from_db()
        self.assertEqual(self.observation.image.name, original_image_name)

    def test_clear_image_when_no_image_returns_200(self):
        self.authenticate()
        self.assertFalse(self.observation.image)

        response = self.client.put(
            self.url,
            {
                "health_status": "GOOD",
                "watering_event": "SKIPPED_WET",
                "image": "",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _, response_data, _ = self.get_response_data(response)
        self.assertIsNone(response_data["image"])


class PlantingDailyObservationBulkCreateApiViewTests(
    RequiredAuthTestsMixin,
    ResponseUtilsMixin,
    APITestCase,
):
    http_method = "POST"

    def setUp(self):
        super().setUp()
        self.planting_a = PlantingFactory(user=self.user)
        self.planting_b = PlantingFactory(user=self.user)
        self.url = reverse("planting-daily-observation-bulk-create")

    def _base_data(self, **overrides):
        data = {
            "planting_ids": [self.planting_a.id, self.planting_b.id],
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
        }
        data.update(overrides)
        return data

    def _post(self, data):
        return self.client.post(self.url, data, format="json")

    def test_bulk_create_success(self):
        self.authenticate()

        data = self._base_data()
        response = self._post(data)

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(response_data), 2)
        self.assertIsNone(message)
        for obs in response_data:
            self.assertEqual(obs["health_status"], data["health_status"])
            self.assertEqual(obs["watering_event"], data["watering_event"])

    def test_bulk_create_creates_correct_count_in_db(self):
        self.authenticate()

        self._post(self._base_data())

        count = PlantingDailyObservation.objects.filter(
            planting__in=[self.planting_a, self.planting_b]
        ).count()
        self.assertEqual(count, 2)

    def test_bulk_create_single_planting_id(self):
        self.authenticate()

        data = self._base_data()
        data["planting_ids"] = [self.planting_a.id]
        response = self._post(data)

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["health_status"], "GOOD")

    def test_bulk_create_observation_fields_applied_to_all(self):
        self.authenticate()

        data = self._base_data(
            pest_pressure="LOW",
            disease_symptoms=True,
            pruned=True,
            pruning_detail="removed lower leaves",
            fertilizer_type="ORGANIC",
            fertilizer_detail="fish emulsion",
            notes="Same note for all.",
        )
        response = self._post(data)

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for obs in response_data:
            self.assertEqual(obs["health_status"], data["health_status"])
            self.assertEqual(obs["watering_event"], data["watering_event"])
            self.assertEqual(obs["pest_pressure"], data["pest_pressure"])
            self.assertTrue(obs["disease_symptoms"])
            self.assertTrue(obs["pruned"])
            self.assertEqual(obs["pruning_detail"], data["pruning_detail"])
            self.assertEqual(obs["fertilizer_type"], data["fertilizer_type"])
            self.assertEqual(
                obs["fertilizer_detail"], data["fertilizer_detail"]
            )
            self.assertEqual(obs["notes"], data["notes"])

    def test_bulk_create_invalid_planting_id_returns_400(self):
        self.authenticate()

        data = self._base_data()
        data["planting_ids"] = [self.planting_a.id, 9999]
        response = self._post(data)

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {
                "planting_ids": [
                    "One or more planting IDs are invalid or do not "
                    "belong to the current user."
                ]
            },
        )

    def test_bulk_create_invalid_planting_id_creates_no_records(self):
        self.authenticate()

        data = self._base_data()
        data["planting_ids"] = [self.planting_a.id, 9999]
        self._post(data)

        count = PlantingDailyObservation.objects.filter(
            planting=self.planting_a
        ).count()
        self.assertEqual(count, 0)

    def test_bulk_create_other_user_planting_returns_400(self):
        self.authenticate()

        other_user = UserFactory(username="other_bulk_obs_user")
        other_planting = PlantingFactory(user=other_user)
        data = self._base_data()
        data["planting_ids"] = [other_planting.id]
        response = self._post(data)

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {
                "planting_ids": [
                    "One or more planting IDs are invalid or do not "
                    "belong to the current user."
                ]
            },
        )

    def test_bulk_create_mixed_ownership_returns_400(self):
        self.authenticate()

        other_user = UserFactory(username="other_bulk_mixed_user")
        other_planting = PlantingFactory(user=other_user)
        data = self._base_data()
        data["planting_ids"] = [self.planting_a.id, other_planting.id]
        response = self._post(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_create_missing_planting_ids_returns_400(self):
        self.authenticate()

        data = {"health_status": "GOOD", "watering_event": "SKIPPED_WET"}
        response = self._post(data)

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"planting_ids": ["This field is required."]},
        )

    def test_bulk_create_empty_planting_ids_returns_400(self):
        self.authenticate()

        data = {
            "planting_ids": [],
            "health_status": "GOOD",
            "watering_event": "SKIPPED_WET",
        }
        response = self._post(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_create_missing_watering_event_returns_400(self):
        self.authenticate()

        data = {
            "planting_ids": [self.planting_a.id],
            "health_status": "GOOD",
        }
        response = self._post(data)

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"watering_event": ["This field is required."]},
        )

    def test_bulk_create_invalid_health_status_returns_400(self):
        self.authenticate()

        data = self._base_data()
        data["health_status"] = "UNKNOWN"
        response = self._post(data)

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"health_status": ['"UNKNOWN" is not a valid choice.']},
        )
