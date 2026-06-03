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

    # Growth
    height_cm = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Plant height in centimetres.",
    )
    leaf_count = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Number of leaves counted.",
    )

    # Environment
    temperature_c = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        required=False,
        allow_null=True,
        help_text="Ambient temperature in degrees Celsius.",
    )
    humidity_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Relative humidity percentage.",
    )
    light_hours = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Hours of light received.",
    )

    # Soil
    soil_moisture_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Soil moisture percentage.",
    )
    soil_ph = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        required=False,
        allow_null=True,
        help_text="Soil pH value.",
    )
    ec_ms_cm = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Electrical conductivity in mS/cm.",
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
        if value is None:
            return value
        return validate_image_file(value)

    class Meta:
        model = PlantingDailyObservation
        fields = (
            "id",
            "stage",
            "stage_name",
            "height_cm",
            "leaf_count",
            "temperature_c",
            "humidity_percent",
            "light_hours",
            "soil_moisture_percent",
            "soil_ph",
            "ec_ms_cm",
            "health_status",
            "pest_pressure",
            "disease_symptoms",
            "watered",
            "notes",
            "image",
            "created_at",
            "updated_at",
        )
