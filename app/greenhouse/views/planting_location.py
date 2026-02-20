from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import PlantingLocation
from ..openapi.examples import (
    CREATE_PLANTING_LOCATION_REQUEST_GROUND_EXAMPLE,
    CREATE_PLANTING_LOCATION_REQUEST_POT_EXAMPLE)
from ..openapi.responses import (PLANTING_LOCATION_CREATE_VALIDATION_RESPONSE,
                                 PLANTING_LOCATION_CREATED_RESPONSE,
                                 PLANTING_LOCATION_LIST_RESPONSE)
from ..serializers import PlantingLocationSerializer
from ..utils.api import CustomAuthentication, CustomResponse


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
            "Create a new planting location record. The location will automatically "
            "be associated with the authenticated user."
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
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingLocationSerializer

    def get_queryset(self):
        return PlantingLocation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.list(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_200_OK
        )

    def post(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.create(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_201_CREATED
        )
