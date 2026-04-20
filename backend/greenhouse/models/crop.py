from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Crop(models.Model):
    CATEGORY_CHOICES = [("VEGETABLE", "Vegetable"), ("FRUIT", "Fruit")]
    SUNLIGHT_REQUIREMENT_CHOICES = [
        ("FULL SUN", "Full Sun"),
        ("PART SUN", "Part Sun"),
        ("FULL SHADE", "Full Shade"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="crops",
    )
    name = models.CharField(max_length=50, unique=True)
    scientific_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
    )
    sunlight_requirement = models.CharField(
        max_length=15,
        choices=SUNLIGHT_REQUIREMENT_CHOICES,
    )
    min_days_to_harvest = models.IntegerField()
    max_days_to_harvest = models.IntegerField()
    image = models.ImageField(upload_to="crops/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "-created_at"],
                name="crop_user_created_idx",
            ),
            GinIndex(
                fields=["name"],
                name="crop_name_trgm_idx",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["scientific_name"],
                name="crop_scientific_name_trgm_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]
