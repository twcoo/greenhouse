from django.db import models

from .variety import Variety


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
        max_length=9, choices=CATEGORY_CHOICES, default="VEGETABLE"
    )
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    sunlight_requirement = models.CharField(
        max_length=10, choices=SUNLIGHT_REQUIREMENT_CHOICES
    )
    min_days_to_harverst = models.IntegerField()
    max_days_to_harverst = models.IntegerField()
