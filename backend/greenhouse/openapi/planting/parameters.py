from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

PLANTING_ID_PARAM = [
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the planting.",
        required=True,
    )
]

PLANTING_STATUS_PARAM = [
    OpenApiParameter(
        name="status",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description=(
            "Filter plantings by status. Use 'all' to return every "
            "status. Defaults to 'ACTIVE'."
        ),
        required=False,
        enum=["ACTIVE", "HARVESTED", "DEAD", "REMOVED", "all"],
    )
]
