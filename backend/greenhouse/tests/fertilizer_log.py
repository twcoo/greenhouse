from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Fertilizer, FertilizerLog
from .commons.factories import (FertilizerFactory, FertilizerLogFactory,
                                UserFactory)
from .commons.mixins import RequiredAuthTestsMixin, ResponseUtilsMixin


class FertilizerLogListApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.url = reverse(
            "fertilizer-log-list-create", args=[self.fertilizer.id]
        )

    def test_list_empty_logs(self):
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

    def test_list_populated_logs(self):
        self.authenticate()

        water_log = FertilizerLogFactory(
            fertilizer=self.fertilizer,
            event_type="ADDED_WATER",
            item_added="",
            quantity="5 liters",
            notes="Topped up.",
        )
        ingredient_log = FertilizerLogFactory(
            fertilizer=self.fertilizer,
            event_type="ADDED_INGREDIENT",
            item_added="egg shells",
            quantity="1 kg",
            notes="Crushed first.",
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

        returned_by_id = {entry["id"]: entry for entry in entries}
        self.assertEqual(set(returned_by_id), {water_log.id, ingredient_log.id})
        for log in (water_log, ingredient_log):
            entry = returned_by_id[log.id]
            self.assertEqual(entry["event_type"], log.event_type)
            self.assertEqual(entry["item_added"], log.item_added)
            self.assertEqual(entry["quantity"], log.quantity)
            self.assertEqual(entry["notes"], log.notes)
            self.assertEqual(entry["log_date"], log.log_date.isoformat())

    def test_list_ordered_by_log_date_desc(self):
        self.authenticate()

        today = date.today()
        older = FertilizerLogFactory(
            fertilizer=self.fertilizer, log_date=today - timedelta(days=2)
        )
        newer = FertilizerLogFactory(fertilizer=self.fertilizer, log_date=today)

        response = self.client.get(self.url)

        _, _, entries, _ = self.get_response_data_many(response)

        self.assertEqual(entries[0]["id"], newer.id)
        self.assertEqual(entries[1]["id"], older.id)

    def test_list_does_not_return_other_fertilizer_logs(self):
        self.authenticate()

        other_fertilizer = FertilizerFactory(user=self.user)
        FertilizerLogFactory(fertilizer=other_fertilizer)
        FertilizerLogFactory(fertilizer=self.fertilizer)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 1)

    def test_list_does_not_return_other_user_logs(self):
        self.authenticate()

        other_user = UserFactory(username="other_log_list_user")
        other_fertilizer = FertilizerFactory(user=other_user)
        FertilizerLogFactory(fertilizer=other_fertilizer)

        response = self.client.get(self.url)

        _, data, _, _ = self.get_response_data_many(response)

        self.assertEqual(data["count"], 0)

    def test_list_fertilizer_not_found(self):
        self.authenticate()

        url = reverse("fertilizer-log-list-create", args=[9999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_other_user_fertilizer_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_log_404_user")
        other_fertilizer = FertilizerFactory(user=other_user)
        url = reverse("fertilizer-log-list-create", args=[other_fertilizer.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FertilizerLogCreateApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "POST"

    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.url = reverse(
            "fertilizer-log-list-create", args=[self.fertilizer.id]
        )

    def test_create_log_success(self):
        self.authenticate()

        data = {
            "event_type": "ADDED_INGREDIENT",
            "item_added": "banana peels",
            "quantity": "2 kg",
            "notes": "Chopped first.",
        }
        response = self.client.post(self.url, data, format="json")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["event_type"], "ADDED_INGREDIENT")
        self.assertEqual(response_data["item_added"], "banana peels")
        self.assertEqual(response_data["quantity"], "2 kg")
        self.assertEqual(response_data["notes"], "Chopped first.")
        self.assertEqual(response_data["log_date"], date.today().isoformat())
        self.assertIsNone(message)

    def test_create_log_defaults(self):
        self.authenticate()

        response = self.client.post(self.url, {}, format="json")

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["event_type"], "OTHER")
        self.assertEqual(response_data["item_added"], "")
        self.assertEqual(response_data["quantity"], "")
        self.assertEqual(response_data["log_date"], date.today().isoformat())

    def test_create_log_adds_new_ingredient_to_fertilizer(self):
        self.authenticate()

        data = {
            "event_type": "ADDED_INGREDIENT",
            "item_added": "egg shells",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fertilizer.refresh_from_db()
        self.assertIn("egg shells", self.fertilizer.ingredients)

    def test_create_log_duplicate_ingredient_skipped(self):
        self.authenticate()

        data = {
            "event_type": "ADDED_INGREDIENT",
            "item_added": "banana peels",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients, ["banana peels", "molasses"]
        )

    def test_create_log_non_ingredient_event_does_not_update_ingredients(self):
        self.authenticate()

        data = {
            "event_type": "ADDED_WATER",
            "item_added": "egg shells",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients, ["banana peels", "molasses"]
        )

    def test_create_log_invalid_event_type(self):
        self.authenticate()

        response = self.client.post(
            self.url, {"event_type": "UNKNOWN"}, format="json"
        )

        response_status, _, message = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_status, "error")
        self.assertEqual(
            message, {"event_type": ['"UNKNOWN" is not a valid choice.']}
        )

    def test_create_log_other_user_fertilizer_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_log_create_user")
        other_fertilizer = FertilizerFactory(user=other_user)
        url = reverse("fertilizer-log-list-create", args=[other_fertilizer.id])

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FertilizerLogDetailApiViewTests(
    RequiredAuthTestsMixin, ResponseUtilsMixin, APITestCase
):
    http_method = "PUT"

    def setUp(self):
        super().setUp()
        self.fertilizer = FertilizerFactory(user=self.user)
        self.log = FertilizerLogFactory(
            fertilizer=self.fertilizer, notes="Initial."
        )
        self.url = reverse(
            "fertilizer-log-detail",
            args=[self.fertilizer.id, self.log.id],
        )

    def test_update_log_success(self):
        self.authenticate()

        data = {
            "event_type": "ADDED_WATER",
            "quantity": "5 liters",
            "notes": "Topped up.",
        }
        response = self.client.put(self.url, data, format="json")

        response_status, response_data, message = self.get_response_data(
            response
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertEqual(response_data["event_type"], "ADDED_WATER")
        self.assertEqual(response_data["quantity"], "5 liters")
        self.assertEqual(response_data["notes"], "Topped up.")
        self.assertIsNone(message)

    def test_partial_update_notes(self):
        self.authenticate()

        response = self.client.patch(
            self.url, {"notes": "Updated."}, format="json"
        )

        _, response_data, _ = self.get_response_data(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["notes"], "Updated.")
        self.assertEqual(response_data["event_type"], self.log.event_type)

    def test_update_log_to_new_ingredient_updates_fertilizer(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
            log_added_ingredients=["banana peels"],
        )

        data = {"event_type": "ADDED_INGREDIENT", "item_added": "egg shells"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients, ["molasses", "egg shells"]
        )

    def test_update_log_to_non_ingredient_removes_ingredient(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
            log_added_ingredients=["banana peels"],
        )

        data = {"event_type": "ADDED_WATER"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.ingredients, ["molasses"])

    def test_update_log_keeps_ingredient_referenced_elsewhere(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
            log_added_ingredients=["banana peels"],
        )
        FertilizerLogFactory(
            fertilizer=self.fertilizer,
            event_type="ADDED_INGREDIENT",
            item_added="banana peels",
        )

        data = {"event_type": "ADDED_INGREDIENT", "item_added": "egg shells"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients,
            ["banana peels", "molasses", "egg shells"],
        )

    def test_update_log_keeps_manually_added_ingredient(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
        )

        data = {"event_type": "ADDED_WATER"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients, ["banana peels", "molasses"]
        )

    def test_update_other_user_log_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_log_update_user")
        other_fertilizer = FertilizerFactory(user=other_user)
        other_log = FertilizerLogFactory(fertilizer=other_fertilizer)
        url = reverse(
            "fertilizer-log-detail",
            args=[other_fertilizer.id, other_log.id],
        )

        response = self.client.put(url, {"notes": "x"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wrong_fertilizer_returns_404(self):
        self.authenticate()

        other_fertilizer = FertilizerFactory(user=self.user)
        url = reverse(
            "fertilizer-log-detail",
            args=[other_fertilizer.id, self.log.id],
        )

        response = self.client.put(url, {"notes": "x"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_found(self):
        self.authenticate()

        url = reverse("fertilizer-log-detail", args=[self.fertilizer.id, 9999])

        response = self.client.put(url, {"notes": "x"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_log_success(self):
        self.authenticate()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FertilizerLog.objects.filter(id=self.log.id).exists())

    def test_delete_log_removes_unreferenced_ingredient(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
            log_added_ingredients=["banana peels"],
        )

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.ingredients, ["molasses"])

    def test_delete_log_keeps_ingredient_referenced_elsewhere(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels"],
            log_added_ingredients=["banana peels"],
        )
        FertilizerLogFactory(
            fertilizer=self.fertilizer,
            event_type="ADDED_INGREDIENT",
            item_added="banana peels",
        )

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.fertilizer.refresh_from_db()
        self.assertEqual(self.fertilizer.ingredients, ["banana peels"])

    def test_delete_log_keeps_manually_added_ingredient(self):
        self.authenticate()
        Fertilizer.objects.filter(pk=self.fertilizer.pk).update(
            ingredients=["banana peels", "molasses"],
        )

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.fertilizer.refresh_from_db()
        self.assertEqual(
            self.fertilizer.ingredients, ["banana peels", "molasses"]
        )

    def test_delete_other_user_log_returns_404(self):
        self.authenticate()

        other_user = UserFactory(username="other_log_delete_user")
        other_fertilizer = FertilizerFactory(user=other_user)
        other_log = FertilizerLogFactory(fertilizer=other_fertilizer)
        url = reverse(
            "fertilizer-log-detail",
            args=[other_fertilizer.id, other_log.id],
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
