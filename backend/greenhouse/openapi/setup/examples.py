from drf_spectacular.utils import OpenApiExample

SETUP_ADMIN_REQUEST_EXAMPLE = OpenApiExample(
    name="Initial Admin Setup Request",
    description="Example request payload for initial admin setup.",
    value={
        "username": "mhillcrest",
        "password": "strongPassword$1",
        "password2": "strongPassword$1",
    },
    request_only=True,
)

SETUP_ADMIN_REQUIRED_FIELDS_VALIDATION_RESPONSE_EXAMPLE = (
    OpenApiExample(
        name="Missing required fields",
        description=(
            "Example response returned when required fields are "
            "missing in the request payload."
        ),
        status_codes=["400"],
        response_only=True,
        value={
            "status": "error",
            "data": None,
            "message": {
                "non_field_errors": [
                    "Admin user already exists. "
                    "Setup cannot be run again."
                ]
            },
        },
    )
)

SETUP_ADMIN_ALREADY_EXISTS_RESPONSE_EXAMPLE = OpenApiExample(
    name="Admin already exists",
    description=(
        "Example response returned when attempting to create an "
        "admin but one already exists."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {
            "non_field_errors": [
                "Admin user already exists. "
                "Setup cannot be run again."
            ]
        },
    },
)

SETUP_ADMIN_PASSWORD_MISMATCH_RESPONSE_EXAMPLE = OpenApiExample(
    name="Password mismatch",
    description=(
        "Example response returned when the password and password "
        "confirmation do not match."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": {"password2": ["Passwords do not match."]},
    },
)

SETUP_ADMIN_CREATED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Initial Admin Created",
    description=(
        "Example response returned after successfully creating "
        "the initial admin user."
    ),
    status_codes=["201"],
    response_only=True,
    value={
        "status": "success",
        "data": {
            "user": {"username": "mhillcrest"},
        },
        "message": "Setup successful",
    },
)

SETUP_STATUS_OK_RESPONSE_EXAMPLE = OpenApiExample(
    name="Setup status OK",
    description=(
        "Example response returned when the application "
        "setup status is OK."
    ),
    status_codes=["200"],
    response_only=True,
    value={
        "status": "success",
        "data": None,
        "message": "ok",
    },
)

SETUP_STATUS_REQUIRED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Setup required",
    description=(
        "Example response returned when the application "
        "requires initial setup."
    ),
    status_codes=["400"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "Setup required.",
    },
)
