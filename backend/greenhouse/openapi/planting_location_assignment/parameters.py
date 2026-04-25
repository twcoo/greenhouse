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

PLANTING_LOCATION_ASSIGNMENT_ID_PARAM = [
    *PLANTING_PK_PARAM,
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description=("Unique identifier of the planting location assignment."),
        required=True,
    ),
]
