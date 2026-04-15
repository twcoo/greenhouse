from ...serializers import KnoxLoginResponseSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

AUTH_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=KnoxLoginResponseSerializer,
).get_schema()
