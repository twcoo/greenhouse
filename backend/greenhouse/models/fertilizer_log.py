from django.db import models
from django.utils import timezone

from .fertilizer import Fertilizer


class FertilizerLog(models.Model):
    EVENT_TYPE_CHOICES = [
        ("ADDED_INGREDIENT", "Added Ingredient"),
        ("ADDED_WATER", "Added Water"),
        ("STIRRED", "Stirred"),
        ("OTHER", "Other"),
    ]

    fertilizer = models.ForeignKey(
        Fertilizer, related_name="logs", on_delete=models.CASCADE
    )
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPE_CHOICES, default="OTHER"
    )
    item_added = models.CharField(max_length=100, blank=True, default="")
    quantity = models.CharField(max_length=50, blank=True, default="")
    notes = models.TextField(blank=True)
    log_date = models.DateField(
        default=timezone.localdate,
        help_text="The date this log entry was recorded.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-log_date", "-pk"]
