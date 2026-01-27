from django.urls import path

from ..views import CropDetailAPIView

urlpatterns = [
    # List and create
    path("", CropDetailAPIView.as_view(), name="crop-list-create"),
    # Get, partial update, full update, and delete
    path("<int:pk>", CropDetailAPIView.as_view(), name="crop-detail"),
]
