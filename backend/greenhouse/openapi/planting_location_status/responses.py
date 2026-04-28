from drf_spectacular.utils import OpenApiResponse

from ...serializers.planting_location_status import \
    PlantingLocationStatusSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_PLANTING_LOCATION_STATUS_RESPONSE_EXAMPLE,
                       PLANTING_LOCATION_STATUS_INVALID_CHOICE_EXAMPLE,
                       PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE_EXAMPLE,
                       PLANTING_LOCATION_STATUS_REQUIRED_FIELDS_EXAMPLE)
from .schemas import PLANTING_LOCATION_STATUS_RESPONSE_DATA_SCHEMA

PLANTING_LOCATION_STATUS_LIST_RESPONSE = OpenApiResponse(
    description=(
        "List of status history entries for the specified " "planting location."
    ),
    response=PlantingLocationStatusSerializer,
)

PLANTING_LOCATION_STATUS_CREATED_RESPONSE = OpenApiResponse(
    description="Planting location status recorded successfully.",
    response=PLANTING_LOCATION_STATUS_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_PLANTING_LOCATION_STATUS_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_STATUS_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_LOCATION_STATUS_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_LOCATION_STATUS_INVALID_CHOICE_EXAMPLE,
    ],
)

PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested planting location does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE_EXAMPLE],
)
