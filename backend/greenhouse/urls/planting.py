from django.urls import include, path

from ..views import PlantingDetailApiView, PlantingListApiView

urlpatterns = [
    # List and create
    path(
        "",
        PlantingListApiView.as_view(),
        name="planting-list-create",
    ),
    # Get, partial update, full update, and delete
    path(
        "<int:pk>",
        PlantingDetailApiView.as_view(),
        name="planting-detail",
    ),
    # Planting location assignments (nested)
    path(
        "<int:planting_pk>/locations/",
        include("greenhouse.urls.planting_location_assignment"),
    ),
    # Daily observations (nested)
    path(
        "<int:planting_pk>/observations/",
        include("greenhouse.urls.planting_daily_observation"),
    ),
]
