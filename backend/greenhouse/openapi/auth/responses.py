from drf_spectacular.utils import OpenApiResponse

from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (
    AUTH_LOGIN_RESPONSE_EXAMPLE,
    AUTH_LOGIN_UNAUTHORIZED_RESPONSE_EXAMPLE,
    AUTH_LOGOUT_RESPONSE_EXAMPLE,
    AUTH_LOGOUT_UNAUTHORIZED_RESPONSE_EXAMPLE,
    AUTH_VALIDATION_RESPONSE_EXAMPLE,
)
from .schemas import AUTH_RESPONSE_DATA_SCHEMA

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
