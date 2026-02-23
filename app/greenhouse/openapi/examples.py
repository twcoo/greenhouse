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

AUTH_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
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
    name="User is already registered",
    description="Example response returned when a user attempts to register with a username that already exists.",
    status_codes=["409"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "A user with that username already exists.",
    },
)

AUTH_LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    name="User login request",
    description="Example request payload for user login.",
    value={
        "username": "mhillcrest",
        "password": "strongPassword$1",
    },
    request_only=True,
)

AUTH_LOGIN_RESPONSE_EXAMPLE = OpenApiExample(
    name="Successful login",
    description="Example response returned after successful login.",
    status_codes=["200"],
    response_only=True,
    value={
        "status": "success",
        "data": {
            "expiry": "2026-01-20T07:21:39.160819Z",
            "token": "ab57a6fb43553fdbe63488748004731714173689eb7.....",
        },
        "message": None,
    },
)

AUTH_LOGIN_UNAUTHORIZED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Invalid provided credentials",
    description="Example response returned when logging in with invalid credentials.",
    status_codes=["401"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "Unable to log in with provided credentials.",
    },
)

AUTH_LOGOUT_RESPONSE_EXAMPLE = OpenApiExample(
    name="Successful logout",
    description="Example response returned after successful logout.",
    status_codes=["200"],
    response_only=True,
    value={
        "status": "success",
        "data": None,
        "message": "Logged out successfully.",
    },
)

AUTH_LOGOUT_UNAUTHORIZED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Invalid provided token",
    description="Example response returned when attempting to log out with an invalid or expired authentication token.",
    status_codes=["401"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "Invalid token.",
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

# Planting Location
PLANTING_LOCATION_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Location",
    description="Example paginated response containing a list of planting locations.",
    value={
        "id": 1,
        "name": "Backyard Garden Bed",
        "location_type": "GROUND",
        "height": None,
        "width": "120.00",
        "length": "5.00",
    },
)

CREATE_PLANTING_LOCATION_REQUEST_GROUND_EXAMPLE = OpenApiExample(
    name="Create ground planting location payload",
    summary="Create a ground planting location",
    description=(
        "Example request payload for creating a ground planting location. "
        "Length is required for ground locations, while height is not applicable."
    ),
    value={
        "name": "Backyard Garden Bed",
        "location_type": "GROUND",
        "width": "120.00",
        "length": "5.00",
    },
    request_only=True,
)

CREATE_PLANTING_LOCATION_REQUEST_POT_EXAMPLE = OpenApiExample(
    name="Create pot planting location payload",
    summary="Create a pot or nursery pot planting location",
    description=(
        "Example request payload for creating a pot-based planting location. "
        "Height is required for pot locations, length is not applicable."
    ),
    value={
        "name": "Balcony Pot",
        "location_type": "POT",
        "height": "30.00",
        "width": "25.00",
    },
    request_only=True,
)

CREATE_GROUND_PLANTING_LOCATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Ground planting location created example",
    summary="Successfully created ground planting location",
    description="Example response returned after a ground planting location is successfully created.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "5.00",
        },
        "message": None,
    },
)

CREATE_POT_PLANTING_LOCATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Pot planting location created example",
    summary="Successfully created pot planting location",
    description="Example response returned after a pot or nursery pot planting location is successfully created.",
    value={
        "status": "success",
        "data": {
            "id": 2,
            "name": "Balcony Pot",
            "location_type": "POT",
            "height": "30.00",
            "width": "25.00",
            "length": None,
        },
        "message": None,
    },
)

PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Missing height for pot location",
    summary="Height required for pot or nursery pot",
    description=(
        "Example response returned when a pot or nursery pot planting location "
        "is created or updated without providing the required height field."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "height": ["Height is required for pot or nursery pot locations."]
        },
    },
)

PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Missing length for ground location",
    summary="Length required for ground location",
    description=(
        "Example response returned when a ground planting location is created  or updated "
        "without providing the required length field."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {"length": ["Length is required for ground locations."]},
    },
)

PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "Example response returned when required fields are missing "
        "in the request payload for creating a planting location."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "name": ["This field is required."],
            "location_type": ["This field is required."],
            "width": ["This field is required."],
        },
    },
)


RETRIEVE_PLANTING_LOCATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location detail",
    summary="Retrieve a planting location by ID",
    description="Example response returning planting location details for the specified ID.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "5.00",
        },
        "message": None,
    },
)

PLANTING_LOCATION_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location not found",
    summary="No planting location exists with the provided ID.",
    description="Example response returned when no planting location exists for the specified ID.",
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Update planting location payload",
    summary="Update a planting location",
    description="Example request payload for updating planting location dimensions and type.",
    value={
        "name": "Backyard Garden Bed",
        "location_type": "GROUND",
        "height": None,
        "width": "120.00",
        "length": "10.00",
    },
    request_only=True,
)

UPDATE_PLANTING_LOCATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location updated",
    summary="Planting location updated successfully",
    description="Example response indicating the planting location details were successfully updated.",
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "10.00",
        },
        "message": None,
    },
)

PARTIAL_UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update planting location payload",
    summary="Partially update a planting location",
    description="Example request payload for partially updating a planting location.",
    value={
        "length": "10.00",
    },
    request_only=True,
)

GROUND_LOCATION_HEIGHT_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name="Invalid height for ground location",
    summary="Height provided for ground location",
    description="Example response returned when a height is provided for a planting location with a type of 'GROUND'.",
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "height": ["Height must not be provided for ground locations."]
        },
    },
)

POT_LOCATION_LENGTH_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name="Invalid length for pot location",
    summary="Length provided for pot location",
    description="Example response returned when a height is provided for a planting location with a type of 'POT'.",
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "length": ["Length must not be provided for ground locations."]
        },
    },
)
