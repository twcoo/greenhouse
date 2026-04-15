from drf_spectacular.utils import OpenApiResponse

from ...serializers import VarietySerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (
    CREATE_VARIETY_RESPONSE_EXAMPLE,
    RETRIEVE_VARIETY_RESPONSE_EXAMPLE,
    UPDATE_VARIETY_RESPONSE_EXAMPLE,
    VARIETY_NOT_FOUND_RESPONSE_EXAMPLE,
    VARIETY_REQUIRED_FIELDS_EXAMPLE,
)
from .schemas import VARIETY_RESPONSE_DATA_SCHEMA

VARIETY_LIST_RESPONSE = OpenApiResponse(
    description=(
        "Paginated list of varieties belonging to the "
        "authenticated user."
    ),
    response=VarietySerializer,
)

VARIETY_CREATED_RESPONSE = OpenApiResponse(
    description="Variety created successfully.",
    response=VARIETY_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_VARIETY_RESPONSE_EXAMPLE],
)

VARIETY_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[VARIETY_REQUIRED_FIELDS_EXAMPLE],
)

VARIETY_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Variety retrieved successfully.",
    response=VARIETY_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_VARIETY_RESPONSE_EXAMPLE],
)

VARIETY_UPDATE_RESPONSE = OpenApiResponse(
    description="Variety updated successfully.",
    response=VARIETY_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_VARIETY_RESPONSE_EXAMPLE],
)

VARIETY_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[VARIETY_REQUIRED_FIELDS_EXAMPLE],
)

VARIETY_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[],
)

VARIETY_DELETE_RESPONSE = OpenApiResponse(
    description="Variety deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

VARIETY_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested variety does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[VARIETY_NOT_FOUND_RESPONSE_EXAMPLE],
)
