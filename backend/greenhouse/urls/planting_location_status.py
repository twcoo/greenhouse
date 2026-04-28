from django.urls import path

from ..views import PlantingLocationStatusListApiView

urlpatterns = [
    # List and create
    path(
        "",
        PlantingLocationStatusListApiView.as_view(),
        name="planting-location-status-list-create",
    ),
]
