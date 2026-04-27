from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_LOCATION_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Location",
    description=(
        "Example paginated response containing a list of " "planting locations."
    ),
    value={
        "id": 1,
        "name": "Backyard Garden Bed",
        "location_type": "GROUND",
        "height": None,
        "width": "120.00",
        "length": "5.00",
        "is_occupied": False,
    },
)

CREATE_PLANTING_LOCATION_REQUEST_GROUND_EXAMPLE = OpenApiExample(
    name="Create ground planting location payload",
    summary="Create a ground planting location",
    description=(
        "Example request payload for creating a ground planting "
        "location. Length is required for ground locations, while "
        "height is not applicable."
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
        "Example request payload for creating a pot-based "
        "planting location. Height is required for pot locations, "
        "length is not applicable."
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
    description=(
        "Example response returned after a ground planting "
        "location is successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "5.00",
            "is_occupied": False,
        },
        "message": None,
    },
)

CREATE_POT_PLANTING_LOCATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Pot planting location created example",
    summary="Successfully created pot planting location",
    description=(
        "Example response returned after a pot or nursery pot "
        "planting location is successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 2,
            "name": "Balcony Pot",
            "location_type": "POT",
            "height": "30.00",
            "width": "25.00",
            "length": None,
            "is_occupied": False,
        },
        "message": None,
    },
)

PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE = (
    OpenApiExample(
        name="Missing height for pot location",
        summary="Height required for pot or nursery pot",
        description=(
            "Example response returned when a pot or nursery pot "
            "planting location is created or updated without "
            "providing the required height field."
        ),
        status_codes=["400"],
        value={
            "status": "error",
            "data": None,
            "message": {
                "height": [
                    "Height is required for pot or nursery pot locations."
                ]
            },
        },
    )
)

PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE = (
    OpenApiExample(
        name="Missing length for ground location",
        summary="Length required for ground location",
        description=(
            "Example response returned when a ground planting "
            "location is created or updated without providing "
            "the required length field."
        ),
        status_codes=["400"],
        value={
            "status": "error",
            "data": None,
            "message": {"length": ["Length is required for ground locations."]},
        },
    )
)

PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "Example response returned when required fields are "
        "missing in the request payload for creating a "
        "planting location."
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
    description=(
        "Example response returning planting location details "
        "for the specified ID."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "5.00",
            "is_occupied": False,
        },
        "message": None,
    },
)

PLANTING_LOCATION_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location not found",
    summary="No planting location exists with the provided ID.",
    description=(
        "Example response returned when no planting location "
        "exists for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)

UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Update planting location payload",
    summary="Update a planting location",
    description=(
        "Example request payload for updating planting location "
        "dimensions and type."
    ),
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
    description=(
        "Example response indicating the planting location "
        "details were successfully updated."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "name": "Backyard Garden Bed",
            "location_type": "GROUND",
            "height": None,
            "width": "120.00",
            "length": "10.00",
            "is_occupied": False,
        },
        "message": None,
    },
)

PARTIAL_UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Partially update planting location payload",
    summary="Partially update a planting location",
    description=(
        "Example request payload for partially updating a " "planting location."
    ),
    value={
        "length": "10.00",
    },
    request_only=True,
)

GROUND_LOCATION_HEIGHT_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name="Invalid height for ground location",
    summary="Height provided for ground location",
    description=(
        "Example response returned when a height is provided "
        "for a planting location with a type of 'GROUND'."
    ),
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
    description=(
        "Example response returned when a height is provided "
        "for a planting location with a type of 'POT'."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "length": ["Length must not be provided for ground locations."]
        },
    },
)

PLANTING_LOCATION_UPLOAD_IMAGE_REQUEST_EXAMPLE = OpenApiExample(
    name="Image Upload",
    summary="Upload or update the site photo",
    media_type="multipart/form-data",
    description=(
        "Example request payload for updating the planting "
        "location image. This request requires "
        "**multipart/form-data** encoding. "
        "Supported formats: **JPG, PNG**. "
        "Maximum file size: **2MB**."
    ),
    value={
        "image": "planting_location.png",
    },
    request_only=True,
)

PLANTING_LOCATION_UPLOAD_IMAGE_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting location image uploaded",
    summary="Planting location image uploaded successfully",
    description=(
        "Example response returned when the planting location "
        "image is successfully uploaded and updated."
    ),
    value={
        "status": "success",
        "data": {
            "image": (
                "http://api.example.com/media/"
                "planting_locations/planting_location.png"
            )
        },
        "message": None,
    },
)
