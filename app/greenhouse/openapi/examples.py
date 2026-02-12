from typing import Optional

from drf_spectacular.utils import OpenApiExample

# Constants
RESOURCE_NOT_FOUND_RESPONSE: dict[str, Optional[str]] = {
    "status": "error",
    "data": None,
    "message": "Resource not found.",
}

NO_DATA_RESPONSE_EXAMPLE = OpenApiExample(
    name="No data response",
    summary="Successful response with no data",
    description=(
        "Example response returned when a request completes successfully "
        "but does not include any data in the response body."
    ),
    value={
        "status": "success",
        "data": None,
        "message": None,
    },
)

# Auth
AUTH_REGISTRATION_REQUEST_EXAMPLE = OpenApiExample(
    name="User registration request",
    summary="User registration",
    description="Example request payload for registering a new user account.",
    value={
        "username": "mhillcrest",
        "email": "mhillcrest@example.com",
        "password": "strongPassword$1",
    },
    request_only=True,
)

AUTH_REGISTERED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Successful registration",
    description="Example response returned after successful registration.",
    status_codes=["201"],
    response_only=True,
    value={
        "status": "success",
        "data": {
            "expiry": "2026-01-20T06:46:33.891979Z",
            "token": "ca57a6fb43553fdbe63488748004731714173689eb7.....",
        },
        "message": None,
    },
)

AUTH_REGISTER_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Auth missing required fields",
    description="Example response returned when required fields are missing in the request payload.",
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {
            "username": ["This field is required."],
            "password": ["This field is required."],
        },
    },
)

AUTH_REGISTER_CONFLICT_RESPONSE_EXAMPLE = OpenApiExample(
    name="User is already registered.",
    description="Example response returned when a user attempts to register with a username that already exists.",
    status_codes=["409"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "A user with that username already exists.",
    },
)

# Crop
CROP_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Crop",
    summary="Crop serializer example",
    description="Example paginated response containing a list of crops.",
    value={
        "id": 1,
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL SUN",
        "min_days_to_harvest": 60,
        "max_days_to_harvest": 90,
    },
)


RETRIEVE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop detail",
    summary="Retrieve a crop by ID",
    description="Example response returning crop details for the specified ID.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        },
        "message": None,
    },
)

CROP_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop not found",
    summary="No crop exists with the provided ID.",
    description="Example response returned when no crop exists for the specified ID.",
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

CREATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Create crop payload",
    summary="Create a crop",
    description="Example request payload for creating a crop.",
    value={
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL SUN",
        "min_days_to_harvest": 60,
        "max_days_to_harvest": 90,
    },
    request_only=True,
)

UPDATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Update crop payload",
    summary="Update a crop",
    description="Example request payload for updating a crop.",
    value={
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL SUN",
        "min_days_to_harvest": 70,
        "max_days_to_harvest": 90,
    },
    request_only=True,
)

PARTIAL_UPDATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update crop payload",
    summary="Partially update a crop",
    description="Example request payload for partially updating a crop.",
    value={
        "min_days_to_harvest": 70,
    },
    request_only=True,
)

CROP_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description="Example response returned when required fields are missing in the request payload.",
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "name": ["This field is required."],
            "scientific_name": ["This field is required."],
        },
    },
)


MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Invalid harvest days range",
    summary="Invalid min/max days to harvest",
    description=(
        "Example response returned when the minimum days to harvest "
        "is greater than the maximum days to harvest."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "min_days_to_harvest": [
                "Cannot be greater than max_days_to_harvest."
            ],
            "max_days_to_harvest": ["Cannot be less than min_days_to_harvest."],
        },
    },
)


CREATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop created example",
    summary="Successfully created crop",
    description="Example response returned after a crop is successfully created.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        },
        "message": None,
    },
)

DUPLICATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Duplicate crop record",
    summary="Crop already exists",
    description="Example response returned when a duplicate record already exists.",
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "non_field_errors": [
                "A crop with the same name and scientific name already exists."
            ]
        },
    },
)


UPDATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop Updated",
    summary="Crop updated successfully",
    description="Example response indicating the crop was successfully updated.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 70,
            "max_days_to_harvest": 90,
        },
        "message": None,
    },
)
