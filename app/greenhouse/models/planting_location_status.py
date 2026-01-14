from django.db import models

from .planting_location import PlantingLocation


class PlantingLocationStatus(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("IN_USE", "In Use"),
        ("DAMAGED", "Damaged"),
        ("DESTROYED", "Destroyed"),
        ("RETIRED", "Retired"),
    ]

    planting_location = models.ForeignKey(
        PlantingLocation,
        related_name="status_history",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to="locations/")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
