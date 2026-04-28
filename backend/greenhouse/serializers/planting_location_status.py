from rest_framework import serializers

from ..models import PlantingLocationStatus


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

    class Meta:
        model = PlantingLocationStatus
        fields = ("id", "status", "notes", "image", "created_at")
