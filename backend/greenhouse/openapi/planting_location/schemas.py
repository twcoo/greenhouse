from ...serializers import PlantingLocationSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_LOCATION_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingLocationSerializer,
).get_schema()
