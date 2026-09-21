from django.urls import path

from ..views import FertilizerLogDetailApiView, FertilizerLogListApiView

urlpatterns = [
    path(
        "",
        FertilizerLogListApiView.as_view(),
        name="fertilizer-log-list-create",
    ),
    path(
        "<int:pk>",
        FertilizerLogDetailApiView.as_view(),
        name="fertilizer-log-detail",
    ),
]
