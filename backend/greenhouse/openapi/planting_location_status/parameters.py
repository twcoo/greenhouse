from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

PLANTING_LOCATION_PK_PARAM = [
    OpenApiParameter(
        name="pk",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the planting location.",
        required=True,
    )
]
