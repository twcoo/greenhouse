from django.db import models
from django.utils import timezone

from .planting import Planting
from .planting_growth_stage import PlantingGrowthStage


class PlantingDailyObservation(models.Model):
    HEALTH_STATUS_CHOICES = [
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
    ]
    PEST_PRESSURE_CHOICES = [
        ("NONE", "None"),
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    FERTILIZER_TYPE_CHOICES = [
        ("NONE", "None"),
        ("ORGANIC", "Organic"),
        ("SYNTHETIC", "Synthetic"),
    ]
    WATERING_EVENT_CHOICES = [
        ("NONE", "None"),
        ("WATERED", "Watered"),
        ("RAINED", "Rained"),
        ("SKIPPED_WET", "Soil still wet"),
    ]

    planting = models.ForeignKey(
        Planting, related_name="daily_observations", on_delete=models.CASCADE
    )
    stage = models.ForeignKey(
        PlantingGrowthStage, null=True, blank=True, on_delete=models.SET_NULL
    )

    # Health
    health_status = models.CharField(
        max_length=20, choices=HEALTH_STATUS_CHOICES, default="GOOD"
    )
    pest_pressure = models.CharField(
        max_length=20, choices=PEST_PRESSURE_CHOICES, default="NONE"
    )
    disease_symptoms = models.BooleanField(default=False)
    watering_event = models.CharField(
        max_length=20,
        choices=WATERING_EVENT_CHOICES,
        default="NONE",
    )
    pruned = models.BooleanField(default=False)
    pruning_detail = models.CharField(max_length=200, blank=True, default="")

    fertilizer_type = models.CharField(
        max_length=20,
        choices=FERTILIZER_TYPE_CHOICES,
        default="NONE",
    )
    fertilizer_detail = models.CharField(max_length=200, blank=True, default="")

    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="observations/", null=True, blank=True)
    observation_date = models.DateField(
        default=timezone.localdate,
        help_text="The date this observation was recorded.",
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
