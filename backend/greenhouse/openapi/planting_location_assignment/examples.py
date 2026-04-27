from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_LOCATION_ASSIGNMENT_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Location Assignment",
    summary="Planting location assignment serializer example",
    description="Example response containing a planting location assignment.",
    value={
        "id": 1,
        "planting_location": 1,
        "planting_location_name": "Greenhouse Bed A",
        "start_date": "2024-03-01",
        "end_date": None,
        "created_at": "2024-03-01T00:00:00Z",
        "updated_at": "2024-03-01T00:00:00Z",
    },
)

CREATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE = OpenApiExample(
    name="Create planting location assignment payload",
    summary="Create a planting location assignment",
    description=(
        "Example request payload for assigning a planting to a location."
    ),
    value={"planting_location": 1, "start_date": "2024-03-01"},
    request_only=True,
)

UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE = OpenApiExample(
    name="Update planting location assignment payload",
    summary="Update a planting location assignment",
    description=(
        "Example request payload for updating a planting location assignment."
    ),
    value={
        "planting_location": 2,
        "start_date": "2024-03-01",
        "end_date": "2024-06-01",
    },
    request_only=True,
)

PARTIAL_UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update planting location assignment payload",
    summary="Partially update a planting location assignment",
    description=(
        "Example request payload for partially updating a "
        "planting location assignment."
    ),
    value={"end_date": "2024-06-01"},
    request_only=True,
)

CREATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location assignment created",
    summary="Successfully created planting location assignment",
    description=(
        "Example response returned after a planting location assignment "
        "is successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "planting_location": 1,
            "planting_location_name": "Greenhouse Bed A",
            "start_date": "2024-03-01",
            "end_date": None,
            "created_at": "2024-03-01T00:00:00Z",
            "updated_at": "2024-03-01T00:00:00Z",
        },
        "message": None,
    },
)

RETRIEVE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location assignment detail",
    summary="Retrieve a planting location assignment by ID",
    description=(
        "Example response returning planting location assignment details."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "planting_location": 1,
            "planting_location_name": "Greenhouse Bed A",
            "start_date": "2024-03-01",
            "end_date": None,
            "created_at": "2024-03-01T00:00:00Z",
            "updated_at": "2024-03-01T00:00:00Z",
        },
        "message": None,
    },
)

UPDATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location assignment updated",
    summary="Planting location assignment updated successfully",
    description=(
        "Example response indicating the planting location assignment "
        "was successfully updated."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "planting_location": 2,
            "planting_location_name": "Outdoor Bed B",
            "start_date": "2024-03-01",
            "end_date": "2024-06-01",
            "created_at": "2024-03-01T00:00:00Z",
            "updated_at": "2024-06-01T00:00:00Z",
        },
        "message": None,
    },
)

PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location assignment not found",
    summary="No assignment exists with the provided ID.",
    description=(
        "Example response returned when no planting location assignment "
        "exists for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

PLANTING_LOCATION_ASSIGNMENT_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
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
            "planting_location": ["This field is required."],
            "start_date": ["This field is required."],
        },
    },
)

PLANTING_LOCATION_ASSIGNMENT_DATE_ORDER_EXAMPLE = OpenApiExample(
    name="End date before start date",
    summary="Invalid date range",
    description=(
        "Example response returned when end_date is earlier than start_date."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "end_date": ["End date must be on or after start date."],
        },
    },
)

PLANTING_LOCATION_ASSIGNMENT_OVERLAP_EXAMPLE = OpenApiExample(
    name="Overlapping assignment",
    summary="Date range overlaps existing assignment",
    description=(
        "Example response returned when the given date range overlaps "
        "with an existing planting location assignment."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "start_date": [
                "This planting already has a location assignment "
                "that overlaps with the given date range."
            ],
        },
    },
)

PLANTING_LOCATION_ASSIGNMENT_LOCATION_OCCUPIED_EXAMPLE = OpenApiExample(
    name="Location already occupied",
    summary="Pot or nursery pot is occupied by another planting",
    description=(
        "Example response returned when attempting to assign a planting "
        "to a pot or nursery pot location that already has an active "
        "planting for the given date range."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "planting_location": [
                "This location already has an active planting "
                "for the given date range."
            ],
        },
    },
)
