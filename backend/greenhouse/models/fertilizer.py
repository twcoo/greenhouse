from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Fertilizer(models.Model):
    TYPE_CHOICES = [
        ("SWAMP", "Swamp"),
        ("COMPOST", "Compost"),
        ("OTHER", "Other"),
    ]
    STATUS_CHOICES = [
        ("BREWING", "Brewing"),
        ("READY", "Ready"),
        ("USED", "Used"),
        ("DISCARDED", "Discarded"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fertilizers"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="SWAMP"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="BREWING"
    )
    start_date = models.DateField(
        default=timezone.localdate,
        help_text="The date this fertilizer batch was started.",
    )
    ingredients = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
    )
    log_added_ingredients = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
