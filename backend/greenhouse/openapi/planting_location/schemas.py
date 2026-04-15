from ...serializers import (PlantingLocationImageSerializer,
                            PlantingLocationSerializer)
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_LOCATION_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingLocationSerializer,
).get_schema()

PLANTING_LOCATION_UPLOADED_IMAGE_RESPONSE_DATA_SCHEMA = (
    CustomOpenAPIResponseSchema(
        data_serializer=PlantingLocationImageSerializer,
    ).get_schema()
)
