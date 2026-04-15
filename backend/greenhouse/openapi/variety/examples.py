from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

VARIETY_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Variety",
    summary="Variety serializer example",
    description=(
        "Example paginated response containing a list of varieties."
    ),
    value={
        "id": 1,
        "name": "Sun Gold",
        "crop": 1,
        "growth_habit": ["INDETERMINATE"],
    },
)

CREATE_VARIETY_REQUEST_EXAMPLE = OpenApiExample(
    name="Create variety payload",
    summary="Create a variety",
    description="Example request payload for creating a variety.",
    value={
        "name": "Sun Gold",
        "crop": 1,
        "growth_habit": ["INDETERMINATE"],
    },
    request_only=True,
)

UPDATE_VARIETY_REQUEST_EXAMPLE = OpenApiExample(
    name="Update variety payload",
    summary="Update a variety",
    description="Example request payload for updating a variety.",
    value={
        "name": "Sun Gold",
        "crop": 1,
        "growth_habit": ["DETERMINATE", "INDETERMINATE"],
    },
    request_only=True,
)

PARTIAL_UPDATE_VARIETY_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update variety payload",
    summary="Partially update a variety",
    description=(
        "Example request payload for partially updating a variety."
    ),
    value={
        "growth_habit": ["DETERMINATE"],
    },
    request_only=True,
)

CREATE_VARIETY_RESPONSE_EXAMPLE = OpenApiExample(
    name="Variety created example",
    summary="Successfully created variety",
    description=(
        "Example response returned after a variety is "
        "successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Sun Gold",
            "crop": 1,
            "growth_habit": ["INDETERMINATE"],
        },
        "message": None,
    },
)

RETRIEVE_VARIETY_RESPONSE_EXAMPLE = OpenApiExample(
    name="Variety detail",
    summary="Retrieve a variety by ID",
    description=(
        "Example response returning variety details for the "
        "specified ID."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Sun Gold",
            "crop": 1,
            "growth_habit": ["INDETERMINATE"],
        },
        "message": None,
    },
)

UPDATE_VARIETY_RESPONSE_EXAMPLE = OpenApiExample(
    name="Variety updated",
    summary="Variety updated successfully",
    description=(
        "Example response indicating the variety was "
        "successfully updated."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Sun Gold",
            "crop": 1,
            "growth_habit": ["DETERMINATE", "INDETERMINATE"],
        },
        "message": None,
    },
)

VARIETY_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Variety not found",
    summary="No variety exists with the provided ID.",
    description=(
        "Example response returned when no variety exists "
        "for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

VARIETY_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
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
            "name": ["This field is required."],
            "crop": ["This field is required."],
        },
    },
)
