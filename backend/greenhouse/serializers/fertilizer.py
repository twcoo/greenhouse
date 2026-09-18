from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import Fertilizer
from ..openapi.fertilizer.examples import FERTILIZER_SERIALIZER_EXAMPLE


@extend_schema_serializer(examples=[FERTILIZER_SERIALIZER_EXAMPLE])
class FertilizerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the fertilizer.",
    )
    name = serializers.CharField(
        max_length=100,
        help_text="Name of the fertilizer batch.",
    )
    type = serializers.ChoiceField(
        choices=Fertilizer.TYPE_CHOICES,
        default="SWAMP",
        help_text="Category of the fertilizer.",
    )
    status = serializers.ChoiceField(
        choices=Fertilizer.STATUS_CHOICES,
        default="BREWING",
        help_text="Current status of the fertilizer batch.",
    )
    start_date = serializers.DateField(
        required=False,
        help_text="The date this fertilizer batch was started.",
    )
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list,
        help_text="List of ingredients in the fertilizer.",
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about this fertilizer.",
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this fertilizer was created.",
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this fertilizer was last updated.",
    )

    class Meta:
        model = Fertilizer
        fields = (
            "id",
            "name",
            "type",
            "status",
            "start_date",
            "ingredients",
            "notes",
            "created_at",
            "updated_at",
        )
