from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_DAILY_OBSERVATION_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Daily Observation",
    description="Example of a planting daily observation entry.",
    value={
        "id": 1,
        "stage": None,
        "stage_name": None,
        "height_cm": "12.50",
        "leaf_count": 8,
        "temperature_c": "24.5",
        "humidity_percent": "65.00",
        "light_hours": "14.00",
        "soil_moisture_percent": "55.00",
        "soil_ph": "6.5",
        "ec_ms_cm": "1.80",
        "health_status": "GOOD",
        "pest_pressure": "NONE",
        "disease_symptoms": False,
        "watered": False,
        "notes": "Looking healthy. New leaves forming.",
        "image": None,
        "created_at": "2024-03-01T08:00:00Z",
        "updated_at": "2024-03-01T08:00:00Z",
    },
)

CREATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Create planting daily observation payload",
    summary="Log a new daily observation",
    description=(
        "Example request payload for logging a new daily observation "
        "for a planting."
    ),
    value={
        "health_status": "GOOD",
        "height_cm": "12.50",
        "leaf_count": 8,
        "notes": "Looking healthy. New leaves forming.",
    },
    media_type="multipart/form-data",
    request_only=True,
)

CREATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting daily observation created",
    summary="Successfully logged daily observation",
    description=(
        "Example response returned after a daily observation is "
        "successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "stage": None,
            "stage_name": None,
            "height_cm": "12.50",
            "leaf_count": 8,
            "temperature_c": None,
            "humidity_percent": None,
            "light_hours": None,
            "soil_moisture_percent": None,
            "soil_ph": None,
            "ec_ms_cm": None,
            "health_status": "GOOD",
            "pest_pressure": "NONE",
            "disease_symptoms": False,
            "watered": False,
            "notes": "Looking healthy. New leaves forming.",
            "image": None,
            "created_at": "2024-03-01T08:00:00Z",
            "updated_at": "2024-03-01T08:00:00Z",
        },
        "message": None,
    },
)

UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Update planting daily observation payload",
    summary="Update a daily observation",
    description=("Example request payload for updating a daily observation."),
    value={
        "health_status": "FAIR",
        "height_cm": "14.00",
        "leaf_count": 10,
        "notes": "Slight yellowing on lower leaves.",
    },
    media_type="multipart/form-data",
    request_only=True,
)

PARTIAL_UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Partial update planting daily observation payload",
    summary="Partially update a daily observation",
    description=(
        "Example request payload for partially updating a daily "
        "observation. Only the fields provided will be updated."
    ),
    value={
        "notes": "Updated after re-inspection. Growth looks normal.",
    },
    media_type="multipart/form-data",
    request_only=True,
)

UPDATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Planting daily observation updated",
    summary="Successfully updated daily observation",
    description=(
        "Example response returned after a daily observation is "
        "successfully updated."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "stage": None,
            "stage_name": None,
            "height_cm": "14.00",
            "leaf_count": 10,
            "temperature_c": "24.5",
            "humidity_percent": "65.00",
            "light_hours": "14.00",
            "soil_moisture_percent": "55.00",
            "soil_ph": "6.5",
            "ec_ms_cm": "1.80",
            "health_status": "FAIR",
            "pest_pressure": "NONE",
            "disease_symptoms": False,
            "watered": False,
            "notes": "Slight yellowing on lower leaves.",
            "image": None,
            "created_at": "2024-03-01T08:00:00Z",
            "updated_at": "2024-03-02T09:00:00Z",
        },
        "message": None,
    },
)

PLANTING_DAILY_OBSERVATION_INVALID_CHOICE_EXAMPLE = OpenApiExample(
    name="Invalid health status choice",
    summary="Health status value is not a valid choice",
    description=(
        "Example response returned when the health_status value is not "
        "one of the accepted choices."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "health_status": ['"UNKNOWN" is not a valid choice.'],
        },
    },
)

PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Resource not found",
    summary="No planting or observation exists with the provided ID.",
    description=(
        "Example response returned when no planting or daily "
        "observation exists for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)
