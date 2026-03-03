from django.urls import path

from ..views import CropDetailAPIView, CropListAPIView, CropUploadImageAPIView

urlpatterns = [
    # List and create
    path("", CropListAPIView.as_view(), name="crop-list-create"),
    # Get, partial update, full update, and delete
    path("<int:pk>", CropDetailAPIView.as_view(), name="crop-detail"),
    # Upload image
    path(
        "<int:pk>/image/",
        CropUploadImageAPIView.as_view(),
        name="crop-image-upload",
    ),
]
