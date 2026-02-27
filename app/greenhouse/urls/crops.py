from django.urls import path

from ..views import CropDetailAPIView, CropListApiView, CropUploadImageView

urlpatterns = [
    # List and create
    path("", CropListApiView.as_view(), name="crop-list-create"),
    # Get, partial update, full update, and delete
    path("<int:pk>", CropDetailAPIView.as_view(), name="crop-detail"),
    # Upload image
    path(
        "<int:pk>/image/",
        CropUploadImageView.as_view(),
        name="crop-image-upload",
    ),
]
