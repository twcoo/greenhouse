from django.urls import path

from ..views import (PlantingLocationAssignmentDetailApiView,
                     PlantingLocationAssignmentListApiView)

urlpatterns = [
    # List and create
    path(
        "",
        PlantingLocationAssignmentListApiView.as_view(),
        name="planting-location-assignment-list-create",
    ),
    # Get, partial update, full update, and delete
    path(
        "<int:pk>",
        PlantingLocationAssignmentDetailApiView.as_view(),
        name="planting-location-assignment-detail",
    ),
]
