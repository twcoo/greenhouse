from datetime import date
from typing import Any

from django.db.models import Q
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from ..models import PlantingLocation, PlantingLocationAssignment
from ..openapi.planting_location_assignment.examples import \
    PLANTING_LOCATION_ASSIGNMENT_SERIALIZER_EXAMPLE


@extend_schema_serializer(
    examples=[PLANTING_LOCATION_ASSIGNMENT_SERIALIZER_EXAMPLE]
)
class PlantingLocationAssignmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier of the assignment.",
    )
    planting_location = serializers.PrimaryKeyRelatedField(
        queryset=PlantingLocation.objects.none(),
        help_text="ID of the planting location.",
    )
    planting_location_name = serializers.SerializerMethodField(
        help_text="Name of the planting location.",
    )
    start_date = serializers.DateField(
        help_text="Date the planting was moved to this location.",
    )
    end_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text=(
            "Date the planting left this location. "
            "Null means it is still here."
        ),
    )

    def get_planting_location_name(
        self, obj: PlantingLocationAssignment
    ) -> str:
        return str(obj.planting_location.name)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["planting_location"].queryset = (
                PlantingLocation.objects.filter(user=request.user)
            )
        return fields

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": ("End date must be on or after start date.")}
            )

        # planting is injected into context by the view, not taken from
        # request data. start_date may be absent on a PATCH that only
        # updates end_date, in which case there is nothing to check.
        planting = self.context.get("planting")

        if planting and not self.instance:
            active_qs = PlantingLocationAssignment.objects.filter(
                planting=planting, end_date__isnull=True
            )
            if active_qs.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": (
                            "This planting is currently assigned to a "
                            "location. End the current assignment before "
                            "adding a new one."
                        )
                    }
                )

        if planting and start_date:
            qs = PlantingLocationAssignment.objects.filter(planting=planting)
            # On updates, exclude the current instance so it doesn't
            # conflict with itself.
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.filter(end_date__isnull=True).exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "This planting already has an active location assignment."
                    }
                )

            # Find existing assignments that overlap with the new date range.
            # An overlap occurs when an existing assignment starts before the new one
            # ends, and ends after the new one starts (or is still open-ended).
            overlap_qs = qs.filter(
                start_date__lte=(end_date or date.max)
            ).filter(Q(end_date__isnull=True) | Q(end_date__gt=start_date))

            if overlap_qs.exists():
                raise serializers.ValidationError(
                    {
                        "start_date": (
                            "This planting already has a location "
                            "assignment that overlaps with the given "
                            "date range."
                        )
                    }
                )

        planting_location = data.get("planting_location")

        if (
            planting
            and planting_location
            and start_date
            and planting_location.location_type in ["NURSERYPOT", "POT"]
        ):
            location_qs = PlantingLocationAssignment.objects.filter(
                planting_location=planting_location
            ).exclude(planting=planting)

            if self.instance:
                location_qs = location_qs.exclude(pk=self.instance.pk)

            location_overlap_qs = location_qs.filter(
                start_date__lte=(end_date or date.max)
            ).filter(Q(end_date__isnull=True) | Q(end_date__gte=start_date))

            if location_overlap_qs.exists():
                raise serializers.ValidationError(
                    {
                        "planting_location": (
                            "This location already has an active "
                            "planting for the given date range."
                        )
                    }
                )

        return data

    class Meta:
        model = PlantingLocationAssignment
        fields = (
            "id",
            "planting_location",
            "planting_location_name",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        )
