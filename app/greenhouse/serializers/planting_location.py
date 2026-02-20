from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import PlantingLocation


class PlantingLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier of the planting location."
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True,
        help_text="ID of the user who owns this planting location.",
    )
    name = serializers.CharField(
        max_length=50, help_text="Human-readable name of the planting location."
    )
    location_type = serializers.ChoiceField(
        choices=PlantingLocation.LOCATION_TYPE_CHOICES,
        help_text="Type of planting location.",
    )
    height = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Height of the planting location, in cm. Required for pot locations.",
    )
    width = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Width of the planting location, in cm.",
    )
    length = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Length of the planting location, in meters. Required for ground locations.",
    )

    def validate(self, attrs):
        location_type = attrs.get(
            "location_type", getattr(self.instance, "location_type", None)
        )
        length = attrs.get("length", getattr(self.instance, "length", None))
        height = attrs.get("height", getattr(self.instance, "height", None))

        if location_type == "GROUND" and not length:
            raise serializers.ValidationError(
                {"length": "Length is required for ground locations."}
            )

        if location_type in ["NURSERYPOT", "POT"] and not height:
            raise serializers.ValidationError(
                {"height": "Height is required for pot locations."}
            )

    class Meta:
        model = PlantingLocation
        fields = (
            "id",
            "user_id",
            "name",
            "location_type",
            "height",
            "width",
            "length",
        )
