from .auth import LoginView, LogoutView
from .crops import CropDetailAPIView, CropListAPIView, CropUploadImageAPIView
from .fertilizer import FertilizerDetailApiView, FertilizerListApiView
from .fertilizer_log import (FertilizerLogDetailApiView,
                             FertilizerLogListApiView)
from .planting import PlantingDetailApiView, PlantingListApiView
from .planting_daily_observation import (
    PlantingDailyObservationBulkCreateApiView,
    PlantingDailyObservationDetailApiView, PlantingDailyObservationListApiView)
from .planting_location import (PlantingLocationDetailAPIView,
                                PlantingLocationListApiView)
from .planting_location_assignment import (
    PlantingLocationAssignmentDetailApiView,
    PlantingLocationAssignmentListApiView)
from .planting_location_status import PlantingLocationStatusListApiView
from .setup import SetupAdminView, SetupStatusView
from .variety import VarietyDetailAPIView, VarietyListApiView

__all__ = [
    "SetupAdminView",
    "SetupStatusView",
    "LoginView",
    "LogoutView",
    "CropDetailAPIView",
    "CropListAPIView",
    "CropUploadImageAPIView",
    "FertilizerListApiView",
    "FertilizerDetailApiView",
    "FertilizerLogListApiView",
    "FertilizerLogDetailApiView",
    "PlantingLocationListApiView",
    "PlantingLocationDetailAPIView",
    "VarietyListApiView",
    "VarietyDetailAPIView",
    "PlantingListApiView",
    "PlantingDetailApiView",
    "PlantingLocationAssignmentListApiView",
    "PlantingLocationAssignmentDetailApiView",
    "PlantingDailyObservationListApiView",
    "PlantingDailyObservationDetailApiView",
    "PlantingDailyObservationBulkCreateApiView",
    "PlantingLocationStatusListApiView",
]
