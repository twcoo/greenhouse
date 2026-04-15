from drf_spectacular.utils import OpenApiParameter

CSRFTOKEN_PARAM = [
    OpenApiParameter(
        name="X-CSRFToken",
        type=str,
        location=OpenApiParameter.HEADER,
        required=True,
        description="CSRF token to authorize the request",
    ),
]
