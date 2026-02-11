from drf_spectacular.utils import OpenApiResponse

from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from .examples import (CREATE_CROP_RESPONSE_EXAMPLE,
                       CROP_NOT_FOUND_RESPONSE_EXAMPLE,
                       CROP_REQUIRED_FIELDS_EXAMPLE,
                       DUPLICATE_CROP_RESPONSE_EXAMPLE,
                       MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
                       NO_DATA_RESPONSE_EXAMPLE,
                       RETRIEVE_CROP_RESPONSE_EXAMPLE,
                       UPDATE_CROP_RESPONSE_EXAMPLE)
from .schemas import CROP_RESPONSE_DATA_SCHEMA

CROP_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested crop does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[CROP_NOT_FOUND_RESPONSE_EXAMPLE],
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
        MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
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
        UPDATE_CROP_RESPONSE_EXAMPLE,
    ],
)

CROP_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        CROP_REQUIRED_FIELDS_EXAMPLE,
        MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
    ],
)

CROP_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
    ],
)

CROP_DELETE_RESPONSE = OpenApiResponse(
    description="Crop deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)
