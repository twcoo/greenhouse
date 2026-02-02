from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..schemas import RESOURCE_NOT_FOUND_RESPONSE, CustomOpenAPIResponseSchema
from ..serializers import CropSerializer
from ..utils.api import CustomAuthentication, CustomResponse

OPEN_API_NOT_FOUND_RESPONSE = OpenApiResponse(
    description="The requested crop does not exist.",
    response=CustomOpenAPIResponseSchema().get_schema(),
    examples=[
        OpenApiExample(
            name="Crop not found",
            summary="No crop exists with the provided ID.",
            description="Returned when a crop with the specified ID does not exist.",
            value=RESOURCE_NOT_FOUND_RESPONSE,
        )
    ],
)

OPEN_API_REQUIRED_FIELDS_EXAMPLE = OpenApiExample(
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
)


RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=CropSerializer,
    additional_required_data_fields=["id", "category", "sunlight_requirement"],
).get_schema()

OPEN_API_PARAMETERS = [
    OpenApiParameter(
        name="id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.PATH,
        description="Unique identifier of the crop.",
        required=True,
    )
]

OPEN_API_UPDATE_RESPONSE = OpenApiResponse(
    description="Crop updated successfully.",
    response=RESPONSE_DATA_SCHEMA,
    examples=[
        OpenApiExample(
            name="Crop Updated",
            summary="Crop updated successfully",
            description="Returned after the crop has been successfully updated.",
            value={
                "status": "success",
                "message": None,
                "data": {
                    "id": 34,
                    "name": "Tomato",
                    "scientific_name": "Solanum lycopersicum",
                    "category": "VEGETABLE",
                    "sunlight_requirement": "FULL SUN",
                    "min_days_to_harvest": 70,
                    "max_days_to_harvest": 90,
                },
            },
        )
    ],
)


@extend_schema_view(
    get=extend_schema(
        tags=["Crops"],
        summary="List crops",
        description="Retrieve all crop records.",
        responses={
            200: OpenApiResponse(
                description="List of crops retrieved successfully.",
                response=CustomOpenAPIResponseSchema(
                    data_serializer=CropSerializer(many=True),
                    additional_required_data_fields=[
                        "id",
                        "category",
                        "sunlight_requirement",
                    ],
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
        description="Create a new crop record.",
        responses={
            201: OpenApiResponse(
                description="Crop created successfully.",
                response=RESPONSE_DATA_SCHEMA,
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
                    OPEN_API_REQUIRED_FIELDS_EXAMPLE,
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
        parameters=OPEN_API_PARAMETERS,
        responses={
            200: OpenApiResponse(
                description="Crop retrieved successfully.",
                response=RESPONSE_DATA_SCHEMA,
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
            404: OPEN_API_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Crops"],
        summary="Update a crop",
        description="Updates an existing crop record by it's ID.",
        parameters=OPEN_API_PARAMETERS,
        responses={
            200: OPEN_API_UPDATE_RESPONSE,
            400: OpenApiResponse(
                description="Invalid request due to validation errors.",
                response=CustomOpenAPIResponseSchema().get_schema(),
                examples=[OPEN_API_REQUIRED_FIELDS_EXAMPLE],
            ),
            404: OPEN_API_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Crops"],
        summary="Partially update a crop",
        description="Partially updates an existing crop record identified by its ID.",
        parameters=OPEN_API_PARAMETERS,
        responses={
            200: OPEN_API_UPDATE_RESPONSE,
            404: OPEN_API_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Crops"],
        summary="Delete a crop",
        description="Deletes an existing crop record identified by its ID.",
        parameters=OPEN_API_PARAMETERS,
        responses={
            204: OpenApiResponse(
                description="Crop deleted successfully. No content is returned.",
            ),
            404: OPEN_API_NOT_FOUND_RESPONSE,
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
