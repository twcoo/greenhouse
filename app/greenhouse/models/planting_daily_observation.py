from django.db import models

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

    planting = models.ForeignKey(
        Planting, related_name="daily_observations", on_delete=models.CASCADE
    )
    stage = models.ForeignKey(
        PlantingGrowthStage, null=True, blank=True, on_delete=models.SET_NULL
    )

    # Growth
    height_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    leaf_count = models.PositiveIntegerField(null=True, blank=True)

    # Environment
    temperature_c = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    humidity_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    light_hours = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    # Soil
    soil_moisture_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    soil_ph = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    ec_ms_cm = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )

    # Health
    health_status = models.CharField(
        max_length=20, choices=HEALTH_STATUS_CHOICES, default="GOOD"
    )
    pest_pressure = models.CharField(
        max_length=20, choices=PEST_PRESSURE_CHOICES, default="NONE"
    )
    disease_symptoms = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="observations/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
