from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Fertilizer, FertilizerLog
from .commons.factories import FertilizerFactory, UserFactory
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin


class FertilizerListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("fertilizer-list-create")
        self.another_user = UserFactory(username="shimmer2")
        self.another_user_fertilizers = FertilizerFactory.create_batch(
            12, user=self.another_user
        )

    def test_list_empty_fertilizers(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, fertilizers, message = (
            self.get_response_data_many(response)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(fertilizers, [])
        self.assertEqual(data["count"], 0)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=fertilizers,
            another_user_data=self.another_user_fertilizers,
        )

    def test_list_populated_fertilizers(self):
        self.authenticate()

        created = FertilizerFactory.create_batch(3, user=self.user)

        response = self.client.get(self.url)

        response_status, data, fertilizers, message = (
            self.get_response_data_many(response)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(fertilizers), 3)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(message)
        self.validate_no_cross_user_data_leakage(
            user_data=fertilizers,
            another_user_data=self.another_user_fertilizers,
        )

        returned_by_id = {row["id"]: row for row in fertilizers}
        self.assertEqual(set(returned_by_id), {item.id for item in created})
        for fertilizer in created:
            row = returned_by_id[fertilizer.id]
            self.assertEqual(row["name"], fertilizer.name)
            self.assertEqual(row["type"], fertilizer.type)
            self.assertEqual(row["status"], fertilizer.status)
            self.assertEqual(
                row["start_date"], fertilizer.start_date.isoformat()
            )
            self.assertEqual(row["ingredients"], fertilizer.ingredients)
            self.assertEqual(row["notes"], fertilizer.notes)

    def test_list_pagination(self):
        self.authenticate()

        created = FertilizerFactory.create_batch(15, user=self.user)

        response = self.client.get(self.url, {"page_size": 10})

        response_status, data, fertilizers, message = (
            self.get_response_data_many(response)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(fertilizers), 10)
        self.assertEqual(data["count"], 15)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertIsNone(message)
        self.assertTrue(
            {row["id"] for row in fertilizers}.issubset(
                {item.id for item in created}
            )
        )

    def test_list_search_by_name(self):
        self.authenticate()

        FertilizerFactory(user=self.user, name="Swamp Batch A")
        FertilizerFactory(user=self.user, name="Compost Batch")

        response = self.client.get(self.url, {"search": "Swamp"})

        response_status, _, fertilizers, _ = self.get_response_data_many(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(len(fertilizers), 1)
        self.assertEqual(fertilizers[0]["name"], "Swamp Batch A")

    def test_list_returns_ingredients_array(self):
        self.authenticate()

        FertilizerFactory(
            user=self.user,
            name="Swamp Batch",
            ingredients=["banana peels", "molasses"],
        )

        response = self.client.get(self.url)

        _, _, fertilizers, _ = self.get_response_data_many(response)

        self.assertEqual(
            fertilizers[0]["ingredients"], ["banana peels", "molasses"]
        )


class FertilizerCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.url = reverse("fertilizer-list-create")
        self.payload = {
            "name": "Swamp Fertilizer #1",
            "type": "SWAMP",
            "status": "BREWING",
            "start_date": date.today().isoformat(),
            "ingredients": ["banana peels", "molasses"],
            "notes": "Fermenting.",
        }

    def test_create_fertilizer_success(self):
        self.authenticate()

        response = self.client.post(self.url, self.payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], "Swamp Fertilizer #1")
        self.assertEqual(data["type"], "SWAMP")
        self.assertEqual(data["status"], "BREWING")
        self.assertEqual(data["ingredients"], ["banana peels", "molasses"])
        self.assertTrue(
            Fertilizer.objects.filter(
                name="Swamp Fertilizer #1", user=self.user
            ).exists()
        )
        self.assertIsNone(message)

    def test_create_fertilizer_defaults(self):
        self.authenticate()

        response = self.client.post(
            self.url, {"name": "Minimal"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["type"], "SWAMP")
        self.assertEqual(data["status"], "BREWING")
        self.assertEqual(data["ingredients"], [])
        self.assertEqual(data["start_date"], date.today().isoformat())
        self.assertIsNone(message)

    def test_create_fertilizer_missing_name(self):
        self.authenticate()

        response = self.client.post(self.url, {}, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, {"name": ["This field is required."]})

    def test_create_fertilizer_invalid_type(self):
        self.authenticate()

        payload = {**self.payload, "type": "UNKNOWN"}

        response = self.client.post(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(
            message, {"type": ['"UNKNOWN" is not a valid choice.']}
        )


class FertilizerGetApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.url = reverse("fertilizer-detail", args=[self.fertilizer.id])
        self.url_not_found = reverse("fertilizer-detail", args=[9999])

    def test_get_fertilizer(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.fertilizer.id)
        self.assertEqual(data["name"], self.fertilizer.name)
        self.assertEqual(data["type"], self.fertilizer.type)
        self.assertEqual(data["status"], self.fertilizer.status)
        self.assertEqual(
            data["start_date"], self.fertilizer.start_date.isoformat()
        )
        self.assertEqual(data["ingredients"], self.fertilizer.ingredients)
        self.assertEqual(data["notes"], self.fertilizer.notes)
        self.assertIsNone(message)

    def test_get_fertilizer_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_fertilizer = FertilizerFactory(user=another_user)

        url = reverse("fertilizer-detail", args=[another_fertilizer.id])

        response = self.client.get(url)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")

    def test_get_fertilizer_not_found(self):
        self.authenticate()

        response = self.client.get(self.url_not_found)

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_status, "error")
        self.assertIsNone(data)
        self.assertEqual(message, "Resource not found.")


class FertilizerUpdateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.url = reverse("fertilizer-detail", args=[self.fertilizer.id])
        self.url_not_found = reverse("fertilizer-detail", args=[9999])

    def test_update_fertilizer(self):
        self.authenticate()

        payload = {
            "name": "Updated Name",
            "type": "COMPOST",
            "status": "READY",
            "ingredients": ["egg shells"],
            "notes": "Updated.",
        }

        response = self.client.put(self.url, payload, format="json")

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["id"], self.fertilizer.id)
        self.assertEqual(data["name"], "Updated Name")
        self.assertEqual(data["type"], "COMPOST")
        self.assertEqual(data["status"], "READY")
        self.assertEqual(data["ingredients"], ["egg shells"])
        self.assertEqual(data["notes"], "Updated.")
        self.assertIsNone(message)

    def test_partial_update_status(self):
        self.authenticate()

        response = self.client.patch(
            self.url, {"status": "READY"}, format="json"
        )

        response_status, data, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(data["status"], "READY")
        self.assertIsNone(message)

    def test_update_prunes_stale_log_added_ingredient(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "egg shells"],
            log_added_ingredients=["egg shells"],
        )

        response = self.client.patch(
            self.url, {"ingredients": ["banana peels"]}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.ingredients, ["banana peels"])
        self.assertEqual(self.fertilizer.log_added_ingredients, [])

    def test_update_keeps_log_added_ingredient_still_present(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "egg shells"],
            log_added_ingredients=["egg shells"],
        )

        response = self.client.put(
            self.url,
            {
                "name": "Updated Name",
                "ingredients": ["banana peels", "egg shells"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.log_added_ingredients, ["egg shells"])

    def test_update_does_not_delete_log_entries(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["egg shells"],
            log_added_ingredients=["egg shells"],
        )
        log = FertilizerLog.objects.create(
            fertilizer=self.fertilizer,
            event_type="ADDED_INGREDIENT",
            item_added="egg shells",
        )

        response = self.client.patch(
            self.url, {"ingredients": []}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.ingredients, [])
        self.assertEqual(self.fertilizer.log_added_ingredients, [])
        self.assertTrue(FertilizerLog.objects.filter(pk=log.pk).exists())

    def test_update_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_fertilizer = FertilizerFactory(user=another_user)

        url = reverse("fertilizer-detail", args=[another_fertilizer.id])

        response = self.client.put(url, {"name": "X"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_found(self):
        self.authenticate()

        response = self.client.put(
            self.url_not_found, {"name": "X"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FertilizerDeleteApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.url = reverse("fertilizer-detail", args=[self.fertilizer.id])
        self.url_not_found = reverse("fertilizer-detail", args=[9999])

    def test_delete_fertilizer(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertFalse(
            Fertilizer.objects.filter(id=self.fertilizer.id).exists()
        )

    def test_delete_not_owned(self):
        self.authenticate()

        another_user = UserFactory(username="shimmer2")
        another_fertilizer = FertilizerFactory(user=another_user)

        url = reverse("fertilizer-detail", args=[another_fertilizer.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_found(self):
        self.authenticate()

        response = self.client.delete(self.url_not_found)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FertilizerLogCascadeTests(ResponseUtilsMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_delete_fertilizer_cascades_logs(self):
        fertilizer = FertilizerFactory(user=self.user)
        FertilizerLog.objects.create(
            fertilizer=fertilizer, event_type="ADDED_WATER"
        )
        self.assertEqual(
            FertilizerLog.objects.filter(fertilizer=fertilizer).count(), 1
        )

        self.client.force_authenticate(user=self.user)
        url = reverse("fertilizer-detail", args=[fertilizer.id])
        self.client.delete(url)

        self.assertEqual(
            FertilizerLog.objects.filter(fertilizer=fertilizer).count(), 0
        )
