from drf_spectacular.utils import OpenApiResponse

from ...serializers import PlantingSerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_PLANTING_RESPONSE_EXAMPLE,
                       PLANTING_NOT_FOUND_RESPONSE_EXAMPLE,
                       PLANTING_REQUIRED_FIELDS_EXAMPLE,
                       PLANTING_VARIETY_CROP_MISMATCH_EXAMPLE,
                       RETRIEVE_PLANTING_RESPONSE_EXAMPLE,
                       UPDATE_PLANTING_RESPONSE_EXAMPLE)
from .schemas import PLANTING_RESPONSE_DATA_SCHEMA

PLANTING_LIST_RESPONSE = OpenApiResponse(
    description=(
        "Paginated list of plantings belonging to the authenticated user."
    ),
    response=PlantingSerializer,
)

PLANTING_CREATED_RESPONSE = OpenApiResponse(
    description="Planting created successfully.",
    response=PLANTING_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_PLANTING_RESPONSE_EXAMPLE],
)

PLANTING_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_VARIETY_CROP_MISMATCH_EXAMPLE,
    ],
)

PLANTING_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Planting retrieved successfully.",
    response=PLANTING_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_PLANTING_RESPONSE_EXAMPLE],
)

PLANTING_UPDATE_RESPONSE = OpenApiResponse(
    description="Planting updated successfully.",
    response=PLANTING_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_PLANTING_RESPONSE_EXAMPLE],
)

PLANTING_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_VARIETY_CROP_MISMATCH_EXAMPLE,
    ],
)

PLANTING_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_VARIETY_CROP_MISMATCH_EXAMPLE],
)

PLANTING_DELETE_RESPONSE = OpenApiResponse(
    description="Planting deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

PLANTING_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested planting does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_NOT_FOUND_RESPONSE_EXAMPLE],
)
