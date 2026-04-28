from django.urls import include, path

from ..views import PlantingLocationDetailAPIView, PlantingLocationListApiView

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
    # Status history (nested)
    path(
        "<int:pk>/statuses/",
        include("greenhouse.urls.planting_location_status"),
    ),
]
