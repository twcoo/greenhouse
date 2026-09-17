from django.urls import include, path

from ..views import FertilizerDetailApiView, FertilizerListApiView

urlpatterns = [
    # List and create
    path(
        "",
        FertilizerListApiView.as_view(),
        name="fertilizer-list-create",
    ),
    # Get, partial update, full update, and delete
    path(
        "<int:pk>",
        FertilizerDetailApiView.as_view(),
        name="fertilizer-detail",
    ),
    # Logs (nested)
    path(
        "<int:fertilizer_pk>/logs/",
        include("greenhouse.urls.fertilizer_log"),
    ),
]
