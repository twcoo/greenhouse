from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Fertilizer
from ..openapi.fertilizer.examples import (
    CREATE_FERTILIZER_REQUEST_EXAMPLE,
    PARTIAL_UPDATE_FERTILIZER_REQUEST_EXAMPLE,
    UPDATE_FERTILIZER_REQUEST_EXAMPLE)
from ..openapi.fertilizer.parameters import FERTILIZER_ID_PARAM
from ..openapi.fertilizer.responses import (
    FERTILIZER_CREATE_VALIDATION_RESPONSE, FERTILIZER_CREATED_RESPONSE,
    FERTILIZER_DELETE_RESPONSE, FERTILIZER_LIST_RESPONSE,
    FERTILIZER_NOT_FOUND_RESPONSE,
    FERTILIZER_PARTIAL_UPDATE_VALIDATION_RESPONSE,
    FERTILIZER_RETRIEVE_RESPONSE, FERTILIZER_UPDATE_RESPONSE,
    FERTILIZER_UPDATE_VALIDATION_RESPONSE)
from ..serializers import FertilizerSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Fertilizer"],
        summary="List fertilizers",
        description=(
            "Returns a paginated list of fertilizer records associated "
            "with the currently authenticated user. Results are "
            "scoped per user."
        ),
        responses={
            200: FERTILIZER_LIST_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Fertilizer"],
        summary="Create fertilizer",
        description=(
            "Create a new fertilizer record. The fertilizer will "
            "automatically be associated with the authenticated user."
        ),
        examples=[CREATE_FERTILIZER_REQUEST_EXAMPLE],
        responses={
            201: FERTILIZER_CREATED_RESPONSE,
            400: FERTILIZER_CREATE_VALIDATION_RESPONSE,
        },
    ),
)
class FertilizerListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FertilizerSerializer

    def get_queryset(self):
        return Fertilizer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Fertilizer"],
        summary="Retrieve a fertilizer",
        description="Retrieve a single fertilizer record by ID.",
        parameters=FERTILIZER_ID_PARAM,
        responses={
            200: FERTILIZER_RETRIEVE_RESPONSE,
            404: FERTILIZER_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Fertilizer"],
        summary="Update a fertilizer",
        description="Updates an existing fertilizer record by ID.",
        parameters=FERTILIZER_ID_PARAM,
        examples=[UPDATE_FERTILIZER_REQUEST_EXAMPLE],
        responses={
            200: FERTILIZER_UPDATE_RESPONSE,
            400: FERTILIZER_UPDATE_VALIDATION_RESPONSE,
            404: FERTILIZER_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Fertilizer"],
        summary="Partially update a fertilizer",
        description="Partially updates an existing fertilizer record by ID.",
        parameters=FERTILIZER_ID_PARAM,
        examples=[PARTIAL_UPDATE_FERTILIZER_REQUEST_EXAMPLE],
        responses={
            200: FERTILIZER_UPDATE_RESPONSE,
            400: FERTILIZER_PARTIAL_UPDATE_VALIDATION_RESPONSE,
            404: FERTILIZER_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Fertilizer"],
        summary="Delete a fertilizer",
        description="Deletes an existing fertilizer record by ID.",
        parameters=FERTILIZER_ID_PARAM,
        responses={
            204: FERTILIZER_DELETE_RESPONSE,
            404: FERTILIZER_NOT_FOUND_RESPONSE,
        },
    ),
)
class FertilizerDetailApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FertilizerSerializer

    def get_queryset(self):
        return Fertilizer.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        fertilizer = serializer.instance
        ingredients = {
            item.casefold() for item in (fertilizer.ingredients or [])
        }
        log_added = list(fertilizer.log_added_ingredients or [])
        pruned = [item for item in log_added if item.casefold() in ingredients]
        if pruned != log_added:
            fertilizer.log_added_ingredients = pruned
            fertilizer.save(
                update_fields=["log_added_ingredients", "updated_at"]
            )

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
