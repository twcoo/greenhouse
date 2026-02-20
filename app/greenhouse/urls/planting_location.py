from django.urls import path

from ..views import PlantingLocationListApiView

urlpatterns = [
    # List and create
    path(
        "",
        PlantingLocationListApiView.as_view(),
        name="planting-location-list-create",
    ),
    # Get, partial update, full update, and delete
    # path("<int:pk>", CropDetailAPIView.as_view(), name="crop-detail"),
]
