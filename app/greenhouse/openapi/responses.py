from typing import Optional

from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from .examples import (CREATE_CROP_RESPONSE_EXAMPLE,
                       CROP_REQUIRED_FIELDS_EXAMPLE,
                       DUPLICATE_CROP_RESPONSE_EXAMPLE,
                       RETRIEVE_CROP_RESPONSE_EXAMPLE)
from .schemas import CROP_RESPONSE_DATA_SCHEMA

RESOURCE_NOT_FOUND_RESPONSE: dict[str, Optional[str]] = {
    "status": "error",
    "message": "Resource not found.",
    "data": None,
}

CROP_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested crop does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        OpenApiExample(
            name="Crop not found",
            summary="No crop exists with the provided ID.",
            description="Returned when a crop with the specified ID does not exist.",
            value=RESOURCE_NOT_FOUND_RESPONSE,
        )
    ],
)

CROP_LIST_RESPONSE = OpenApiResponse(
    description="List of crops retrieved successfully.",
    response=CropSerializer,
)

CROP_CREATED_RESPONSE = OpenApiResponse(
    description="Crop created successfully.",
    response=CROP_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_CROP_RESPONSE_EXAMPLE],
)

CROP_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        DUPLICATE_CROP_RESPONSE_EXAMPLE,
        CROP_REQUIRED_FIELDS_EXAMPLE,
    ],
)

CROP_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Crop retrieved successfully.",
    response=CROP_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_CROP_RESPONSE_EXAMPLE],
)


CROP_UPDATE_RESPONSE = OpenApiResponse(
    description="Crop updated successfully.",
    response=CROP_RESPONSE_DATA_SCHEMA,
    examples=[
        OpenApiExample(
            name="Crop Updated",
            summary="Crop updated successfully",
            description="Returned after the crop has been successfully updated.",
            value={
                "status": "success",
                "message": None,
                "data": {
                    "id": 34,
                    "name": "Tomato",
                    "scientific_name": "Solanum lycopersicum",
                    "category": "VEGETABLE",
                    "sunlight_requirement": "FULL SUN",
                    "min_days_to_harvest": 70,
                    "max_days_to_harvest": 90,
                },
            },
        )
    ],
)

CROP_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[CROP_REQUIRED_FIELDS_EXAMPLE],
)

CROP_DELETE_RESPONSE = OpenApiResponse(
    description="Crop deleted successfully. No content is returned.",
)
