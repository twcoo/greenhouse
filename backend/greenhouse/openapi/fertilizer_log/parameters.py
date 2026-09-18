from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

FERTILIZER_PK_PARAM = [
    OpenApiParameter(
        name="fertilizer_pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the fertilizer.",
        required=True,
    )
]

FERTILIZER_LOG_ID_PARAM = [
    OpenApiParameter(
        name="fertilizer_pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the fertilizer.",
        required=True,
    ),
    OpenApiParameter(
        name="pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the log entry.",
        required=True,
    ),
]
