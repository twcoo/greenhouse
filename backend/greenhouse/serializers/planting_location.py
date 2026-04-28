from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import PlantingLocation
from ..openapi.planting_location.examples import \
    PLANTING_LOCATION_SERIALIZER_EXAMPLE
from .planting_location_status import PlantingLocationStatusSerializer
from .utils import UploadImageSerializer


@extend_schema_serializer(examples=[PLANTING_LOCATION_SERIALIZER_EXAMPLE])
class PlantingLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier of the planting location."
    )
    name = serializers.CharField(
        max_length=50, help_text="Human-readable name of the planting location."
    )
    location_type = serializers.ChoiceField(
        choices=PlantingLocation.LOCATION_TYPE_CHOICES,
        help_text="Type of planting location.",
    )
    current_status = serializers.SerializerMethodField(
        help_text="The most recent status entry for this location, or null.",
    )
    height = serializers.DecimalField(
        required=False,
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
        required=False,
        max_digits=6,
        decimal_places=2,
        help_text="Length of the planting location, in meters. Required for ground locations.",
    )

    def get_current_status(self, instance):
        latest = instance.status_history.order_by("-pk").first()
        if latest is None:
            return None
        return PlantingLocationStatusSerializer(latest).data

    def validate(self, attrs):
        location_type = attrs.get(
            "location_type", getattr(self.instance, "location_type", None)
        )
        length = attrs.get("length", getattr(self.instance, "length", None))
        height = attrs.get("height", getattr(self.instance, "height", None))

        if location_type == "GROUND":
            if not length:
                raise serializers.ValidationError(
                    {"length": "Length is required for ground locations."}
                )

            if height:
                raise serializers.ValidationError(
                    {
                        "height": "Height must not be provided for ground locations."
                    }
                )

        if location_type in ["NURSERYPOT", "POT"]:
            if not height:
                raise serializers.ValidationError(
                    {"height": "Height is required for pot locations."}
                )

            if length:
                raise serializers.ValidationError(
                    {
                        "length": "Length must not be provided for ground locations."
                    }
                )

        return attrs

    class Meta:
        model = PlantingLocation
        fields = (
            "id",
            "name",
            "location_type",
            "height",
            "width",
            "length",
            "current_status",
        )


class PlantingLocationImageSerializer(UploadImageSerializer):
    class Meta:
        model = PlantingLocation
        fields = ["image"]
