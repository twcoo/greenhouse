from drf_spectacular.utils import OpenApiResponse

from ...serializers import FertilizerLogSerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_FERTILIZER_LOG_RESPONSE_EXAMPLE,
                       FERTILIZER_LOG_INVALID_CHOICE_EXAMPLE,
                       FERTILIZER_LOG_NOT_FOUND_RESPONSE_EXAMPLE,
                       UPDATE_FERTILIZER_LOG_RESPONSE_EXAMPLE)
from .schemas import FERTILIZER_LOG_RESPONSE_DATA_SCHEMA

FERTILIZER_LOG_LIST_RESPONSE = OpenApiResponse(
    description="List of log entries for the specified fertilizer.",
    response=FertilizerLogSerializer,
)

FERTILIZER_LOG_CREATED_RESPONSE = OpenApiResponse(
    description="Fertilizer log entry created successfully.",
    response=FERTILIZER_LOG_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_FERTILIZER_LOG_RESPONSE_EXAMPLE],
)

FERTILIZER_LOG_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_LOG_INVALID_CHOICE_EXAMPLE],
)

FERTILIZER_LOG_UPDATE_RESPONSE = OpenApiResponse(
    description="Fertilizer log entry updated successfully.",
    response=FERTILIZER_LOG_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_FERTILIZER_LOG_RESPONSE_EXAMPLE],
)

FERTILIZER_LOG_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_LOG_INVALID_CHOICE_EXAMPLE],
)

FERTILIZER_LOG_PARTIAL_UPDATE_RESPONSE = OpenApiResponse(
    description="Fertilizer log entry partially updated successfully.",
    response=FERTILIZER_LOG_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_FERTILIZER_LOG_RESPONSE_EXAMPLE],
)

FERTILIZER_LOG_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_LOG_INVALID_CHOICE_EXAMPLE],
)

FERTILIZER_LOG_DELETE_RESPONSE = OpenApiResponse(
    description="Fertilizer log entry deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

FERTILIZER_LOG_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested fertilizer or log entry does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[FERTILIZER_LOG_NOT_FOUND_RESPONSE_EXAMPLE],
)
