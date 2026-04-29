from typing import Any, cast

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import (Planting, PlantingLocationAssignment,
                      PlantingLocationStatus)
from ..openapi.planting_location_assignment.examples import (
    CREATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE,
    PARTIAL_UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE,
    UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE)
from ..openapi.planting_location_assignment.parameters import (
    PLANTING_LOCATION_ASSIGNMENT_ID_PARAM, PLANTING_PK_PARAM)
from ..openapi.planting_location_assignment.responses import (
    PLANTING_LOCATION_ASSIGNMENT_CREATE_VALIDATION_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_CREATED_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_DELETE_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_LIST_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_RETRIEVE_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_UPDATE_RESPONSE,
    PLANTING_LOCATION_ASSIGNMENT_UPDATE_VALIDATION_RESPONSE)
from ..serializers import PlantingLocationAssignmentSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Location Assignment"],
        summary="List planting location assignments",
        description=(
            "Returns a list of location assignments for the specified "
            "planting, ordered by start date. Results are scoped to the "
            "authenticated user's planting."
        ),
        parameters=PLANTING_PK_PARAM,
        responses={
            200: PLANTING_LOCATION_ASSIGNMENT_LIST_RESPONSE,
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Planting Location Assignment"],
        summary="Create planting location assignment",
        description=(
            "Assign the specified planting to a location with a start date. "
            "The date range must not overlap with any existing assignment "
            "for this planting."
        ),
        parameters=PLANTING_PK_PARAM,
        examples=[CREATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE],
        responses={
            201: PLANTING_LOCATION_ASSIGNMENT_CREATED_RESPONSE,
            400: PLANTING_LOCATION_ASSIGNMENT_CREATE_VALIDATION_RESPONSE,
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingLocationAssignmentListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlantingLocationAssignmentSerializer

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
        return PlantingLocationAssignment.objects.filter(
            planting=self._get_planting()
        ).order_by("start_date")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["planting"] = self._get_planting()
        return context

    def perform_create(self, serializer):
        assignment = serializer.save(planting=self._get_planting())
        location = assignment.planting_location
        if location.location_type in ["NURSERYPOT", "POT"]:
            PlantingLocationStatus.objects.create(
                planting_location=location, status="IN_USE"
            )

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Location Assignment"],
        summary="Retrieve a planting location assignment",
        description=("Retrieve a single planting location assignment by ID."),
        parameters=PLANTING_LOCATION_ASSIGNMENT_ID_PARAM,
        responses={
            200: PLANTING_LOCATION_ASSIGNMENT_RETRIEVE_RESPONSE,
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Planting Location Assignment"],
        summary="Update a planting location assignment",
        description=("Updates an existing planting location assignment by ID."),
        parameters=PLANTING_LOCATION_ASSIGNMENT_ID_PARAM,
        examples=[UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_LOCATION_ASSIGNMENT_UPDATE_RESPONSE,
            400: PLANTING_LOCATION_ASSIGNMENT_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Planting Location Assignment"],
        summary="Partially update a planting location assignment",
        description=(
            "Partially updates an existing planting location assignment "
            "by ID."
        ),
        parameters=PLANTING_LOCATION_ASSIGNMENT_ID_PARAM,
        examples=[PARTIAL_UPDATE_PLANTING_LOCATION_ASSIGNMENT_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_LOCATION_ASSIGNMENT_UPDATE_RESPONSE,
            400: (
                PLANTING_LOCATION_ASSIGNMENT_PARTIAL_UPDATE_VALIDATION_RESPONSE
            ),
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Planting Location Assignment"],
        summary="Delete a planting location assignment",
        description=("Deletes an existing planting location assignment by ID."),
        parameters=PLANTING_LOCATION_ASSIGNMENT_ID_PARAM,
        responses={
            204: PLANTING_LOCATION_ASSIGNMENT_DELETE_RESPONSE,
            404: PLANTING_LOCATION_ASSIGNMENT_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingLocationAssignmentDetailApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlantingLocationAssignmentSerializer

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
        return PlantingLocationAssignment.objects.filter(
            planting=self._get_planting()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["planting"] = self._get_planting()
        return context

    def perform_update(self, serializer):
        end_date_before = serializer.instance.end_date
        assignment = serializer.save()
        location = assignment.planting_location
        if (
            location.location_type in ["NURSERYPOT", "POT"]
            and end_date_before is None
            and assignment.end_date is not None
        ):
            PlantingLocationStatus.objects.create(
                planting_location=location, status="AVAILABLE"
            )

    def perform_destroy(self, instance):
        location = instance.planting_location
        super().perform_destroy(instance)
        if location.location_type in ["NURSERYPOT", "POT"]:
            PlantingLocationStatus.objects.create(
                planting_location=location, status="AVAILABLE"
            )

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
