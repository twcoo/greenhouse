from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

CROP_ID_PARAM = [
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the crop.",
        required=True,
    )
]

PLANTING_LOCATION_ID_PARAM = [
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the planting location.",
        required=True,
    )
]

CSRFTOKEN_PARAM = [
    OpenApiParameter(
        name="X-CSRFToken",
        type=str,
        location=OpenApiParameter.HEADER,
        required=True,
        description="CSRF token to authorize the request",
    ),
]
