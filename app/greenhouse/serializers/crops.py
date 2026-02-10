from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from ..models import Crop
from ..openapi.examples import CROP_SERIALIZER_EXAMPLE


@extend_schema_serializer(examples=[CROP_SERIALIZER_EXAMPLE])
class CropSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier of the crop"
    )
    name = serializers.CharField(
        max_length=50,
        help_text="Common name of the crop",
        validators=[
            UniqueValidator(
                queryset=Crop.objects.all(),
                message="A crop with this name already exists.",
            )
        ],
    )
    scientific_name = serializers.CharField(
        max_length=100,
        help_text="Scientific (Latin) name of the crop",
        validators=[
            UniqueValidator(
                queryset=Crop.objects.all(),
                message="A crop with this scientific name already exists.",
            )
        ],
    )
    category = serializers.ChoiceField(
        choices=Crop.CATEGORY_CHOICES, help_text="Category of the crop"
    )
    sunlight_requirement = serializers.ChoiceField(
        choices=Crop.SUNLIGHT_REQUIREMENT_CHOICES,
        help_text="Sunlight requirement of the crop",
    )
    min_days_to_harvest = serializers.IntegerField(
        min_value=1, help_text="Estimated minimum number of days until harvest"
    )
    max_days_to_harvest = serializers.IntegerField(
        min_value=1, help_text="Estimated maximum number of days until harvest"
    )

    def validate_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Name must be a valid string.")

        return value

    def validate_scientific_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError(
                "Scientific name must be a valid string."
            )

        return value

    class Meta:
        model = Crop
        fields = (
            "id",
            "name",
            "scientific_name",
            "category",
            "sunlight_requirement",
            "min_days_to_harvest",
            "max_days_to_harvest",
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Crop.objects.all(),
                fields=["name", "scientific_name"],
                message="A crop with the same name and scientific name already exists.",
            )
        ]
