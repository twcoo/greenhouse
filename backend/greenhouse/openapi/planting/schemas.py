from ...serializers import PlantingSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingSerializer,
).get_schema()
