from drf_spectacular.utils import OpenApiResponse

from ...serializers import PlantingLocationSerializer
from ..shared.examples import (
    NO_DATA_RESPONSE_EXAMPLE,
    UPLOAD_IMAGE_TOO_LARGE_ERROR_EXAMPLE,
    UPLOAD_IMAGE_UNSUPPORTED_EXTENSION_ERROR_EXAMPLE,
    UPLOAD_INVALID_IMAGE_VALIDATION_ERROR_EXAMPLE,
)
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (
    CREATE_GROUND_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    CREATE_POT_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    GROUND_LOCATION_HEIGHT_VALIDATION_ERROR_EXAMPLE,
    PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_NOT_FOUND_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE,
    PLANTING_LOCATION_UPLOAD_IMAGE_RESPONSE_EXAMPLE,
    POT_LOCATION_LENGTH_VALIDATION_ERROR_EXAMPLE,
    RETRIEVE_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    UPDATE_PLANTING_LOCATION_RESPONSE_EXAMPLE,
)
from .schemas import (
    PLANTING_LOCATION_RESPONSE_DATA_SCHEMA,
    PLANTING_LOCATION_UPLOADED_IMAGE_RESPONSE_DATA_SCHEMA,
)

PLANTING_LOCATION_LIST_RESPONSE = OpenApiResponse(
    description=(
        "Paginated list of planting locations belonging to "
        "the authenticated user."
    ),
    response=PlantingLocationSerializer,
)

PLANTING_LOCATION_CREATED_RESPONSE = OpenApiResponse(
    description="Planting location created successfully.",
    response=PLANTING_LOCATION_RESPONSE_DATA_SCHEMA,
    examples=[
        CREATE_GROUND_PLANTING_LOCATION_RESPONSE_EXAMPLE,
        CREATE_POT_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    ],
)

PLANTING_LOCATION_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
        PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    ],
)

PLANTING_LOCATION_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Planting location retrieved successfully.",
    response=PLANTING_LOCATION_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_PLANTING_LOCATION_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested planting location does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_LOCATION_NOT_FOUND_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_UPDATE_RESPONSE = OpenApiResponse(
    description="Planting location updated successfully.",
    response=PLANTING_LOCATION_RESPONSE_DATA_SCHEMA,
    examples=[
        UPDATE_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    ],
)

PLANTING_LOCATION_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
        PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    ],
)

PLANTING_LOCATION_PARTIAL_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        GROUND_LOCATION_HEIGHT_VALIDATION_ERROR_EXAMPLE,
        POT_LOCATION_LENGTH_VALIDATION_ERROR_EXAMPLE,
    ],
)

PLANTING_LOCATION_DELETE_RESPONSE = OpenApiResponse(
    description="Planting location deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_IMAGE_UPLOADED_RESPONSE = OpenApiResponse(
    description="Planting location image uploaded successfully.",
    response=PLANTING_LOCATION_UPLOADED_IMAGE_RESPONSE_DATA_SCHEMA,
    examples=[PLANTING_LOCATION_UPLOAD_IMAGE_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_IMAGE_UPLOAD_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        UPLOAD_INVALID_IMAGE_VALIDATION_ERROR_EXAMPLE,
        UPLOAD_IMAGE_UNSUPPORTED_EXTENSION_ERROR_EXAMPLE,
        UPLOAD_IMAGE_TOO_LARGE_ERROR_EXAMPLE,
    ],
)
