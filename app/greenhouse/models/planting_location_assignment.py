from django.db import models

from .planting import Planting
from .planting_location import PlantingLocation


class PlantingLocationAssignment(models.Model):
    planting = models.ForeignKey(
        Planting, related_name="locations", on_delete=models.CASCADE
    )
    planting_location = models.ForeignKey(PlantingLocation, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
