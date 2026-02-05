from django.db import models


class Crop(models.Model):
    CATEGORY_CHOICES = [("VEGETABLE", "Vegetable"), ("FRUIT", "Fruit")]
    SUNLIGHT_REQUIREMENT_CHOICES = [
        ("FULL SUN", "Full Sun"),
        ("PART SUN", "Part Sun"),
        ("FULL SHADE", "Full Shade"),
    ]

    name = models.CharField(max_length=50, unique=True)
    scientific_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=15, choices=CATEGORY_CHOICES, default="VEGETABLE"
    )
    sunlight_requirement = models.CharField(
        max_length=15, choices=SUNLIGHT_REQUIREMENT_CHOICES, default="FULL SUN"
    )
    min_days_to_harvest = models.IntegerField()
    max_days_to_harvest = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
