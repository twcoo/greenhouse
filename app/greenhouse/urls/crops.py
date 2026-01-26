from django.urls import path

from ..views import CropDetailAPIView

urlpatterns = [
    path("", CropDetailAPIView.as_view(), name="crop-list-create"),
]
