from drf_spectacular.utils import OpenApiResponse

from ...serializers.planting_daily_observation import \
    PlantingDailyObservationSerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE,
                       PLANTING_DAILY_OBSERVATION_INVALID_CHOICE_EXAMPLE,
                       PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE_EXAMPLE,
                       UPDATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE)
from .schemas import PLANTING_DAILY_OBSERVATION_RESPONSE_DATA_SCHEMA

PLANTING_DAILY_OBSERVATION_LIST_RESPONSE = OpenApiResponse(
    description="List of daily observations for the specified planting.",
    response=PlantingDailyObservationSerializer,
)

PLANTING_DAILY_OBSERVATION_CREATED_RESPONSE = OpenApiResponse(
    description="Daily observation logged successfully.",
    response=PLANTING_DAILY_OBSERVATION_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_DAILY_OBSERVATION_INVALID_CHOICE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_UPDATE_RESPONSE = OpenApiResponse(
    description="Daily observation updated successfully.",
    response=PLANTING_DAILY_OBSERVATION_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_DAILY_OBSERVATION_INVALID_CHOICE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_RESPONSE = OpenApiResponse(
    description="Daily observation partially updated successfully.",
    response=PLANTING_DAILY_OBSERVATION_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_DAILY_OBSERVATION_INVALID_CHOICE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_DELETE_RESPONSE = OpenApiResponse(
    description="Daily observation deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested planting or observation does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE_EXAMPLE],
)
