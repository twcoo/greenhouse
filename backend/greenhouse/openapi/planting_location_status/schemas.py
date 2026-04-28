from ...serializers.planting_location_status import \
    PlantingLocationStatusSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_LOCATION_STATUS_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingLocationStatusSerializer,
).get_schema()
