from django.db import models


class PlantingLocation(models.Model):
    LOCATION_TYPE_CHOICES = [
        ("NURSERYPOT", "Nursery Pot"),
        ("POT", "Pot"),
        ("GROUND", "Ground"),
    ]

    name = models.CharField(max_length=50)
    location_type = models.CharField(
        max_length=20, choices=LOCATION_TYPE_CHOICES
    )
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
