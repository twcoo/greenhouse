from ...serializers import CropSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

CROP_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=CropSerializer,
    additional_required_data_fields=[
        "id",
        "category",
        "sunlight_requirement",
    ],
).get_schema()
