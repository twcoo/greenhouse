from typing import Any

from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, extend_schema_view)
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..openapi.examples import (CREATE_CROP_REQUEST_EXAMPLE,
                                CROP_REQUIRED_FIELDS_EXAMPLE)
from ..openapi.parameters import CROP_ID_PARAM
from ..openapi.responses import CROP_NOT_FOUND_RESPONSE, CROP_UPDATE_RESPONSE
from ..openapi.schemas import CROP_RESPONSE_DATA_SCHEMA
from ..schemas import CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from ..utils.api import CustomAuthentication, CustomResponse


@extend_schema_view(
    get=extend_schema(
        tags=["Crops"],
        summary="List crops",
        description="Retrieve all crop records.",
        responses={
            200: OpenApiResponse(
                description="List of crops retrieved successfully.",
                response=CropSerializer,
            ),
        },
    ),
    post=extend_schema(
        tags=["Crops"],
        summary="Create crop",
        description="Create a new crop record.",
        examples=[
            CREATE_CROP_REQUEST_EXAMPLE,
        ],
        responses={
            201: OpenApiResponse(
                description="Crop created successfully.",
                response=CROP_RESPONSE_DATA_SCHEMA,
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
                description="Invalid request due to validation errors.",
                response=CustomOpenAPIResponseSchema().get_schema(),
                examples=[
                    OpenApiExample(
                        name="Duplicate crop record",
                        summary="Crop already exists",
                        description="This response is returned when a duplicate record already exists.",
                        status_codes=["400"],
                        value={
                            "status": "error",
                            "data": None,
                            "message": {
                                "non_field_errors": [
                                    "A crop with the same name and scientific name already exists."
                                ]
                            },
                        },
                    ),
                    CROP_REQUIRED_FIELDS_EXAMPLE,
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


@extend_schema_view(
    get=extend_schema(
        tags=["Crops"],
        summary="Retrieve a crop",
        description="Retrieve a single crop record by it's ID.",
        parameters=CROP_ID_PARAM,
        responses={
            200: OpenApiResponse(
                description="Crop retrieved successfully.",
                response=CROP_RESPONSE_DATA_SCHEMA,
                examples=[
                    OpenApiExample(
                        name="Crop detail",
                        summary="Retrieve a crop by ID",
                        description="Returns the details of a crop identified by the provided ID.",
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
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Crops"],
        summary="Update a crop",
        description="Updates an existing crop record by it's ID.",
        parameters=CROP_ID_PARAM,
        responses={
            200: CROP_UPDATE_RESPONSE,
            400: OpenApiResponse(
                description="Invalid request due to validation errors.",
                response=CustomOpenAPIResponseSchema().get_schema(),
                examples=[CROP_REQUIRED_FIELDS_EXAMPLE],
            ),
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Crops"],
        summary="Partially update a crop",
        description="Partially updates an existing crop record identified by its ID.",
        parameters=CROP_ID_PARAM,
        responses={
            200: CROP_UPDATE_RESPONSE,
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Crops"],
        summary="Delete a crop",
        description="Deletes an existing crop record identified by its ID.",
        parameters=CROP_ID_PARAM,
        responses={
            204: OpenApiResponse(
                description="Crop deleted successfully. No content is returned.",
            ),
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
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
