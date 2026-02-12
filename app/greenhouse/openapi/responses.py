from drf_spectacular.utils import OpenApiResponse

from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from .examples import (AUTH_LOGIN_RESPONSE_EXAMPLE,
                       AUTH_REGISTER_CONFLICT_RESPONSE_EXAMPLE,
                       AUTH_REGISTERED_RESPONSE_EXAMPLE,
                       AUTH_UNAUTHORIZED_RESPONSE_EXAMPLE,
                       AUTH_VALIDATION_RESPONSE_EXAMPLE,
                       CREATE_CROP_RESPONSE_EXAMPLE,
                       CROP_NOT_FOUND_RESPONSE_EXAMPLE,
                       CROP_REQUIRED_FIELDS_EXAMPLE,
                       DUPLICATE_CROP_RESPONSE_EXAMPLE,
                       MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
                       NO_DATA_RESPONSE_EXAMPLE,
                       RETRIEVE_CROP_RESPONSE_EXAMPLE,
                       UPDATE_CROP_RESPONSE_EXAMPLE)
from .schemas import AUTH_RESPONSE_DATA_SCHEMA, CROP_RESPONSE_DATA_SCHEMA

# Auth
AUTH_REGISTERED_RESPONSE = OpenApiResponse(
    description="Registration completed successfully.",
    response=AUTH_RESPONSE_DATA_SCHEMA,
    examples=[AUTH_REGISTERED_RESPONSE_EXAMPLE],
)

AUTH_REGISTER_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[AUTH_VALIDATION_RESPONSE_EXAMPLE],
)

AUTH_REGISTER_CONFLICT_RESPONSE = OpenApiResponse(
    description="Conflict",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        AUTH_REGISTER_CONFLICT_RESPONSE_EXAMPLE,
    ],
)

AUTH_LOGIN_RESPONSE = OpenApiResponse(
    description="Login completed successfully.",
    response=AUTH_RESPONSE_DATA_SCHEMA,
    examples=[
        AUTH_LOGIN_RESPONSE_EXAMPLE,
    ],
)

AUTH_LOGIN_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[AUTH_VALIDATION_RESPONSE_EXAMPLE],
)

AUTH_LOGIN_UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Unauthorized access.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        AUTH_UNAUTHORIZED_RESPONSE_EXAMPLE,
    ],
)

# Crop
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
