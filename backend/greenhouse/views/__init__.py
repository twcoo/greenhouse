from .auth import LoginView, LogoutView
from .crops import CropDetailAPIView, CropListAPIView, CropUploadImageAPIView
from .planting import PlantingDetailApiView, PlantingListApiView
from .planting_daily_observation import (PlantingDailyObservationDetailApiView,
                                         PlantingDailyObservationListApiView)
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
    "PlantingLocationStatusListApiView",
]
