from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from .crop import Crop


class Variety(models.Model):
    GROWTH_HABIT_CHOICES = [
        ("DETERMINATE", "Determinate"),
        ("INDETERMINATE", "Indeterminate"),
    ]

    name = models.CharField(max_length=50)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    growth_habit = ArrayField(
        models.CharField(max_length=15, choices=GROWTH_HABIT_CHOICES),
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["crop", "-created_at"],
                name="variety_crop_created_idx",
            ),
            GinIndex(
                fields=["name"],
                name="variety_name_trgm_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]
