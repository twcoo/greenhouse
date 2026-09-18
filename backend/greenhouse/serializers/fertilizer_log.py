from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import FertilizerLog
from ..openapi.fertilizer_log.examples import FERTILIZER_LOG_SERIALIZER_EXAMPLE


@extend_schema_serializer(examples=[FERTILIZER_LOG_SERIALIZER_EXAMPLE])
class FertilizerLogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the log entry.",
    )
    event_type = serializers.ChoiceField(
        choices=FertilizerLog.EVENT_TYPE_CHOICES,
        default="OTHER",
        help_text="Type of action recorded in this log entry.",
    )
    item_added = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Item or ingredient that was added, if any.",
    )
    quantity = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Quantity or amount that was added, if any.",
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about this log entry.",
    )
    log_date = serializers.DateField(
        required=False,
        help_text="The date this log entry was recorded (defaults to today).",
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this log entry was recorded.",
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this log entry was last updated.",
    )

    class Meta:
        model = FertilizerLog
        fields = (
            "id",
            "event_type",
            "item_added",
            "quantity",
            "notes",
            "log_date",
            "created_at",
            "updated_at",
        )
