from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import PlantingLocationAssignment, PlantingLocationStatus
from .commons.factories import (PlantingFactory,
                                PlantingLocationAssignmentFactory,
                                PlantingLocationFactory, UserFactory)
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin


class PlantingLocationAssignmentListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-assignment-list-create",
            args=[self.planting.id],
        )

    def test_list_empty_assignments(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, assignments, message = (
            self.get_response_data_many(response)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(assignments, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)

    def test_list_populated_assignments(self):
        self.authenticate()

        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )
        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-07-01",
            end_date=None,
        )

        response = self.client.get(self.url)

        response_status, data, assignments, message = (
            self.get_response_data_many(response)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(assignments), 2)
        self.assertEqual(data["count"], 2)
        self.assertIsNone(message)

    def test_list_does_not_return_other_planting_assignments(self):
        self.authenticate()

        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
        )
        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
        )

        response = self.client.get(self.url)

        _, data, assignments, _ = self.get_response_data_many(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(assignments), 1)

    def test_list_planting_not_found(self):
        self.authenticate()

        url = reverse("planting-location-assignment-list-create", args=[9999])

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_list_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-list-create",
            args=[another_planting.id],
        )

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationAssignmentCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "POST"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.url = reverse(
            "planting-location-assignment-list-create",
            args=[self.planting.id],
        )
        self.payload = {
            "planting_location": self.planting_location.id,
            "start_date": "2024-01-01",
        }

    def test_create_assignment_success(self):
        self.authenticate()

        response = self.client.post(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["planting_location"], self.planting_location.id)
        self.assertEqual(
            data["planting_location_name"], self.planting_location.name
        )
        self.assertEqual(data["start_date"], "2024-01-01")
        self.assertIsNone(data["end_date"])
        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])
        self.assertTrue(
            PlantingLocationAssignment.objects.filter(
                planting=self.planting,
                planting_location=self.planting_location,
            ).exists()
        )
        self.assertIsNone(message)

    def test_create_assignment_missing_required_fields(self):
        self.authenticate()

        response = self.client.post(self.url, {}, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "planting_location": ["This field is required."],
                "start_date": ["This field is required."],
            },
        )

    def test_create_assignment_planting_location_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_location = PlantingLocationFactory(user=another_user)

        payload = {**self.payload, "planting_location": another_location.id}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "planting_location": [
                    f'Invalid pk "{another_location.id}" - object does not'
                    " exist."
                ]
            },
        )

    def test_create_assignment_planting_not_found(self):
        self.authenticate()

        url = reverse("planting-location-assignment-list-create", args=[9999])

        response = self.client.post(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_create_assignment_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-list-create",
            args=[another_planting.id],
        )

        response = self.client.post(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_create_assignment_end_date_before_start_date(self):
        self.authenticate()

        payload = {
            **self.payload,
            "start_date": "2024-06-01",
            "end_date": "2024-01-01",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"end_date": ["End date must be on or after start date."]},
        )

    def test_create_assignment_overlap_with_open_ended_existing(self):
        self.authenticate()

        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date=None,
        )

        payload = {**self.payload, "start_date": "2024-03-01"}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "start_date": [
                    "This planting already has a location assignment "
                    "that overlaps with the given date range."
                ]
            },
        )

    def test_create_assignment_overlap_with_bounded_existing(self):
        self.authenticate()

        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )

        payload = {
            **self.payload,
            "start_date": "2024-03-01",
            "end_date": "2024-09-01",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "start_date": [
                    "This planting already has a location assignment "
                    "that overlaps with the given date range."
                ]
            },
        )

    def test_create_assignment_sequential_after_closed(self):
        self.authenticate()

        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )

        payload = {**self.payload, "start_date": "2024-06-02"}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assignment_pot_occupied_by_other_planting(self):
        self.authenticate()

        pot = PlantingLocationFactory(
            user=self.user,
            location_type="POT",
            height="30.00",
            length=None,
        )
        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=pot,
            start_date="2024-01-01",
            end_date=None,
        )

        payload = {
            "planting_location": pot.id,
            "start_date": "2024-03-01",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "planting_location": [
                    "This location already has an active planting "
                    "for the given date range."
                ]
            },
        )

    def test_create_assignment_nursery_pot_occupied_by_other_planting(self):
        self.authenticate()

        nursery_pot = PlantingLocationFactory(
            user=self.user,
            location_type="NURSERYPOT",
            height="20.00",
            length=None,
        )
        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=nursery_pot,
            start_date="2024-01-01",
            end_date=None,
        )

        payload = {
            "planting_location": nursery_pot.id,
            "start_date": "2024-03-01",
        }

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "planting_location": [
                    "This location already has an active planting "
                    "for the given date range."
                ]
            },
        )

    def test_create_assignment_pot_available_after_other_planting_closed(self):
        self.authenticate()

        pot = PlantingLocationFactory(
            user=self.user,
            location_type="POT",
            height="30.00",
            length=None,
        )
        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=pot,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )

        payload = {
            "planting_location": pot.id,
            "start_date": "2024-06-02",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assignment_ground_allows_multiple_active_plantings(self):
        self.authenticate()

        ground = PlantingLocationFactory(
            user=self.user,
            location_type="GROUND",
        )
        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=ground,
            start_date="2024-01-01",
            end_date=None,
        )

        payload = {
            "planting_location": ground.id,
            "start_date": "2024-03-01",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PlantingLocationAssignmentGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date=None,
        )
        self.url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, self.assignment.id],
        )
        self.url_not_found = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, 9999],
        )

    def test_get_assignment(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.assignment.id)
        self.assertEqual(data["planting_location"], self.planting_location.id)
        self.assertEqual(
            data["planting_location_name"], self.planting_location.name
        )
        self.assertEqual(data["start_date"], "2024-01-01")
        self.assertIsNone(data["end_date"])
        self.assertIsNotNone(data["created_at"])
        self.assertIsNotNone(data["updated_at"])
        self.assertIsNone(message)

    def test_get_assignment_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_assignment_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-detail",
            args=[another_planting.id, self.assignment.id],
        )

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_assignment_wrong_planting(self):
        self.authenticate()

        other_planting = PlantingFactory(user=self.user)
        url = reverse(
            "planting-location-assignment-detail",
            args=[other_planting.id, self.assignment.id],
        )

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationAssignmentUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "PUT"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )
        self.url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, self.assignment.id],
        )
        self.payload = {
            "planting_location": self.planting_location.id,
            "start_date": "2024-01-01",
            "end_date": "2024-09-01",
        }

    def test_update_assignment(self):
        self.authenticate()

        response = self.client.put(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.assignment.id)
        self.assertEqual(data["end_date"], "2024-09-01")
        self.assertIsNone(message)

    def test_update_assignment_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.put(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_assignment_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-detail",
            args=[another_planting.id, self.assignment.id],
        )

        response = self.client.put(url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_update_assignment_end_date_before_start_date(self):
        self.authenticate()

        payload = {
            **self.payload,
            "start_date": "2024-06-01",
            "end_date": "2024-01-01",
        }

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {"end_date": ["End date must be on or after start date."]},
        )

    def test_update_assignment_excludes_self_from_overlap_check(self):
        self.authenticate()

        payload = {
            **self.payload,
            "start_date": "2024-02-01",
            "end_date": "2024-07-01",
        }

        response = self.client.put(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_assignment_overlap_with_other(self):
        self.authenticate()

        other_location = PlantingLocationFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=other_location,
            start_date="2024-07-01",
            end_date="2024-12-01",
        )

        payload = {
            **self.payload,
            "start_date": "2024-01-01",
            "end_date": "2024-08-01",
        }

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "start_date": [
                    "This planting already has a location assignment "
                    "that overlaps with the given date range."
                ]
            },
        )

    def test_update_assignment_pot_occupied_by_other_planting(self):
        self.authenticate()

        pot = PlantingLocationFactory(
            user=self.user,
            location_type="POT",
            height="30.00",
            length=None,
        )
        other_planting = PlantingFactory(user=self.user)
        PlantingLocationAssignmentFactory(
            planting=other_planting,
            planting_location=pot,
            start_date="2024-01-01",
            end_date=None,
        )

        payload = {
            "planting_location": pot.id,
            "start_date": "2024-01-01",
            "end_date": "2024-09-01",
        }

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message,
            {
                "planting_location": [
                    "This location already has an active planting "
                    "for the given date range."
                ]
            },
        )

    def test_update_assignment_excludes_self_from_pot_occupied_check(self):
        self.authenticate()

        pot = PlantingLocationFactory(
            user=self.user,
            location_type="POT",
            height="30.00",
            length=None,
        )
        # Use a fresh planting with no other assignments so the same-planting
        # overlap check does not interfere with this test.
        planting = PlantingFactory(user=self.user)
        assignment = PlantingLocationAssignmentFactory(
            planting=planting,
            planting_location=pot,
            start_date="2024-01-01",
            end_date="2024-06-01",
        )
        url = reverse(
            "planting-location-assignment-detail",
            args=[planting.id, assignment.id],
        )

        payload = {
            "planting_location": pot.id,
            "start_date": "2024-01-01",
            "end_date": "2024-09-01",
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlantingLocationAssignmentPartialUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "PATCH"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
            end_date=None,
        )
        self.url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, self.assignment.id],
        )

    def test_partial_update_assignment_end_date(self):
        self.authenticate()

        response = self.client.patch(
            self.url, {"end_date": "2024-06-01"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.assignment.id)
        self.assertEqual(data["end_date"], "2024-06-01")
        self.assertIsNone(message)

    def test_partial_update_excludes_self_from_overlap_check(self):
        self.authenticate()

        response = self.client.patch(
            self.url,
            {"start_date": "2024-02-01"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_assignment_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.patch(
            url, {"end_date": "2024-06-01"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_partial_update_assignment_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-detail",
            args=[another_planting.id, self.assignment.id],
        )

        response = self.client.patch(
            url, {"end_date": "2024-06-01"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationAssignmentDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "DELETE"

    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.planting_location = PlantingLocationFactory(user=self.user)
        self.assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.planting_location,
            start_date="2024-01-01",
        )
        self.url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, self.assignment.id],
        )

    def test_delete_assignment(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            PlantingLocationAssignment.objects.filter(
                pk=self.assignment.id
            ).exists()
        )

    def test_delete_assignment_not_found(self):
        self.authenticate()

        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, 9999],
        )

        response = self.client.delete(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_delete_assignment_planting_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_planting = PlantingFactory(user=another_user)
        url = reverse(
            "planting-location-assignment-detail",
            args=[another_planting.id, self.assignment.id],
        )

        response = self.client.delete(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class PlantingLocationStatusAutoSyncTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.planting = PlantingFactory(user=self.user)
        self.pot_location = PlantingLocationFactory(
            user=self.user,
            location_type="POT",
            height="30.00",
            length=None,
        )
        self.ground_location = PlantingLocationFactory(
            user=self.user,
            location_type="GROUND",
        )
        self.url = reverse(
            "planting-location-assignment-list-create",
            args=[self.planting.id],
        )

    def test_create_assignment_creates_in_use_status(self):
        self.authenticate()

        self.client.post(
            self.url,
            {
                "planting_location": self.pot_location.id,
                "start_date": "2024-01-01",
            },
            format="json",
        )

        self.assertEqual(
            PlantingLocationStatus.objects.filter(
                planting_location=self.pot_location, status="IN_USE"
            ).count(),
            1,
        )

    def test_create_assignment_ground_does_not_create_status(self):
        self.authenticate()

        self.client.post(
            self.url,
            {
                "planting_location": self.ground_location.id,
                "start_date": "2024-01-01",
            },
            format="json",
        )

        self.assertEqual(
            PlantingLocationStatus.objects.filter(
                planting_location=self.ground_location
            ).count(),
            0,
        )

    def test_close_assignment_creates_available_status(self):
        self.authenticate()

        assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.pot_location,
            start_date="2024-01-01",
            end_date=None,
        )
        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, assignment.id],
        )

        self.client.patch(url, {"end_date": "2024-06-01"}, format="json")

        self.assertEqual(
            PlantingLocationStatus.objects.filter(
                planting_location=self.pot_location, status="AVAILABLE"
            ).count(),
            1,
        )

    def test_update_without_closing_does_not_create_status(self):
        self.authenticate()

        assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.pot_location,
            start_date="2024-01-01",
            end_date=None,
        )
        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, assignment.id],
        )

        self.client.patch(url, {"start_date": "2024-02-01"}, format="json")

        self.assertEqual(
            PlantingLocationStatus.objects.filter(
                planting_location=self.pot_location
            ).count(),
            0,
        )

    def test_delete_assignment_creates_available_status(self):
        self.authenticate()

        assignment = PlantingLocationAssignmentFactory(
            planting=self.planting,
            planting_location=self.pot_location,
            start_date="2024-01-01",
            end_date=None,
        )
        url = reverse(
            "planting-location-assignment-detail",
            args=[self.planting.id, assignment.id],
        )

        self.client.delete(url)

        self.assertEqual(
            PlantingLocationStatus.objects.filter(
                planting_location=self.pot_location, status="AVAILABLE"
            ).count(),
            1,
        )
