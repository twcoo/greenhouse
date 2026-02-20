from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import PlantingLocation
from ..serializers import PlantingLocationSerializer
from ..utils.api import CustomAuthentication, CustomResponse


# @extend_schema_view(
#     get=extend_schema(
#         tags=["Crops"],
#         summary="List crops",
#         description="Retrieve all crop records.",
#         responses={
#             200: CROP_LIST_RESPONSE,
#         },
#     ),
#     post=extend_schema(
#         tags=["Crops"],
#         summary="Create crop",
#         description="Create a new crop record.",
#         examples=[
#             CREATE_CROP_REQUEST_EXAMPLE,
#         ],
#         responses={
#             201: CROP_CREATED_RESPONSE,
#             400: CROP_CREATE_VALIDATION_RESPONSE,
#         },
#     ),
# )
class PlantingLocationListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlantingLocationSerializer
    # queryset = PlantingLocation.objects.all()

    def get_queryset(self):
        return PlantingLocation.objects.filter(user=self.request.user)

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
