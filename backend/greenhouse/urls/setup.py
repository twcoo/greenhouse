from django.urls import path

from ..views import SetupAdminView

urlpatterns = [
    path("admin", SetupAdminView.as_view(), name="setup_admin"),
]
