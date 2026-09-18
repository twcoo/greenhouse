from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

FERTILIZER_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Fertilizer",
    summary="Fertilizer serializer example",
    description="Example paginated response containing a list of fertilizers.",
    value={
        "id": 1,
        "name": "Swamp Fertilizer #1",
        "type": "SWAMP",
        "status": "BREWING",
        "start_date": "2024-01-01",
        "ingredients": ["banana peels", "molasses"],
        "notes": "Fermenting in the barrel.",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    },
)

CREATE_FERTILIZER_REQUEST_EXAMPLE = OpenApiExample(
    name="Create fertilizer payload",
    summary="Create a fertilizer",
    description="Example request payload for creating a fertilizer.",
    value={
        "name": "Swamp Fertilizer #1",
        "type": "SWAMP",
        "status": "BREWING",
        "start_date": "2024-01-01",
        "ingredients": ["banana peels", "molasses"],
        "notes": "Fermenting in the barrel.",
    },
    request_only=True,
)

UPDATE_FERTILIZER_REQUEST_EXAMPLE = OpenApiExample(
    name="Update fertilizer payload",
    summary="Update a fertilizer",
    description="Example request payload for updating a fertilizer.",
    value={
        "name": "Swamp Fertilizer #1",
        "type": "SWAMP",
        "status": "READY",
        "start_date": "2024-01-01",
        "ingredients": ["banana peels", "molasses", "egg shells"],
        "notes": "Ready to use.",
    },
    request_only=True,
)

PARTIAL_UPDATE_FERTILIZER_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update fertilizer payload",
    summary="Partially update a fertilizer",
    description="Example request payload for partially updating a fertilizer.",
    value={"status": "READY"},
    request_only=True,
)

CREATE_FERTILIZER_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer created example",
    summary="Successfully created fertilizer",
    description=(
        "Example response returned after a fertilizer is "
        "successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Swamp Fertilizer #1",
            "type": "SWAMP",
            "status": "BREWING",
            "start_date": "2024-01-01",
            "ingredients": ["banana peels", "molasses"],
            "notes": "Fermenting in the barrel.",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
        "message": None,
    },
)

RETRIEVE_FERTILIZER_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer detail",
    summary="Retrieve a fertilizer by ID",
    description="Example response returning fertilizer details for the specified ID.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Swamp Fertilizer #1",
            "type": "SWAMP",
            "status": "BREWING",
            "start_date": "2024-01-01",
            "ingredients": ["banana peels", "molasses"],
            "notes": "Fermenting in the barrel.",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
        "message": None,
    },
)

UPDATE_FERTILIZER_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer updated",
    summary="Fertilizer updated successfully",
    description="Example response indicating the fertilizer was successfully updated.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Swamp Fertilizer #1",
            "type": "SWAMP",
            "status": "READY",
            "start_date": "2024-01-01",
            "ingredients": ["banana peels", "molasses", "egg shells"],
            "notes": "Ready to use.",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        },
        "message": None,
    },
)

FERTILIZER_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer not found",
    summary="No fertilizer exists with the provided ID.",
    description=(
        "Example response returned when no fertilizer exists "
        "for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

FERTILIZER_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
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
        },
    },
)

FERTILIZER_INVALID_TYPE_EXAMPLE = OpenApiExample(
    name="Invalid fertilizer type value",
    summary="Invalid fertilizer type choice",
    description=(
        "Example response returned when an unrecognised value "
        "is provided for type."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "type": ['"UNKNOWN" is not a valid choice.'],
        },
    },
)
