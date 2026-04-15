from ...serializers import VarietySerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

VARIETY_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=VarietySerializer,
).get_schema()
