import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .commons.factories import (PlantingLocationFactory,
                                PlantingLocationStatusFactory, UserFactory)
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin
from .commons.utils import CreateTestImageMixin


class PlantingLocationStatusListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-status-list-create",
            args=[self.planting_location.id],
        )

    def test_list_empty_status_history(self):
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

    def test_list_populated_status_history(self):
        self.authenticate()

        PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="AVAILABLE",
        )
        PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="DAMAGED",
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

        first = PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="AVAILABLE",
        )
        second = PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="DAMAGED",
        )

        response = self.client.get(self.url)

        _, _, entries, _ = self.get_response_data_many(response)

        self.assertEqual(entries[0]["id"], second.id)
        self.assertEqual(entries[1]["id"], first.id)

    def test_list_does_not_return_other_location_statuses(self):
        self.authenticate()

        other_location = PlantingLocationFactory(user=self.user)
        PlantingLocationStatusFactory(planting_location=other_location)
        PlantingLocationStatusFactory(planting_location=self.planting_location)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 1)

    def test_list_does_not_return_other_user_location_statuses(self):
        self.authenticate()

        other_user = UserFactory(username="other_status_user")
        other_location = PlantingLocationFactory(user=other_user)
        PlantingLocationStatusFactory(planting_location=other_location)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 0)

    def test_list_location_not_found(self):
        self.authenticate()

        url = reverse("planting-location-status-list-create", args=[9999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_other_user_location_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_list_user")
        other_location = PlantingLocationFactory(user=other_user)
        url = reverse(
            "planting-location-status-list-create",
            args=[other_location.id],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PlantingLocationStatusCreateApiViewTests(
    CreateTestImageMixin,
    RequiredAuthTestsMixin,
    ResponseUtilsMixin,
    APITestCase,
):
    http_method = "POST"

    def setUp(self):
        super().setUp()
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-status-list-create",
            args=[self.planting_location.id],
        )

    def test_create_status_success(self):
        self.authenticate()

        data = {"status": "AVAILABLE", "notes": "Ready for use."}
        response = self.client.post(self.url, data, format="multipart")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["status"], "AVAILABLE")
        self.assertEqual(response_data["notes"], "Ready for use.")
        self.assertIsNone(response_data["image"])
        self.assertIsNone(message)

    def test_create_status_without_notes(self):
        self.authenticate()

        data = {"status": "RETIRED"}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_status_missing_status_field(self):
        self.authenticate()

        data = {"notes": "Some notes."}
        response = self.client.post(self.url, data, format="multipart")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(message, {"status": ["This field is required."]})

    def test_create_status_invalid_choice(self):
        self.authenticate()

        data = {"status": "UNKNOWN"}
        response = self.client.post(self.url, data, format="multipart")

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message, {"status": ['"UNKNOWN" is not a valid choice.']}
        )

    def test_create_status_location_not_found(self):
        self.authenticate()

        url = reverse("planting-location-status-list-create", args=[9999])
        data = {"status": "AVAILABLE"}
        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_status_image_unsupported_extension(self):
        self.authenticate()

        image = self.create_test_image(name="status_gif", extension="gif")
        response = self.client.post(
            self.url,
            {"status": "AVAILABLE", "image": image},
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

    def test_create_status_image_too_large(self):
        self.authenticate()

        image = self.create_test_image(name="status_large", target_mb=3)
        response = self.client.post(
            self.url,
            {"status": "AVAILABLE", "image": image},
            format="multipart",
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            {"image": ["File too large. Size should not exceed 2.0MB."]},
        )

    def test_create_status_blocked_when_pot_is_in_use(self):
        self.authenticate()

        pot_location = PlantingLocationFactory(
            user=self.user, location_type="POT"
        )
        PlantingLocationStatusFactory(
            planting_location=pot_location, status="IN_USE"
        )
        url = reverse(
            "planting-location-status-list-create",
            args=[pot_location.id],
        )

        response = self.client.post(
            url, {"status": "AVAILABLE"}, format="multipart"
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            ["Cannot set status while the location is in use."],
        )

    def test_create_status_allowed_when_pot_is_not_in_use(self):
        self.authenticate()

        pot_location = PlantingLocationFactory(
            user=self.user, location_type="POT"
        )
        PlantingLocationStatusFactory(
            planting_location=pot_location, status="AVAILABLE"
        )
        url = reverse(
            "planting-location-status-list-create",
            args=[pot_location.id],
        )

        response = self.client.post(
            url, {"status": "DAMAGED"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_status_blocked_when_ground_is_in_use(self):
        self.authenticate()

        ground_location = PlantingLocationFactory(
            user=self.user, location_type="GROUND"
        )
        PlantingLocationStatusFactory(
            planting_location=ground_location, status="IN_USE"
        )
        url = reverse(
            "planting-location-status-list-create",
            args=[ground_location.id],
        )

        response = self.client.post(
            url, {"status": "DAMAGED"}, format="multipart"
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message,
            ["Cannot set status while the location is in use."],
        )

    def test_create_status_other_user_location_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_create_user")
        other_location = PlantingLocationFactory(user=other_user)
        url = reverse(
            "planting-location-status-list-create",
            args=[other_location.id],
        )
        data = {"status": "AVAILABLE"}
        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlantingLocationCurrentStatusTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-list-create",
        )

    def test_current_status_is_none_when_no_history(self):
        self.authenticate()

        response = self.client.get(self.url)

        _, _, locations, _ = self.get_response_data_many(response)

        location = next(
            loc for loc in locations if loc["id"] == self.planting_location.id
        )
        self.assertIsNone(location["current_status"])

    def test_current_status_returns_most_recent_entry(self):
        self.authenticate()

        PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="AVAILABLE",
        )
        latest = PlantingLocationStatusFactory(
            planting_location=self.planting_location,
            status="DAMAGED",
        )

        response = self.client.get(self.url)

        _, _, locations, _ = self.get_response_data_many(response)

        location = next(
            loc for loc in locations if loc["id"] == self.planting_location.id
        )
        self.assertIsNotNone(location["current_status"])
        self.assertEqual(location["current_status"]["id"], latest.id)
        self.assertEqual(location["current_status"]["status"], "DAMAGED")
