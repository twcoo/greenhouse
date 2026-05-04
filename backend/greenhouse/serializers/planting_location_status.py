from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import PlantingLocationStatus
from ..openapi.planting_location_status.examples import \
    PLANTING_LOCATION_STATUS_SERIALIZER_EXAMPLE
from .utils import validate_image_file


@extend_schema_serializer(
    examples=[PLANTING_LOCATION_STATUS_SERIALIZER_EXAMPLE]
)
class PlantingLocationStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the planting location status.",
    )
    status = serializers.ChoiceField(
        choices=PlantingLocationStatus.STATUS_CHOICES,
        help_text="Status of the planting location.",
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about this status entry.",
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Optional image documenting this status.",
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this status entry was recorded.",
    )

    def validate_image(self, value):
        if value is None:
            return value
        return validate_image_file(value)

    class Meta:
        model = PlantingLocationStatus
        fields = ("id", "status", "notes", "image", "created_at")
