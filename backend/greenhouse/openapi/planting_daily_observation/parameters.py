from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

PLANTING_PK_PARAM = [
    OpenApiParameter(
        name="planting_pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the planting.",
        required=True,
    )
]

PLANTING_DAILY_OBSERVATION_ID_PARAM = [
    OpenApiParameter(
        name="planting_pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the planting.",
        required=True,
    ),
    OpenApiParameter(
        name="pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the observation.",
        required=True,
    ),
]
