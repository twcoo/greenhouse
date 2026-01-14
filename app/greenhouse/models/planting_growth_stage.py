from django.db import models

from .planting import Planting


class PlantingGrowthStage(models.Model):
    STAGE_CHOICES = [
        ("SOWING", "Sowing"),
        ("GERMINATION", "Germination"),
        ("TRANSPLANTING", "Transplanting"),
        ("VEGETATIVE", "Vegetative"),
        ("FLOWERING", "Flowering"),
        ("FRUITING", "Fruiting"),
        ("HARVEST", "Harvest"),
    ]

    planting = models.ForeignKey(
        Planting, related_name="stages", on_delete=models.CASCADE
    )
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    image = models.ImageField(upload_to="stages/")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
