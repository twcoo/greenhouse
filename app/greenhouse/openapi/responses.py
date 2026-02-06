from typing import Optional

from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from ..schemas import CustomOpenAPIResponseSchema
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
