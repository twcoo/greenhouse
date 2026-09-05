from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

PLANTING_DAILY_OBSERVATION_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Planting Daily Observation",
    description="Example of a planting daily observation entry.",
    value={
        "id": 1,
        "stage": None,
        "stage_name": None,
        "health_status": "GOOD",
        "pest_pressure": "NONE",
        "disease_symptoms": False,
        "watering_event": "SKIPPED_WET",
        "pruned": False,
        "notes": "Looking healthy. New leaves forming.",
        "image": None,
        "observation_date": "2024-03-01",
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
        "observation_date": "2024-03-01",
        "health_status": "GOOD",
        "watering_event": "SKIPPED_WET",
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
            "health_status": "GOOD",
            "pest_pressure": "NONE",
            "disease_symptoms": False,
            "watering_event": "SKIPPED_WET",
            "pruned": False,
            "notes": "Looking healthy. New leaves forming.",
            "image": None,
            "observation_date": "2024-03-01",
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
        "observation_date": "2024-03-01",
        "health_status": "FAIR",
        "watering_event": "WATERED",
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
            "health_status": "FAIR",
            "pest_pressure": "NONE",
            "disease_symptoms": False,
            "watering_event": "WATERED",
            "pruned": False,
            "notes": "Slight yellowing on lower leaves.",
            "image": None,
            "observation_date": "2024-03-01",
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

PLANTING_DAILY_OBSERVATION_INVALID_WATERING_EVENT_EXAMPLE = OpenApiExample(
    name="Invalid watering event choice",
    summary="Watering event value is not a valid choice",
    description=(
        "Example response returned when the watering_event value is not "
        "one of the accepted choices."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "watering_event": ['"SPRINKLER" is not a valid choice.'],
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

BULK_CREATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE = OpenApiExample(
    name="Bulk create daily observation payload",
    summary="Log the same daily observation for multiple plantings",
    description=(
        "Example request payload for bulk logging a daily observation "
        "across multiple plantings."
    ),
    value={
        "planting_ids": [1, 2, 3],
        "observation_date": "2024-03-01",
        "health_status": "GOOD",
        "watering_event": "SKIPPED_WET",
        "notes": "All looking healthy.",
    },
    media_type="application/json",
    request_only=True,
)

BULK_CREATE_PLANTING_DAILY_OBSERVATION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Bulk daily observations created",
    summary="Successfully logged daily observations for multiple plantings",
    description=(
        "Example response returned after daily observations are "
        "successfully created for multiple plantings."
    ),
    value={
        "status": "success",
        "data": [
            {
                "id": 1,
                "stage": None,
                "stage_name": None,
                "health_status": "GOOD",
                "pest_pressure": "NONE",
                "disease_symptoms": False,
                "watering_event": "SKIPPED_WET",
                "pruned": False,
                "notes": "All looking healthy.",
                "image": None,
                "observation_date": "2024-03-01",
                "created_at": "2024-03-01T08:00:00Z",
                "updated_at": "2024-03-01T08:00:00Z",
            },
            {
                "id": 2,
                "stage": None,
                "stage_name": None,
                "health_status": "GOOD",
                "pest_pressure": "NONE",
                "disease_symptoms": False,
                "watering_event": "SKIPPED_WET",
                "pruned": False,
                "notes": "All looking healthy.",
                "image": None,
                "observation_date": "2024-03-01",
                "created_at": "2024-03-01T08:00:00Z",
                "updated_at": "2024-03-01T08:00:00Z",
            },
        ],
        "message": None,
    },
)

BULK_CREATE_INVALID_PLANTING_IDS_EXAMPLE = OpenApiExample(
    name="Invalid planting IDs",
    summary="One or more planting IDs are invalid",
    description=(
        "Example response returned when one or more planting IDs do not "
        "exist or belong to another user."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "planting_ids": [
                "One or more planting IDs are invalid or do not belong "
                "to the current user."
            ],
        },
    },
)
