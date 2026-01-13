from django.db import models


class Crop(models.Model):
    CATEGORY_CHOICES = [("VEGETABLE", "Vegetable"), ("FRUIT", "Fruit")]
    SUNLIGHT_REQUIREMENT_CHOICES = [
        ("FULL SUN", "Full Sun"),
        ("PART SUN", "Part Sun"),
        ("FULL SHADE", "Full Shade"),
    ]

    name = models.CharField(max_length=50)
    scientific_name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=15, choices=CATEGORY_CHOICES, default="VEGETABLE"
    )
    sunlight_requirement = models.CharField(
        max_length=15, choices=SUNLIGHT_REQUIREMENT_CHOICES
    )
    min_days_to_harverst = models.IntegerField()
    max_days_to_harverst = models.IntegerField()
