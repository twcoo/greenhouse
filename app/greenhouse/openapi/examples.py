from drf_spectacular.utils import OpenApiExample

CREATE_CROP_REQUEST_EXAMPLE = OpenApiExample(
    name="Create tomato crop payload",
    summary="Create a tomato crop",
    description="Example request payload for creating a tomato crop.",
    value={
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "VEGETABLE",
        "sunlight_requirement": "FULL_SUN",
        "min_days_to_harvest": 60,
        "max_days_to_harvest": 90,
    },
    request_only=True,
)

CROP_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
    name="Required field missing",
    summary="Missing required fields",
    description=(
        "This response is returned when one or more required fields are missing "
        "in the request payload."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "name": ["This field is required."],
            "scientific_name": ["This field is required."],
        },
    },
)
