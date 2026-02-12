from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer, KnoxLoginResponseSerializer

CROP_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=CropSerializer,
    additional_required_data_fields=["id", "category", "sunlight_requirement"],
).get_schema()

AUTH_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=KnoxLoginResponseSerializer,
).get_schema()
