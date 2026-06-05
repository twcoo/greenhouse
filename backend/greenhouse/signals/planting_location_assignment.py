from typing import Any

from django.db.models.signals import post_delete

from greenhouse.models.planting_location_assignment import \
    PlantingLocationAssignment
from greenhouse.models.planting_location_status import PlantingLocationStatus


def set_location_available_on_assignment_delete(
    sender: type,
    instance: PlantingLocationAssignment,
    **kwargs: Any,
) -> None:
    location = instance.planting_location
    if location.location_type in ["NURSERYPOT", "POT"]:
        PlantingLocationStatus.objects.create(
            planting_location=location, status="AVAILABLE"
        )


post_delete.connect(
    set_location_available_on_assignment_delete,
    sender=PlantingLocationAssignment,
)
