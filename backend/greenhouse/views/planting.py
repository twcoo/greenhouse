from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Planting
from ..openapi.planting.examples import (
    CREATE_PLANTING_REQUEST_EXAMPLE, PARTIAL_UPDATE_PLANTING_REQUEST_EXAMPLE,
    UPDATE_PLANTING_REQUEST_EXAMPLE)
from ..openapi.planting.parameters import PLANTING_ID_PARAM
from ..openapi.planting.responses import (
    PLANTING_CREATE_VALIDATION_RESPONSE, PLANTING_CREATED_RESPONSE,
    PLANTING_DELETE_RESPONSE, PLANTING_LIST_RESPONSE,
    PLANTING_NOT_FOUND_RESPONSE, PLANTING_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    PLANTING_RETRIEVE_RESPONSE, PLANTING_UPDATE_RESPONSE,
    PLANTING_UPDATE_VALIDATION_RESPONSE)
from ..serializers import PlantingSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Planting"],
        summary="List plantings",
        description=(
            "Returns a paginated list of planting records associated "
            "with the currently authenticated user. Results are "
            "scoped per user."
        ),
        responses={
            200: PLANTING_LIST_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Planting"],
        summary="Create planting",
        description=(
            "Create a new planting record. The planting will "
            "automatically be associated with the authenticated user."
        ),
        examples=[CREATE_PLANTING_REQUEST_EXAMPLE],
        responses={
            201: PLANTING_CREATED_RESPONSE,
            400: PLANTING_CREATE_VALIDATION_RESPONSE,
        },
    ),
)
class PlantingListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    filter_backends = [SearchFilter]
    search_fields = ["crop__name", "variety__name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingSerializer

    def get_queryset(self):
        return Planting.objects.filter(user=self.request.user).prefetch_related(
            "locations__planting_location"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Planting"],
        summary="Retrieve a planting",
        description="Retrieve a single planting record by ID.",
        parameters=PLANTING_ID_PARAM,
        responses={
            200: PLANTING_RETRIEVE_RESPONSE,
            404: PLANTING_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Planting"],
        summary="Update a planting",
        description="Updates an existing planting record by ID.",
        parameters=PLANTING_ID_PARAM,
        examples=[UPDATE_PLANTING_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_UPDATE_RESPONSE,
            400: PLANTING_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Planting"],
        summary="Partially update a planting",
        description="Partially updates an existing planting record by ID.",
        parameters=PLANTING_ID_PARAM,
        examples=[PARTIAL_UPDATE_PLANTING_REQUEST_EXAMPLE],
        responses={
            200: PLANTING_UPDATE_RESPONSE,
            400: PLANTING_PARTIAL_UPDATE_VALIDATION_RESPONSE,
            404: PLANTING_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Planting"],
        summary="Delete a planting",
        description="Deletes an existing planting record by ID.",
        parameters=PLANTING_ID_PARAM,
        responses={
            204: PLANTING_DELETE_RESPONSE,
            404: PLANTING_NOT_FOUND_RESPONSE,
        },
    ),
)
class PlantingDetailApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingSerializer

    def get_queryset(self):
        return Planting.objects.filter(user=self.request.user).prefetch_related(
            "locations__planting_location"
        )

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
