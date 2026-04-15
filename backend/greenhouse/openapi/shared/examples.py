from typing import Optional

from drf_spectacular.utils import OpenApiExample

RESOURCE_NOT_FOUND_RESPONSE: dict[str, Optional[str]] = {
    "status": "error",
    "data": None,
    "message": "Resource not found.",
}

NO_DATA_RESPONSE_EXAMPLE = OpenApiExample(
    name="No data response",
    summary="Successful response with no data",
    description=(
        "Example response returned when a request completes "
        "successfully but does not include any data in the "
        "response body."
    ),
    value={
        "status": "success",
        "data": None,
        "message": None,
    },
)

UPLOAD_INVALID_IMAGE_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name="Invalid image upload",
    summary="Invalid or corrupted image file",
    description=(
        "Example response returned when the uploaded file "
        "is not a valid image."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {
            "image": [
                "Upload a valid image. The file you uploaded "
                "was either not an image or a corrupted image."
            ]
        },
    },
)

UPLOAD_IMAGE_TOO_LARGE_ERROR_EXAMPLE = OpenApiExample(
    name="Image file too large",
    summary="Uploaded image exceeds maximum file size",
    description=(
        "Example response returned when the uploaded image "
        "exceeds the maximum allowed file size of 2MB."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {
            "image": ["File too large. Size should not exceed 2.0MB."]
        },
    },
)

UPLOAD_IMAGE_UNSUPPORTED_EXTENSION_ERROR_EXAMPLE = OpenApiExample(
    name="Unsupported image file extension",
    summary="Invalid image file type",
    description=(
        "Example response returned when the uploaded image has "
        "an unsupported file extension. Only .jpg and .png files "
        "are allowed."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {
            "image": [
                "Unsupported file extension. "
                "Please upload a .jpg or .png image."
            ]
        },
    },
)
