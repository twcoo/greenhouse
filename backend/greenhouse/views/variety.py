from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Variety
from ..openapi.variety.examples import (CREATE_VARIETY_REQUEST_EXAMPLE,
                                        PARTIAL_UPDATE_VARIETY_REQUEST_EXAMPLE,
                                        UPDATE_VARIETY_REQUEST_EXAMPLE)
from ..openapi.variety.parameters import VARIETY_ID_PARAM
from ..openapi.variety.responses import (VARIETY_CREATE_VALIDATION_RESPONSE,
                                         VARIETY_CREATED_RESPONSE,
                                         VARIETY_DELETE_RESPONSE,
                                         VARIETY_LIST_RESPONSE,
                                         VARIETY_NOT_FOUND_RESPONSE,
                                         VARIETY_RETRIEVE_RESPONSE,
                                         VARIETY_UPDATE_RESPONSE,
                                         VARIETY_UPDATE_VALIDATION_RESPONSE)
from ..serializers import VarietySerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Variety"],
        summary="List varieties",
        description=(
            "Returns a paginated list of variety records associated "
            "with the currently authenticated user. Results are "
            "scoped per user."
        ),
        responses={
            200: VARIETY_LIST_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Variety"],
        summary="Create variety",
        description=(
            "Create a new variety record. The variety will "
            "automatically be associated with the authenticated user."
        ),
        examples=[CREATE_VARIETY_REQUEST_EXAMPLE],
        responses={
            201: VARIETY_CREATED_RESPONSE,
            400: VARIETY_CREATE_VALIDATION_RESPONSE,
        },
    ),
)
class VarietyListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = VarietySerializer

    def get_queryset(self):
        return Variety.objects.filter(crop__user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Variety"],
        summary="Retrieve a variety",
        description="Retrieve a single variety record by ID.",
        parameters=VARIETY_ID_PARAM,
        responses={
            200: VARIETY_RETRIEVE_RESPONSE,
            404: VARIETY_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Variety"],
        summary="Update a variety",
        description="Updates an existing variety record by ID.",
        parameters=VARIETY_ID_PARAM,
        examples=[UPDATE_VARIETY_REQUEST_EXAMPLE],
        responses={
            200: VARIETY_UPDATE_RESPONSE,
            400: VARIETY_UPDATE_VALIDATION_RESPONSE,
            404: VARIETY_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Variety"],
        summary="Partially update a variety",
        description=("Partially updates an existing variety record by ID."),
        parameters=VARIETY_ID_PARAM,
        examples=[PARTIAL_UPDATE_VARIETY_REQUEST_EXAMPLE],
        responses={
            200: VARIETY_UPDATE_RESPONSE,
            404: VARIETY_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Variety"],
        summary="Delete a variety",
        description="Deletes an existing variety record by ID.",
        parameters=VARIETY_ID_PARAM,
        responses={
            204: VARIETY_DELETE_RESPONSE,
            404: VARIETY_NOT_FOUND_RESPONSE,
        },
    ),
)
class VarietyDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = VarietySerializer

    def get_queryset(self):
        return Variety.objects.filter(crop__user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)
