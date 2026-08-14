from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import PlantingDailyObservation
from ..openapi.planting_daily_observation.examples import \
    PLANTING_DAILY_OBSERVATION_SERIALIZER_EXAMPLE
from .utils import UploadableImageField, validate_image_file


@extend_schema_serializer(
    examples=[PLANTING_DAILY_OBSERVATION_SERIALIZER_EXAMPLE]
)
class PlantingDailyObservationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the observation.",
    )
    stage = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True,
        help_text="ID of the associated growth stage, if any.",
    )
    stage_name = serializers.SerializerMethodField(
        help_text="Display name of the associated growth stage.",
    )

    # Health
    health_status = serializers.ChoiceField(
        choices=PlantingDailyObservation.HEALTH_STATUS_CHOICES,
        default="GOOD",
        help_text="Overall health status of the plant.",
    )
    pest_pressure = serializers.ChoiceField(
        choices=PlantingDailyObservation.PEST_PRESSURE_CHOICES,
        default="NONE",
        help_text="Level of pest pressure observed.",
    )
    disease_symptoms = serializers.BooleanField(
        default=False,
        help_text="Whether disease symptoms are present.",
    )
    watered = serializers.BooleanField(
        default=False,
        help_text=("Whether the planting was watered during this observation."),
    )
    rained = serializers.BooleanField(
        default=False,
        help_text="Whether watering was skipped because it rained.",
    )

    fertilizer_type = serializers.ChoiceField(
        choices=PlantingDailyObservation.FERTILIZER_TYPE_CHOICES,
        default="NONE",
        help_text="Whether the plant was fertilized and with what category.",
    )
    fertilizer_detail = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text=(
            "Optional detail, e.g. 'fermented swamp fertilizer',"
            " 'fish emulsion'."
        ),
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about this observation.",
    )
    image = UploadableImageField(
        required=False,
        allow_null=True,
        help_text="Optional image documenting this observation.",
    )
    observation_date = serializers.DateField(
        required=False,
        help_text=(
            "The date this observation was recorded " "(defaults to today)."
        ),
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this observation was recorded.",
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this observation was last updated.",
    )

    def get_stage_name(self, obj) -> str | None:
        if obj.stage:
            return str(obj.stage.get_stage_display())
        return None

    def validate_image(self, value):
        if value in (None, ""):
            return None
        return validate_image_file(value)

    def update(self, instance, validated_data):
        if (
            "image" in validated_data
            and validated_data["image"] is None
            and instance.image
        ):
            instance.image.delete(save=False)
        return super().update(instance, validated_data)

    class Meta:
        model = PlantingDailyObservation
        fields = (
            "id",
            "stage",
            "stage_name",
            "health_status",
            "pest_pressure",
            "disease_symptoms",
            "watered",
            "rained",
            "fertilizer_type",
            "fertilizer_detail",
            "notes",
            "image",
            "observation_date",
            "created_at",
            "updated_at",
        )
