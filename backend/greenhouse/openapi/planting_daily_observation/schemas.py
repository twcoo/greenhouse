from ...serializers.planting_daily_observation import \
    PlantingDailyObservationSerializer
from ..shared.schemas import CustomOpenAPIResponseSchema

PLANTING_DAILY_OBSERVATION_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingDailyObservationSerializer,
).get_schema()
