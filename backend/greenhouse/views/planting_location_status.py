from typing import Any, cast

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import PlantingLocation, PlantingLocationStatus
from ..openapi.planting_location_status.examples import \
    CREATE_PLANTING_LOCATION_STATUS_REQUEST_EXAMPLE
from ..openapi.planting_location_status.parameters import \
    PLANTING_LOCATION_PK_PARAM
from ..openapi.planting_location_status.responses import (
    PLANTING_LOCATION_STATUS_CREATE_VALIDATION_RESPONSE,
    PLANTING_LOCATION_STATUS_CREATED_RESPONSE,
    PLANTING_LOCATION_STATUS_LIST_RESPONSE,
    PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE)
from ..serializers import PlantingLocationStatusSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Location Status"],
        summary="List planting location status history",
        description=(
            "Returns a paginated list of status entries for the specified "
            "planting location, ordered most recent first. Results are "
            "scoped to the authenticated user."
        ),
        parameters=PLANTING_LOCATION_PK_PARAM,
        responses={
            200: PLANTING_LOCATION_STATUS_LIST_RESPONSE,
            404: PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Planting Location Status"],
        summary="Record a planting location status",
        description=(
            "Record a new status entry for the specified planting location."
        ),
        parameters=PLANTING_LOCATION_PK_PARAM,
        examples=[CREATE_PLANTING_LOCATION_STATUS_REQUEST_EXAMPLE],
        responses={
            201: PLANTING_LOCATION_STATUS_CREATED_RESPONSE,
            400: PLANTING_LOCATION_STATUS_CREATE_VALIDATION_RESPONSE,
            404: PLANTING_LOCATION_STATUS_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingLocationStatusListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlantingLocationStatusSerializer
    parser_classes = [MultiPartParser]

    def _get_planting_location(self) -> PlantingLocation:
        return cast(
            PlantingLocation,
            get_object_or_404(
                PlantingLocation,
                pk=self.kwargs["pk"],
                user=self.request.user,
            ),
        )

    def get_queryset(self):
        return PlantingLocationStatus.objects.filter(
            planting_location=self._get_planting_location()
        ).order_by("-pk")

    def perform_create(self, serializer):
        serializer.save(planting_location=self._get_planting_location())

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)
