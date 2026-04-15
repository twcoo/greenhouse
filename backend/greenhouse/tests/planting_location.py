import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import PlantingLocation
from .commons.factories import PlantingLocationFactory, UserFactory
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin
from .commons.utils import ImageUploadAPITestCase


class PlantingLocationListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("planting-location-list-create")
        self.another_user = UserFactory(username="shimmer2")
        self.another_user_locations = PlantingLocationFactory.create_batch(
            12, user=self.another_user
        )

    def test_list_empty_planting_locations(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, locations, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(locations, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=locations,
            another_user_data=self.another_user_locations,
        )

    def test_list_populated_planting_locations(self):
        self.authenticate()

        PlantingLocationFactory.create_batch(3, user=self.user)

        response = self.client.get(self.url)

        response_status, data, locations, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(locations), 3)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=locations,
            another_user_data=self.another_user_locations,
        )

    def test_list_pagination(self):
        self.authenticate()

        PlantingLocationFactory.create_batch(15, user=self.user)

        response = self.client.get(self.url, {"page_size": 10})

        response_status, data, locations, message = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(locations), 10)
        self.assertEqual(data["count"], 15)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=locations,
            another_user_data=self.another_user_locations,
        )


class PlantingLocationCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("planting-location-list-create")
        self.ground_payload = {
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "width": "120.00",
            "length": "5.00",
        }
        self.pot_payload = {
            "name": "Balcony Pot",
            "location_type": "POT",
            "width": "25.00",
            "height": "30.00",
        }

    def test_create_ground_planting_location_success(self):
        self.authenticate()

        response = self.client.post(
            self.url, self.ground_payload, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], self.ground_payload["name"])
        self.assertEqual(
            data["location_type"], self.ground_payload["location_type"]
        )
        self.assertEqual(data["width"], self.ground_payload["width"])
        self.assertEqual(data["length"], self.ground_payload["length"])
        self.assertIsNone(data["height"])
        location = PlantingLocation.objects.get(id=data["id"])
        self.assertEqual(location.user_id, self.user.id)
        self.assertIsNone(message)

    def test_create_pot_planting_location_success(self):
        self.authenticate()

        response = self.client.post(self.url, self.pot_payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], self.pot_payload["name"])
        self.assertEqual(
            data["location_type"], self.pot_payload["location_type"]
        )
        self.assertEqual(data["width"], self.pot_payload["width"])
        self.assertEqual(data["height"], self.pot_payload["height"])
        self.assertIsNone(data["length"])
        self.assertIsNone(message)

    def test_create_planting_location_missing_required_fields(self):
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
                "location_type": ["This field is required."],
                "width": ["This field is required."],
            },
        )

    def test_create_ground_location_requires_length(self):
        self.authenticate()

        payload = {
            "name": "Garden Bed",
            "location_type": "GROUND",
            "width": "120.00",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"length": ["Length is required for ground locations."]},
        )

    def test_create_ground_location_rejects_height(self):
        self.authenticate()

        payload = {
            "name": "Garden Bed",
            "location_type": "GROUND",
            "width": "120.00",
            "length": "5.00",
            "height": "30.00",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"height": ["Height must not be provided for ground locations."]},
        )

    def test_create_pot_location_requires_height(self):
        self.authenticate()

        payload = {
            "name": "Balcony Pot",
            "location_type": "POT",
            "width": "25.00",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"height": ["Height is required for pot locations."]},
        )

    def test_create_pot_location_rejects_length(self):
        self.authenticate()

        payload = {
            "name": "Balcony Pot",
            "location_type": "POT",
            "width": "25.00",
            "height": "30.00",
            "length": "5.00",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"length": ["Length must not be provided for ground locations."]},
        )

    def test_create_planting_location_invalid_location_type(self):
        self.authenticate()

        payload = {
            "name": "Garden Bed",
            "location_type": "INVALID_TYPE",
            "width": "120.00",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"location_type": ['"INVALID_TYPE" is not a valid choice.']},
        )


class PlantingLocationGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.location = PlantingLocationFactory(user=self.user)
        self.url = reverse("planting-location-detail", args=[self.location.id])
        self.url_not_found = reverse("planting-location-detail", args=[9999])

    def test_get_planting_location(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.location.id,
                "name": self.location.name,
                "location_type": self.location.location_type,
                "height": self.location.height,
                "width": str(self.location.width),
                "length": str(self.location.length),
            },
        )
        self.assertIsNone(message)

    def test_get_planting_location_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_location = PlantingLocationFactory(user=another_user)

        url = reverse("planting-location-detail", args=[another_location.id])

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_planting_location_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.location = PlantingLocationFactory(user=self.user)
        self.url = reverse("planting-location-detail", args=[self.location.id])
        self.url_not_found = reverse("planting-location-detail", args=[9999])
        self.payload = {
            "name": "Updated Garden Bed",
            "location_type": "GROUND",
            "width": "200.00",
            "length": "10.00",
        }

    def test_update_planting_location(self):
        self.authenticate()

        response = self.client.put(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.location.id,
                **self.payload,
                "height": None,
            },
        )
        self.assertIsNone(message)

    def test_update_planting_location_not_found(self):
        self.authenticate()

        response = self.client.put(
            self.url_not_found, self.payload, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_planting_location_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_location = PlantingLocationFactory(user=another_user)

        url = reverse("planting-location-detail", args=[another_location.id])

        response = self.client.put(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_ground_location_requires_length(self):
        self.authenticate()

        payload = {
            "name": "Garden Bed",
            "location_type": "GROUND",
            "width": "120.00",
            "length": None,
        }

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"length": ["This field may not be null."]},
        )


class PlantingLocationPartialUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.location = PlantingLocationFactory(
            user=self.user,
            name="Garden Bed",
            location_type="GROUND",
            width="120.00",
            length="5.00",
            height=None,
        )
        self.url = reverse("planting-location-detail", args=[self.location.id])
        self.url_not_found = reverse("planting-location-detail", args=[9999])

    def test_partially_update_planting_location(self):
        self.authenticate()

        payload = {"length": "10.00"}

        response = self.client.patch(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(
            data,
            {
                "id": self.location.id,
                "name": self.location.name,
                "location_type": self.location.location_type,
                "height": None,
                "width": str(self.location.width),
                "length": "10.00",
            },
        )
        self.assertIsNone(message)

    def test_partial_update_ground_location_rejects_height(self):
        self.authenticate()

        payload = {"height": "30.00"}

        response = self.client.patch(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"height": ["Height must not be provided for ground locations."]},
        )

    def test_partial_update_planting_location_not_found(self):
        self.authenticate()

        response = self.client.patch(
            self.url_not_found, {"length": "10.00"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_partial_update_planting_location_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_location = PlantingLocationFactory(user=another_user)

        url = reverse("planting-location-detail", args=[another_location.id])

        response = self.client.patch(url, {"length": "10.00"}, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.location = PlantingLocationFactory(user=self.user)
        self.url = reverse("planting-location-detail", args=[self.location.id])
        self.url_not_found = reverse("planting-location-detail", args=[9999])

    def test_delete_planting_location(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(
            PlantingLocation.objects.filter(id=self.location.id).exists()
        )

    def test_delete_planting_location_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_location = PlantingLocationFactory(user=another_user)

        url = reverse("planting-location-detail", args=[another_location.id])

        response = self.client.delete(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_delete_planting_location_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PlantingLocationImageUploadApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, ImageUploadAPITestCase
):
    def setUp(self):
        super().setUp()
        self.location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-image-upload", args=[self.location.id]
        )
        self.upload_to = "planting_locations"
        self.url_not_found = reverse("planting-location-detail", args=[9999])
