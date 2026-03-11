from django.urls import path

from ..views import SetupAdminView, SetupStatusView

urlpatterns = [
    path("admin", SetupAdminView.as_view(), name="setup_admin"),
    path("status", SetupStatusView.as_view(), name="setup_status"),
]
