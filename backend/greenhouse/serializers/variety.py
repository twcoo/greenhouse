from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import Crop, Variety
from ..openapi.variety.examples import VARIETY_SERIALIZER_EXAMPLE


@extend_schema_serializer(examples=[VARIETY_SERIALIZER_EXAMPLE])
class VarietySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the variety.",
    )
    name = serializers.CharField(
        max_length=50,
        help_text="Human-readable name of the variety.",
    )
    crop = serializers.PrimaryKeyRelatedField(
        queryset=Crop.objects.none(),
        help_text="ID of the crop this variety belongs to.",
    )
    crop_name = serializers.SerializerMethodField(
        help_text="Name of the crop this variety belongs to.",
    )
    growth_habit = serializers.ListField(
        child=serializers.ChoiceField(choices=Variety.GROWTH_HABIT_CHOICES),
        help_text=(
            "Growth habit of the variety. "
            "Accepted values: DETERMINATE, INDETERMINATE."
        ),
    )

    def get_crop_name(self, obj: Variety) -> str:
        return str(obj.crop.name)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["crop"].queryset = Crop.objects.filter(user=request.user)
        return fields

    class Meta:
        model = Variety
        fields = ("id", "name", "crop", "crop_name", "growth_habit")
