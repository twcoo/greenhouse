from typing import Any

from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, extend_schema_view)
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import (CropListResponseSerializer, CropResponseSerializer,
                           CropSerializer)
from ..utils.api import CustomAuthentication, CustomResponse


@extend_schema_view(
    get=extend_schema(
        tags=["Crops"],
        summary="List crops",
        description="Returns a list of crops.",
        responses={
            200: OpenApiResponse(
                response=CropListResponseSerializer, description="Success"
            ),
        },
    ),
    post=extend_schema(
        tags=["Crops"],
        summary="Create crop",
        description="Create a crop record.",
        responses={
            201: OpenApiResponse(
                response=CropResponseSerializer, description="Created"
            ),
            400: OpenApiResponse(
                description="Bad Request",
                response=CustomOpenAPIResponseSchema().get_schema(),
                examples=[
                    OpenApiExample(
                        name="Record already exist",
                        status_codes=["400"],
                        value={
                            "status": "error",
                            "data": None,
                            "message": {
                                "non_field_errors": ["Record already exist."]
                            },
                        },
                    ),
                ],
            ),
        },
    ),
)
class CropListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CropSerializer
    queryset = Crop.objects.all()

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


class CropDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CropSerializer
    queryset = Crop.objects.all()

    def get(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.retrieve(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_200_OK
        )

    def put(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.update(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_200_OK
        )

    def patch(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.partial_update(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_200_OK
        )

    def delete(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> CustomResponse:
        response = self.destroy(request, *args, **kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_204_NO_CONTENT
        )
