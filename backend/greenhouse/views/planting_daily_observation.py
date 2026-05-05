from typing import Any, cast

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Planting, PlantingDailyObservation
from ..openapi.planting_daily_observation.examples import (
    CREATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE,
    PARTIAL_UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE,
    UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE)
from ..openapi.planting_daily_observation.parameters import (
    PLANTING_DAILY_OBSERVATION_ID_PARAM, PLANTING_PK_PARAM)
from ..openapi.planting_daily_observation.responses import (
    PLANTING_DAILY_OBSERVATION_CREATE_VALIDATION_RESPONSE,
    PLANTING_DAILY_OBSERVATION_CREATED_RESPONSE,
    PLANTING_DAILY_OBSERVATION_DELETE_RESPONSE,
    PLANTING_DAILY_OBSERVATION_LIST_RESPONSE,
    PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
    PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_RESPONSE,
    PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    PLANTING_DAILY_OBSERVATION_UPDATE_RESPONSE,
    PLANTING_DAILY_OBSERVATION_UPDATE_VALIDATION_RESPONSE)
from ..serializers import PlantingDailyObservationSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Daily Observation"],
        summary="List daily observations",
        description=(
            "Returns a paginated list of daily observations for the "
            "specified planting, ordered most recent first. Results are "
            "scoped to the authenticated user."
        ),
        parameters=PLANTING_PK_PARAM,
        responses={
            200: PLANTING_DAILY_OBSERVATION_LIST_RESPONSE,
            404: PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Planting Daily Observation"],
        summary="Log a daily observation",
        description=("Log a new daily observation for the specified planting."),
        parameters=PLANTING_PK_PARAM,
        examples=[CREATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE],
        responses={
            201: PLANTING_DAILY_OBSERVATION_CREATED_RESPONSE,
            400: PLANTING_DAILY_OBSERVATION_CREATE_VALIDATION_RESPONSE,
            404: PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingDailyObservationListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlantingDailyObservationSerializer
    parser_classes = [MultiPartParser]

    def _get_planting(self) -> Planting:
        return cast(
            Planting,
            get_object_or_404(
                Planting,
                pk=self.kwargs["planting_pk"],
                user=self.request.user,
            ),
        )

    def get_queryset(self):
        return PlantingDailyObservation.objects.filter(
            planting=self._get_planting()
        ).order_by("-pk")

    def perform_create(self, serializer):
        serializer.save(planting=self._get_planting())

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    put=extend_schema(
        tags=["Planting Daily Observation"],
        summary="Update a daily observation",
        description="Updates an existing daily observation by ID.",
        parameters=PLANTING_DAILY_OBSERVATION_ID_PARAM,
        examples=[UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_DAILY_OBSERVATION_UPDATE_RESPONSE,
            400: PLANTING_DAILY_OBSERVATION_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Planting Daily Observation"],
        summary="Partially update a daily observation",
        description=(
            "Partially updates an existing daily observation by ID. "
            "Only the fields provided will be updated."
        ),
        parameters=PLANTING_DAILY_OBSERVATION_ID_PARAM,
        examples=[PARTIAL_UPDATE_PLANTING_DAILY_OBSERVATION_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_RESPONSE,
            400: (
                PLANTING_DAILY_OBSERVATION_PARTIAL_UPDATE_VALIDATION_RESPONSE
            ),
            404: PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Planting Daily Observation"],
        summary="Delete a daily observation",
        description="Deletes an existing daily observation by ID.",
        parameters=PLANTING_DAILY_OBSERVATION_ID_PARAM,
        responses={
            204: PLANTING_DAILY_OBSERVATION_DELETE_RESPONSE,
            404: PLANTING_DAILY_OBSERVATION_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingDailyObservationDetailApiView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlantingDailyObservationSerializer
    parser_classes = [MultiPartParser]

    def _get_planting(self) -> Planting:
        return cast(
            Planting,
            get_object_or_404(
                Planting,
                pk=self.kwargs["planting_pk"],
                user=self.request.user,
            ),
        )

    def get_queryset(self):
        return PlantingDailyObservation.objects.filter(
            planting=self._get_planting()
        )

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
