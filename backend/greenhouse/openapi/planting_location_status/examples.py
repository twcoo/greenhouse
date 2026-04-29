from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_LOCATION_STATUS_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Location Status",
    description="Example of a planting location status entry.",
    value={
        "id": 1,
        "status": "AVAILABLE",
        "notes": "Cleaned and ready for next planting.",
        "image": None,
        "created_at": "2024-03-01T00:00:00Z",
    },
)

CREATE_PLANTING_LOCATION_STATUS_REQUEST_EXAMPLE = OpenApiExample(
    name="Create planting location status payload",
    summary="Record a new status for a planting location",
    description=(
        "Example request payload for recording a new status entry "
        "for a planting location."
    ),
    value={
        "status": "DAMAGED",
        "notes": "Cracked from heat exposure during dry season.",
    },
    media_type="multipart/form-data",
    request_only=True,
)

CREATE_PLANTING_LOCATION_STATUS_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location status created",
    summary="Successfully recorded planting location status",
    description=(
        "Example response returned after a planting location status "
        "entry is successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "status": "DAMAGED",
            "notes": "Cracked from heat exposure during dry season.",
            "image": None,
            "created_at": "2024-03-01T00:00:00Z",
        },
        "message": None,
    },
)

PLANTING_LOCATION_STATUS_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "Example response returned when the status field is "
        "missing from the request payload."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {"status": ["This field is required."]},
    },
)

PLANTING_LOCATION_STATUS_INVALID_CHOICE_EXAMPLE = OpenApiExample(
    name="Invalid status choice",
    summary="Status value is not a valid choice",
    description=(
        "Example response returned when the status value is not one "
        "of the accepted choices."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "status": ['"UNKNOWN" is not a valid choice.'],
        },
    },
)

PLANTING_LOCATION_STATUS_LOCATION_IN_USE_EXAMPLE = OpenApiExample(
    name="Location is in use",
    summary="Status change blocked while location is in use",
    description=(
        "Example response returned when attempting to manually set "
        "a status on a location whose current status is IN_USE."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": ["Cannot set status while the location is in use."],
    },
)

PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location not found",
    summary="No planting location exists with the provided ID.",
    description=(
        "Example response returned when no planting location "
        "exists for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)
