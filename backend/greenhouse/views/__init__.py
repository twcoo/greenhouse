from .auth import LoginView, LogoutView
from .crops import CropDetailAPIView, CropListAPIView, CropUploadImageAPIView
from .planting import PlantingDetailApiView, PlantingListApiView
from .planting_location import (PlantingLocationDetailAPIView,
                                PlantingLocationListApiView,
                                PlantingLocationUploadImageView)
from .planting_location_assignment import (
    PlantingLocationAssignmentDetailApiView,
    PlantingLocationAssignmentListApiView)
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
    "PlantingLocationUploadImageView",
    "VarietyListApiView",
    "VarietyDetailAPIView",
    "PlantingListApiView",
    "PlantingDetailApiView",
    "PlantingLocationAssignmentListApiView",
    "PlantingLocationAssignmentDetailApiView",
]
