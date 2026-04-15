from drf_spectacular.utils import OpenApiExample

AUTH_VALIDATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Auth missing required fields",
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
            "username": ["This field is required."],
            "password": ["This field is required."],
        },
    },
)

AUTH_LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    name="User login request",
    description="Example request payload for user login.",
    value={
        "username": "mhillcrest",
        "password": "strongPassword$1",
    },
    request_only=True,
)

AUTH_LOGIN_RESPONSE_EXAMPLE = OpenApiExample(
    name="Successful login",
    description=(
        "Example response returned after successful login."
    ),
    status_codes=["200"],
    response_only=True,
    value={
        "status": "success",
        "data": None,
        "message": "Login successful",
    },
)

AUTH_LOGIN_UNAUTHORIZED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Invalid provided credentials",
    description=(
        "Example response returned when logging in with "
        "invalid credentials."
    ),
    status_codes=["401"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "Unable to log in with provided credentials.",
    },
)

AUTH_LOGOUT_RESPONSE_EXAMPLE = OpenApiExample(
    name="Successful logout",
    description=(
        "Example response returned after successful logout."
    ),
    status_codes=["200"],
    response_only=True,
    value={
        "status": "success",
        "data": None,
        "message": "Logged out successfully.",
    },
)

AUTH_LOGOUT_UNAUTHORIZED_RESPONSE_EXAMPLE = OpenApiExample(
    name="Invalid provided token",
    description=(
        "Example response returned when attempting to log out "
        "with an invalid or expired authentication token."
    ),
    status_codes=["401"],
    response_only=True,
    value={
        "status": "error",
        "data": None,
        "message": "Invalid token.",
    },
)
