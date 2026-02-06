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
