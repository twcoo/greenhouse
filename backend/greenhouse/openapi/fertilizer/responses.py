from drf_spectacular.utils import OpenApiResponse

from ...serializers import FertilizerSerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_FERTILIZER_RESPONSE_EXAMPLE,
                       FERTILIZER_INVALID_TYPE_EXAMPLE,
                       FERTILIZER_NOT_FOUND_RESPONSE_EXAMPLE,
                       FERTILIZER_REQUIRED_FIELDS_EXAMPLE,
                       RETRIEVE_FERTILIZER_RESPONSE_EXAMPLE,
                       UPDATE_FERTILIZER_RESPONSE_EXAMPLE)
from .schemas import FERTILIZER_RESPONSE_DATA_SCHEMA

FERTILIZER_LIST_RESPONSE = OpenApiResponse(
    description=(
        "Paginated list of fertilizers belonging to the authenticated user."
    ),
    response=FertilizerSerializer,
)

FERTILIZER_CREATED_RESPONSE = OpenApiResponse(
    description="Fertilizer created successfully.",
    response=FERTILIZER_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_FERTILIZER_RESPONSE_EXAMPLE],
)

FERTILIZER_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        FERTILIZER_REQUIRED_FIELDS_EXAMPLE,
        FERTILIZER_INVALID_TYPE_EXAMPLE,
    ],
)

FERTILIZER_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Fertilizer retrieved successfully.",
    response=FERTILIZER_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_FERTILIZER_RESPONSE_EXAMPLE],
)

FERTILIZER_UPDATE_RESPONSE = OpenApiResponse(
    description="Fertilizer updated successfully.",
    response=FERTILIZER_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_FERTILIZER_RESPONSE_EXAMPLE],
)

FERTILIZER_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        FERTILIZER_REQUIRED_FIELDS_EXAMPLE,
        FERTILIZER_INVALID_TYPE_EXAMPLE,
    ],
)

FERTILIZER_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_INVALID_TYPE_EXAMPLE],
)

FERTILIZER_DELETE_RESPONSE = OpenApiResponse(
    description="Fertilizer deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

FERTILIZER_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested fertilizer does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_NOT_FOUND_RESPONSE_EXAMPLE],
)
