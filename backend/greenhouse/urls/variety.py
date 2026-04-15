from django.urls import path

from ..views import VarietyDetailAPIView, VarietyListApiView

urlpatterns = [
    # List and create
    path(
        "",
        VarietyListApiView.as_view(),
        name="variety-list-create",
    ),
    # Get, partial update, full update, and delete
    path(
        "<int:pk>",
        VarietyDetailAPIView.as_view(),
        name="variety-detail",
    ),
]
