from django.contrib.postgres.fields import ArrayField
from django.db import models


class Variety(models.Model):
    GROWTH_HABIT_CHOICES = [
        ("DETERMINATE", "Determinate"),
        ("INDETERMINATE", "Indeterminate"),
    ]

    name = models.CharField(max_length=50)
    growth_habit = ArrayField(
        models.CharField(max_length=13, choices=GROWTH_HABIT_CHOICES),
        default=list,
    )
