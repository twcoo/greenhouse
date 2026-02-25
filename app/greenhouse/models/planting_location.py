from django.contrib.auth.models import User
from django.db import models


class PlantingLocation(models.Model):
    LOCATION_TYPE_CHOICES = [
        ("NURSERYPOT", "Nursery Pot"),
        ("POT", "Pot"),
        ("GROUND", "Ground"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="planting_locations",
    )
    name = models.CharField(max_length=50)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="planting_locations/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
