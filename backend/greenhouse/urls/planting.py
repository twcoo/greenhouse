from django.urls import path

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
]
