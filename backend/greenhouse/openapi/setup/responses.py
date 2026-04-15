from drf_spectacular.utils import OpenApiResponse

from ..auth.schemas import AUTH_RESPONSE_DATA_SCHEMA
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (
    SETUP_ADMIN_ALREADY_EXISTS_RESPONSE_EXAMPLE,
    SETUP_ADMIN_CREATED_RESPONSE_EXAMPLE,
    SETUP_ADMIN_PASSWORD_MISMATCH_RESPONSE_EXAMPLE,
    SETUP_ADMIN_REQUIRED_FIELDS_VALIDATION_RESPONSE_EXAMPLE,
    SETUP_STATUS_OK_RESPONSE_EXAMPLE,
    SETUP_STATUS_REQUIRED_RESPONSE_EXAMPLE,
)

SETUP_ADMIN_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        SETUP_ADMIN_REQUIRED_FIELDS_VALIDATION_RESPONSE_EXAMPLE,
        SETUP_ADMIN_PASSWORD_MISMATCH_RESPONSE_EXAMPLE,
        SETUP_ADMIN_ALREADY_EXISTS_RESPONSE_EXAMPLE,
    ],
)

SETUP_ADMIN_CREATED_RESPONSE = OpenApiResponse(
    description="Admin setup completed successfully.",
    response=AUTH_RESPONSE_DATA_SCHEMA,
    examples=[SETUP_ADMIN_CREATED_RESPONSE_EXAMPLE],
)

SETUP_STATUS_OK_RESPONSE = OpenApiResponse(
    description=(
        "Successful response indicating that the application "
        "setup status is OK."
    ),
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        SETUP_STATUS_OK_RESPONSE_EXAMPLE,
    ],
)

SETUP_STATUS_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[SETUP_STATUS_REQUIRED_RESPONSE_EXAMPLE],
)
