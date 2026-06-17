from typing import Any

from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import PlantingLocation, PlantingLocationStatus
from ..openapi.planting_location.examples import (
    CREATE_PLANTING_LOCATION_REQUEST_GROUND_EXAMPLE,
    CREATE_PLANTING_LOCATION_REQUEST_POT_EXAMPLE,
    PARTIAL_UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE,
    UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE)
from ..openapi.planting_location.parameters import PLANTING_LOCATION_ID_PARAM
from ..openapi.planting_location.responses import (
    PLANTING_LOCATION_CREATE_VALIDATION_RESPONSE,
    PLANTING_LOCATION_CREATED_RESPONSE, PLANTING_LOCATION_DELETE_RESPONSE,
    PLANTING_LOCATION_LIST_RESPONSE, PLANTING_LOCATION_NOT_FOUND_RESPONSE,
    PLANTING_LOCATION_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    PLANTING_LOCATION_RETRIEVE_RESPONSE, PLANTING_LOCATION_UPDATE_RESPONSE,
    PLANTING_LOCATION_UPDATE_VALIDATION_RESPONSE)
from ..serializers import PlantingLocationSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Location"],
        summary="List planting locations",
        description=(
            "Returns a paginated list of planting location records associated with the "
            "currently authenticated user. Results are scoped per user."
        ),
        responses={
            200: PLANTING_LOCATION_LIST_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Planting Location"],
        summary="Create planting location",
        description=(
            "Create a new planting location record. The planting "
            "location will automatically be associated with the "
            "authenticated user and an initial status of AVAILABLE "
            "will be set."
        ),
        examples=[
            CREATE_PLANTING_LOCATION_REQUEST_GROUND_EXAMPLE,
            CREATE_PLANTING_LOCATION_REQUEST_POT_EXAMPLE,
        ],
        responses={
            201: PLANTING_LOCATION_CREATED_RESPONSE,
            400: PLANTING_LOCATION_CREATE_VALIDATION_RESPONSE,
        },
    ),
)
class PlantingLocationListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    filter_backends = [SearchFilter]
    search_fields = ["name", "location_type"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingLocationSerializer

    def get_queryset(self):
        return PlantingLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            planting_location = serializer.save(user=self.request.user)

            PlantingLocationStatus.objects.create(
                planting_location=planting_location, status="AVAILABLE"
            )

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Planting Location"],
        summary="Retrieve a planting location",
        description="Retrieve a single planting location record by ID.",
        parameters=PLANTING_LOCATION_ID_PARAM,
        responses={
            200: PLANTING_LOCATION_RETRIEVE_RESPONSE,
            404: PLANTING_LOCATION_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Planting Location"],
        summary="Update a planting location",
        description="Updates an existing planting location record by ID.",
        parameters=PLANTING_LOCATION_ID_PARAM,
        examples=[UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_LOCATION_UPDATE_RESPONSE,
            400: PLANTING_LOCATION_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_LOCATION_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Planting Location"],
        summary="Partially update a planting location",
        description="Partially updates an existing planting location record by ID.",
        parameters=PLANTING_LOCATION_ID_PARAM,
        examples=[PARTIAL_UPDATE_PLANTING_LOCATION_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_LOCATION_UPDATE_RESPONSE,
            400: PLANTING_LOCATION_PARTIAL_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_LOCATION_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Planting Location"],
        summary="Delete a crop",
        description="Deletes an existing planting location record by ID.",
        parameters=PLANTING_LOCATION_ID_PARAM,
        responses={
            204: PLANTING_LOCATION_DELETE_RESPONSE,
            404: PLANTING_LOCATION_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingLocationDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingLocationSerializer

    def get_queryset(self):
        return PlantingLocation.objects.filter(user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
