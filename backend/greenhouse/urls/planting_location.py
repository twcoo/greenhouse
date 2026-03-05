from django.urls import path

from ..views import (PlantingLocationDetailAPIView,
                     PlantingLocationListApiView,
                     PlantingLocationUploadImageView)

urlpatterns = [
    # List and create
    path(
        "",
        PlantingLocationListApiView.as_view(),
        name="planting-location-list-create",
    ),
    # Get, partial update, full update, and delete
    path(
        "<int:pk>",
        PlantingLocationDetailAPIView.as_view(),
        name="planting-location-detail",
    ),
    # Upload image
    path(
        "<int:pk>/image/",
        PlantingLocationUploadImageView.as_view(),
        name="planting-location-image-upload",
    ),
]
