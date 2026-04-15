from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

CROP_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Crop",
    summary="Crop serializer example",
    description=(
        "Example paginated response containing a list of crops."
    ),
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
    description=(
        "Example response returning crop details for the "
        "specified ID."
    ),
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
    description=(
        "Example response returned when no crop exists "
        "for the specified ID."
    ),
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
    description=(
        "Example request payload for partially updating a crop."
    ),
    value={
        "min_days_to_harvest": 70,
    },
    request_only=True,
)

CROP_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
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
            "scientific_name": ["This field is required."],
        },
    },
)

MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE = (
    OpenApiExample(
        name="Invalid harvest days range",
        summary="Invalid min/max days to harvest",
        description=(
            "Example response returned when the minimum days to "
            "harvest is greater than the maximum days to harvest."
        ),
        status_codes=["400"],
        value={
            "status": "error",
            "data": None,
            "message": {
                "min_days_to_harvest": [
                    "Cannot be greater than max_days_to_harvest."
                ],
                "max_days_to_harvest": [
                    "Cannot be less than min_days_to_harvest."
                ],
            },
        },
    )
)

CREATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop created example",
    summary="Successfully created crop",
    description=(
        "Example response returned after a crop is "
        "successfully created."
    ),
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
    description=(
        "Example response returned when a duplicate record "
        "already exists."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "non_field_errors": [
                "A crop with the same name and scientific name "
                "already exists."
            ]
        },
    },
)

UPDATE_CROP_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop Updated",
    summary="Crop updated successfully",
    description=(
        "Example response indicating the crop was "
        "successfully updated."
    ),
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

CROP_UPLOAD_IMAGE_REQUEST_EXAMPLE = OpenApiExample(
    name="Image Upload",
    summary="Upload or update the crop photo",
    media_type="multipart/form-data",
    description=(
        "Example request payload for updating the crop image. "
        "This request requires **multipart/form-data** encoding. "
        "Supported formats: **JPG, PNG**. Maximum file size: **2MB**."
    ),
    value={
        "image": "crop.png",
    },
    request_only=True,
)

CROP_UPLOAD_IMAGE_RESPONSE_EXAMPLE = OpenApiExample(
    name="Crop image uploaded",
    summary="Crop image uploaded successfully",
    description=(
        "Example response returned when the crop image is "
        "successfully uploaded and updated."
    ),
    value={
        "status": "success",
        "data": {
            "image": "http://api.example.com/media/crops/crop.png"
        },
        "message": None,
    },
)
