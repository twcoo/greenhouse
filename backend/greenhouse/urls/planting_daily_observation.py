from django.urls import path

from ..views import (PlantingDailyObservationDetailApiView,
                     PlantingDailyObservationListApiView)

urlpatterns = [
    path(
        "",
        PlantingDailyObservationListApiView.as_view(),
        name="planting-daily-observation-list-create",
    ),
    path(
        "<int:pk>",
        PlantingDailyObservationDetailApiView.as_view(),
        name="planting-daily-observation-detail",
    ),
]
