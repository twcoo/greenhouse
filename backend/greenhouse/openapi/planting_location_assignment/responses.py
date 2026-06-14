from drf_spectacular.utils import OpenApiResponse

from ...serializers.planting_location_assignment import \
    PlantingLocationAssignmentSerializer
from ..shared.examples import NO_DATA_RESPONSE_EXAMPLE
from ..shared.schemas import CustomOpenAPIResponseSchema
from .examples import (CREATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_ACTIVE_EXISTS_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_ALREADY_ASSIGNED_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_DATE_ORDER_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_LOCATION_OCCUPIED_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_OVERLAP_EXAMPLE,
                       PLANTING_LOCATION_ASSIGNMENT_REQUIRED_FIELDS_EXAMPLE,
                       RETRIEVE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE,
                       UPDATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE)
from .schemas import PLANTING_LOCATION_ASSIGNMENT_RESPONSE_DATA_SCHEMA

PLANTING_LOCATION_ASSIGNMENT_LIST_RESPONSE = OpenApiResponse(
    description=("List of location assignments for the specified planting."),
    response=PlantingLocationAssignmentSerializer,
)

PLANTING_LOCATION_ASSIGNMENT_CREATED_RESPONSE = OpenApiResponse(
    description="Planting location assignment created successfully.",
    response=PLANTING_LOCATION_ASSIGNMENT_RESPONSE_DATA_SCHEMA,
    examples=[CREATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_ASSIGNMENT_CREATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_LOCATION_ASSIGNMENT_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_DATE_ORDER_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_OVERLAP_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_LOCATION_OCCUPIED_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_ALREADY_ASSIGNED_EXAMPLE,
    ],
)

PLANTING_LOCATION_ASSIGNMENT_RETRIEVE_RESPONSE = OpenApiResponse(
    description="Planting location assignment retrieved successfully.",
    response=PLANTING_LOCATION_ASSIGNMENT_RESPONSE_DATA_SCHEMA,
    examples=[RETRIEVE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_ASSIGNMENT_UPDATE_RESPONSE = OpenApiResponse(
    description="Planting location assignment updated successfully.",
    response=PLANTING_LOCATION_ASSIGNMENT_RESPONSE_DATA_SCHEMA,
    examples=[UPDATE_PLANTING_LOCATION_ASSIGNMENT_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_ASSIGNMENT_UPDATE_VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid request due to validation errors.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        PLANTING_LOCATION_ASSIGNMENT_REQUIRED_FIELDS_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_DATE_ORDER_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_ACTIVE_EXISTS_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_OVERLAP_EXAMPLE,
        PLANTING_LOCATION_ASSIGNMENT_LOCATION_OCCUPIED_EXAMPLE,
    ],
)

PLANTING_LOCATION_ASSIGNMENT_PARTIAL_UPDATE_VALIDATION_RESPONSE = (
    OpenApiResponse(
        description="Invalid request due to validation errors.",
        response=CustomOpenAPIResponseSchema().get_schema(),
        examples=[
            PLANTING_LOCATION_ASSIGNMENT_DATE_ORDER_EXAMPLE,
            PLANTING_LOCATION_ASSIGNMENT_ACTIVE_EXISTS_EXAMPLE,
            PLANTING_LOCATION_ASSIGNMENT_OVERLAP_EXAMPLE,
            PLANTING_LOCATION_ASSIGNMENT_LOCATION_OCCUPIED_EXAMPLE,
        ],
    )
)

PLANTING_LOCATION_ASSIGNMENT_DELETE_RESPONSE = OpenApiResponse(
    description="Planting location assignment deleted successfully.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[NO_DATA_RESPONSE_EXAMPLE],
)

PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested planting location assignment does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE_EXAMPLE],
)
