from ...serializers.planting_location_assignment import \
    PlantingLocationAssignmentSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_LOCATION_ASSIGNMENT_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingLocationAssignmentSerializer,
).get_schema()
