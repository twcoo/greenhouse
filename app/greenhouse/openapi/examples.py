from typing import Optional

from drf_spectacular.utils import OpenApiExample

RESOURCE_NOT_FOUND_RESPONSE: dict[str, Optional[str]] = {
    "status": "error",
    "message": "Resource not found.",
    "data": None,
}


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
        "message": None,
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        },
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


CREATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop created example",
    summary="Successfully created crop",
    description="Example response returned after a crop is successfully created.",
    value={
        "status": "success",
        "message": None,
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 60,
            "max_days_to_harvest": 90,
        },
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
        "message": None,
        "data": {
            "id": 1,
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "VEGETABLE",
            "sunlight_requirement": "FULL SUN",
            "min_days_to_harvest": 70,
            "max_days_to_harvest": 90,
        },
    },
)
