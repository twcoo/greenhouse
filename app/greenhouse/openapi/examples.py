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
    description="Represents a crop object returned by the API.",
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
    description="Returns the details of a crop identified by the provided ID.",
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

CREATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Create tomato crop payload",
    summary="Create a tomato crop",
    description="Example request payload for creating a tomato crop.",
    value={
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL_SUN",
        "min_days_to_harvest": 60,
        "max_days_to_harvest": 90,
    },
    request_only=True,
)

UPDATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Update tomato crop payload",
    summary="Update a tomato crop",
    description="Example request payload for update a tomato crop.",
    value={
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL_SUN",
        "min_days_to_harvest": 70,
        "max_days_to_harvest": 90,
    },
    request_only=True,
)

CROP_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "This response is returned when one or more required fields are missing "
        "in the request payload."
    ),
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
    description="This response is returned when a duplicate record already exists.",
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
    description="Returned after the crop has been successfully updated.",
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

CROP_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop not found",
    summary="No crop exists with the provided ID.",
    description="Returned when a crop with the specified ID does not exist.",
    value=RESOURCE_NOT_FOUND_RESPONSE,
)
