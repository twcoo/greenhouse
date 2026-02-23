from drf_spectacular.utils import OpenApiResponse

from ..serializers import CropSerializer, PlantingLocationSerializer
from .examples import (
    AUTH_LOGIN_RESPONSE_EXAMPLE, AUTH_LOGIN_UNAUTHORIZED_RESPONSE_EXAMPLE,
    AUTH_LOGOUT_RESPONSE_EXAMPLE, AUTH_LOGOUT_UNAUTHORIZED_RESPONSE_EXAMPLE,
    AUTH_REGISTER_CONFLICT_RESPONSE_EXAMPLE, AUTH_REGISTERED_RESPONSE_EXAMPLE,
    AUTH_VALIDATION_RESPONSE_EXAMPLE, CREATE_CROP_RESPONSE_EXAMPLE,
    CREATE_GROUND_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    CREATE_POT_PLANTING_LOCATION_RESPONSE_EXAMPLE,
    CROP_NOT_FOUND_RESPONSE_EXAMPLE, CROP_REQUIRED_FIELDS_EXAMPLE,
    DUPLICATE_CROP_RESPONSE_EXAMPLE,
    GROUND_LOCATION_HEIGHT_VALIDATION_ERROR_EXAMPLE,
    MIN_AND_MAX_DAYS_HARVEST_VALIDATION_RESPONSE_EXAMPLE,
    NO_DATA_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_GROUND_LENGTH_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_NOT_FOUND_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_POT_HEIGHT_REQUIRED_VALIDATION_RESPONSE_EXAMPLE,
    PLANTING_LOCATION_REQUIRED_FIELDS_EXAMPLE,
    POT_LOCATION_LENGTH_VALIDATION_ERROR_EXAMPLE,
    RETRIEVE_CROP_RESPONSE_EXAMPLE,
    RETRIEVE_PLANTING_LOCATION_RESPONSE_EXAMPLE, UPDATE_CROP_RESPONSE_EXAMPLE,
    UPDATE_PLANTING_LOCATION_RESPONSE_EXAMPLE)
from .schemas import (AUTH_RESPONSE_DATA_SCHEMA, CROP_RESPONSE_DATA_SCHEMA,
                      PLANTING_LOCATION_RESPONSE_DATA_SCHEMA,
                      CustomOpenAPIResponseSchema)

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
        AUTH_LOGIN_UNAUTHORIZED_RESPONSE_EXAMPLE,
    ],
)

AUTH_LOGOUT_RESPONSE = OpenApiResponse(
    description="Logout completed successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        AUTH_LOGOUT_RESPONSE_EXAMPLE,
    ],
)

AUTH_LOGOUT_UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Unauthorized access.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[AUTH_LOGOUT_UNAUTHORIZED_RESPONSE_EXAMPLE],
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

# Planting Location
PLANTING_LOCATION_LIST_RESPONSE = OpenApiResponse(
    description="Paginated list of planting locations belonging to the authenticated user.",
    response=PlantingLocationSerializer,
)

PLANTING_LOCATION_CREATED_RESPONSE = OpenApiResponse(
    description="Plating location created successfully.",
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
