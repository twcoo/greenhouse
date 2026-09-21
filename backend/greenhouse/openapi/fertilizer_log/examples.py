from drf_spectacular.utils import OpenApiExample

from ..shared.examples import RESOURCE_NOT_FOUND_RESPONSE

FERTILIZER_LOG_SERIALIZER_EXAMPLE = OpenApiExample(
    name="Fertilizer Log",
    description="Example of a fertilizer log entry.",
    value={
        "id": 1,
        "event_type": "ADDED_INGREDIENT",
        "item_added": "banana peels",
        "quantity": "2 kg",
        "notes": "Chopped into small pieces first.",
        "log_date": "2024-03-01",
        "created_at": "2024-03-01T08:00:00Z",
        "updated_at": "2024-03-01T08:00:00Z",
    },
)

CREATE_FERTILIZER_LOG_REQUEST_EXAMPLE = OpenApiExample(
    name="Create fertilizer log payload",
    summary="Log a new fertilizer entry",
    description=(
        "Example request payload for logging a new entry for a fertilizer."
    ),
    value={
        "event_type": "ADDED_INGREDIENT",
        "item_added": "banana peels",
        "quantity": "2 kg",
        "notes": "Chopped into small pieces first.",
        "log_date": "2024-03-01",
    },
    request_only=True,
)

UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE = OpenApiExample(
    name="Update fertilizer log payload",
    summary="Update a fertilizer log entry",
    description="Example request payload for updating a fertilizer log entry.",
    value={
        "event_type": "ADDED_WATER",
        "item_added": "",
        "quantity": "5 liters",
        "notes": "Topped up the barrel.",
        "log_date": "2024-03-01",
    },
    request_only=True,
)

PARTIAL_UPDATE_FERTILIZER_LOG_REQUEST_EXAMPLE = OpenApiExample(
    name="Partial update fertilizer log payload",
    summary="Partially update a fertilizer log entry",
    description=(
        "Example request payload for partially updating a fertilizer "
        "log entry. Only the fields provided will be updated."
    ),
    value={"notes": "Adjusted the notes."},
    request_only=True,
)

CREATE_FERTILIZER_LOG_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer log created",
    summary="Successfully logged fertilizer entry",
    description=(
        "Example response returned after a fertilizer log entry is "
        "successfully created."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "event_type": "ADDED_INGREDIENT",
            "item_added": "banana peels",
            "quantity": "2 kg",
            "notes": "Chopped into small pieces first.",
            "log_date": "2024-03-01",
            "created_at": "2024-03-01T08:00:00Z",
            "updated_at": "2024-03-01T08:00:00Z",
        },
        "message": None,
    },
)

UPDATE_FERTILIZER_LOG_RESPONSE_EXAMPLE = OpenApiExample(
    name="Fertilizer log updated",
    summary="Successfully updated fertilizer log entry",
    description=(
        "Example response returned after a fertilizer log entry is "
        "successfully updated."
    ),
    value={
        "status": "success",
        "data": {
            "id": 1,
            "event_type": "ADDED_WATER",
            "item_added": "",
            "quantity": "5 liters",
            "notes": "Topped up the barrel.",
            "log_date": "2024-03-01",
            "created_at": "2024-03-01T08:00:00Z",
            "updated_at": "2024-03-02T09:00:00Z",
        },
        "message": None,
    },
)

FERTILIZER_LOG_INVALID_CHOICE_EXAMPLE = OpenApiExample(
    name="Invalid event type choice",
    summary="Event type value is not a valid choice",
    description=(
        "Example response returned when the event_type value is not "
        "one of the accepted choices."
    ),
    status_codes=["400"],
    value={
        "status": "error",
        "data": None,
        "message": {
            "event_type": ['"UNKNOWN" is not a valid choice.'],
        },
    },
)

FERTILIZER_LOG_NOT_FOUND_RESPONSE_EXAMPLE = OpenApiExample(
    name="Resource not found",
    summary="No fertilizer or log entry exists with the provided ID.",
    description=(
        "Example response returned when no fertilizer or log entry "
        "exists for the specified ID."
    ),
    value=RESOURCE_NOT_FOUND_RESPONSE,
)
