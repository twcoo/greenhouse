from typing import Any

from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, extend_schema_view)
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from ..utils.api import CustomAuthentication, CustomResponse


@extend_schema_view(
    get=extend_schema(
        tags=["Crops"],
        summary="List crops",
        description=(
            "Retrieve all crops in the system. "
            "Each crop includes basic details such as `name` and `scientific_name`."
        ),
        responses={
            200: OpenApiResponse(
                description="List of crops retrieved successfully.",
                response=CustomOpenAPIResponseSchema(
                    data_serializer=CropSerializer(many=True)
                ).get_schema(),
                examples=[
                    OpenApiExample(
                        name="Crop list",
                        summary="List of all crops",
                        value={
                            "status": "success",
                            "message": None,
                            "data": [
                                {
                                    "id": 34,
                                    "name": "Tomato",
                                    "scientific_name": "Solanum lycopersicum",
                                    "category": "VEGETABLE",
                                    "sunlight_requirement": "FULL SUN",
                                    "min_days_to_harvest": 60,
                                    "max_days_to_harvest": 90,
                                }
                            ],
                        },
                    )
                ],
            ),
        },
    ),
    post=extend_schema(
        tags=["Crops"],
        summary="Create crop",
        description=(
            "Create a new crop record. "
            "Duplicate `name` and `scientific_name` combinations are not allowed."
        ),
        responses={
            201: OpenApiResponse(
                description="Crop created successfully.",
                response=CustomOpenAPIResponseSchema(
                    data_serializer=CropSerializer
                ).get_schema(),
                examples=[
                    OpenApiExample(
                        name="Crop created example",
                        summary="Successfully created crop",
                        description="Example response returned after a crop is successfully created.",
                        value={
                            "status": "success",
                            "message": None,
                            "data": {
                                "id": 34,
                                "name": "Tomato",
                                "scientific_name": "Solanum lycopersicum",
                                "category": "VEGETABLE",
                                "sunlight_requirement": "FULL SUN",
                                "min_days_to_harvest": 60,
                                "max_days_to_harvest": 90,
                            },
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="The request is invalid due to validation errors.",
                response=CustomOpenAPIResponseSchema().get_schema(),
                examples=[
                    OpenApiExample(
                        name="Duplicate crop record",
                        summary="Crop already exists",
                        description=(
                            "This response is returned when a crop with the same `name` and "
                            "`scientific_name` already exists in the database. "
                            "The request is rejected to maintain uniqueness."
                        ),
                        status_codes=["400"],
                        value={
                            "status": "error",
                            "data": None,
                            "message": {
                                "non_field_errors": ["Record already exist."]
                            },
                        },
                    ),
                    OpenApiExample(
                        name="Required field missing",
                        summary="Missing required fields",
                        description=(
                            "This response is returned when one or more required fields are missing "
                            "in the request payload."
                        ),
                        status_codes=["400"],
                        value={
                            "status": "error",
                            "data": None,
                            "message": {
                                "name": ["This field is required."],
                                "scientific_name": ["This field is required."],
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
