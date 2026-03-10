from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        f"api/{settings.API_VERSION}/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        f"api/{settings.API_VERSION}/docs",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        f"api/{settings.API_VERSION}/setup/", include("greenhouse.urls.setup")
    ),
    path(f"api/{settings.API_VERSION}/auth/", include("greenhouse.urls.auth")),
    path(
        f"api/{settings.API_VERSION}/crops/", include("greenhouse.urls.crops")
    ),
    path(
        f"api/{settings.API_VERSION}/planting-locations/",
        include("greenhouse.urls.planting_location"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
