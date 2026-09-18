from ...serializers import FertilizerLogSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

FERTILIZER_LOG_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=FertilizerLogSerializer,
).get_schema()
