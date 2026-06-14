from django.contrib.auth.models import User
from django.db import models

from .crop import Crop
from .variety import Variety


class Planting(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="plantings"
    )
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
