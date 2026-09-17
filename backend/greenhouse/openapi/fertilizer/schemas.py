from ...serializers import FertilizerSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

FERTILIZER_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=FertilizerSerializer,
).get_schema()
