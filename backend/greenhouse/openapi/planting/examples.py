from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting",
    summary="Planting serializer example",
    description="Example paginated response containing a list of plantings.",
    value={
        "id": 1,
        "crop": 1,
        "crop_name": "Tomato",
        "variety": 1,
        "variety_name": "Sun Gold",
        "status": "ACTIVE",
        "current_location": None,
        "has_daily_observation": False,
        "created_at": "2024-01-01T00:00:00Z",
    },
)

CREATE_PLANTING_REQUEST_EXAMPLE = OpenApiExample(
    name="Create planting payload",
    summary="Create a planting",
    description="Example request payload for creating a planting.",
    value={"crop": 1, "variety": 1, "status": "ACTIVE"},
    request_only=True,
)

UPDATE_PLANTING_REQUEST_EXAMPLE = OpenApiExample(
    name="Update planting payload",
    summary="Update a planting",
    description="Example request payload for updating a planting.",
    value={"crop": 1, "variety": 2, "status": "HARVESTED"},
    request_only=True,
)

PARTIAL_UPDATE_PLANTING_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update planting payload",
    summary="Partially update a planting",
    description="Example request payload for partially updating a planting.",
    value={"status": "DEAD"},
    request_only=True,
)

CREATE_PLANTING_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting created example",
    summary="Successfully created planting",
    description=(
        "Example response returned after a planting is successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "crop": 1,
            "crop_name": "Tomato",
            "variety": 1,
            "variety_name": "Sun Gold",
            "status": "ACTIVE",
            "current_location": None,
            "has_daily_observation": False,
            "created_at": "2024-01-01T00:00:00Z",
        },
        "message": None,
    },
)

RETRIEVE_PLANTING_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting detail",
    summary="Retrieve a planting by ID",
    description="Example response returning planting details for the specified ID.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "crop": 1,
            "crop_name": "Tomato",
            "variety": 1,
            "variety_name": "Sun Gold",
            "status": "ACTIVE",
            "current_location": None,
            "has_daily_observation": False,
            "created_at": "2024-01-01T00:00:00Z",
        },
        "message": None,
    },
)

UPDATE_PLANTING_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting updated",
    summary="Planting updated successfully",
    description="Example response indicating the planting was successfully updated.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "crop": 1,
            "crop_name": "Tomato",
            "variety": 2,
            "variety_name": "Sweet 100",
            "status": "HARVESTED",
            "current_location": None,
            "has_daily_observation": False,
            "created_at": "2024-01-01T00:00:00Z",
        },
        "message": None,
    },
)

PLANTING_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting not found",
    summary="No planting exists with the provided ID.",
    description=(
        "Example response returned when no planting exists "
        "for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

PLANTING_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "Example response returned when required fields are "
        "missing in the request payload."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "crop": ["This field is required."],
            "variety": ["This field is required."],
        },
    },
)

PLANTING_VARIETY_CROP_MISMATCH_EXAMPLE = OpenApiExample(
    name="Variety does not belong to crop",
    summary="Cross-field validation error",
    description=(
        "Example response returned when the selected variety "
        "does not belong to the selected crop."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "variety": ["Variety does not belong to the selected crop."],
        },
    },
)
