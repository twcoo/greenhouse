from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Crop
from .utils import CustomReponseSerializer


class CropSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier of the crop"
    )
    name = serializers.CharField(
        max_length=50, help_text="Common name of the crop"
    )
    scientific_name = serializers.CharField(
        max_length=100, help_text="Scientific (Latin) name of the crop"
    )
    category = serializers.ChoiceField(
        choices=Crop.CATEGORY_CHOICES,
        default="VEGETABLE",
        help_text="Category of the crop",
    )
    sunlight_requirement = serializers.ChoiceField(
        choices=Crop.SUNLIGHT_REQUIREMENT_CHOICES,
        default="FULL SUN",
        help_text="Sunlight requirement of the crop",
    )
    min_days_to_harvest = serializers.IntegerField(
        min_value=1, help_text="Estimated minimum number of days until harvest"
    )
    max_days_to_harvest = serializers.IntegerField(
        min_value=1, help_text="Estimated maximum number of days until harvest"
    )

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
                message="Record already exist.",
            )
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Crop list example",
            summary="Typical crop object",
            value={
                "status": "success",
                "message": None,
                "data": [
                    {
                        "id": 34,
                        "name": "Tomato",
                        "scientific_name": "Solanum lycopersicum",
                        "category": "VEGETABLE",
                        "sunlight_requirement": "FULL SUN",
                        "min_days_to_harvest": 60,
                        "max_days_to_harvest": 90,
                    }
                ],
            },
        )
    ]
)
class CropListResponseSerializer(CustomReponseSerializer):
    data = CropSerializer(many=True)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Crop list example",
            summary="Typical crop object",
            value={
                "status": "success",
                "message": None,
                "data": {
                    "id": 34,
                    "name": "Tomato",
                    "scientific_name": "Solanum lycopersicum",
                    "category": "VEGETABLE",
                    "sunlight_requirement": "FULL SUN",
                    "min_days_to_harvest": 60,
                    "max_days_to_harvest": 90,
                },
            },
        )
    ]
)
class CropResponseSerializer(CustomReponseSerializer):
    data = CropSerializer()
