from typing import Any

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import Crop, Planting, Variety
from ..openapi.planting.examples import PLANTING_SERIALIZER_EXAMPLE


@extend_schema_serializer(examples=[PLANTING_SERIALIZER_EXAMPLE])
class PlantingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the planting.",
    )
    crop = serializers.PrimaryKeyRelatedField(
        queryset=Crop.objects.none(),
        help_text="ID of the crop being planted.",
    )
    variety = serializers.PrimaryKeyRelatedField(
        queryset=Variety.objects.none(),
        help_text="ID of the variety being planted.",
    )
    crop_name = serializers.SerializerMethodField(
        help_text="Name of the crop being planted.",
    )
    variety_name = serializers.SerializerMethodField(
        help_text="Name of the variety being planted.",
    )
    current_location = serializers.SerializerMethodField(
        help_text=("Name of the currently active planting location, if any."),
    )
    has_daily_observation = serializers.BooleanField(
        read_only=True,
        help_text=(
            "Whether this planting has a daily observation "
            "recorded for today."
        ),
    )

    def get_crop_name(self, obj: Planting) -> str:
        return str(obj.crop.name)

    def get_variety_name(self, obj: Planting) -> str:
        return str(obj.variety.name)

    def get_current_location(self, obj: Planting) -> str | None:
        active = next(
            (a for a in obj.locations.all() if a.end_date is None),
            None,
        )
        return str(active.planting_location.name) if active else None

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["crop"].queryset = Crop.objects.filter(user=request.user)
            fields["variety"].queryset = Variety.objects.filter(
                crop__user=request.user
            )
        return fields

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        variety = data.get("variety")
        crop = data.get("crop")
        if variety and crop is None and self.instance:
            crop = self.instance.crop
        if variety and crop and variety.crop != crop:
            raise serializers.ValidationError(
                {"variety": ("Variety does not belong to the selected crop.")}
            )
        return data

    class Meta:
        model = Planting
        fields = (
            "id",
            "crop",
            "crop_name",
            "variety",
            "variety_name",
            "current_location",
            "has_daily_observation",
            "created_at",
        )
