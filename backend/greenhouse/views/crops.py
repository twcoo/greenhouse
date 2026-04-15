from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..openapi.crop.examples import (CREATE_CROP_REQUEST_EXAMPLE,
                                     CROP_UPLOAD_IMAGE_REQUEST_EXAMPLE,
                                     PARTIAL_UPDATE_CROP_REQUEST_EXAMPLE,
                                     UPDATE_CROP_REQUEST_EXAMPLE)
from ..openapi.crop.parameters import CROP_ID_PARAM
from ..openapi.crop.responses import (CROP_CREATE_VALIDATION_RESPONSE,
                                      CROP_CREATED_RESPONSE,
                                      CROP_DELETE_RESPONSE,
                                      CROP_IMAGE_UPLOAD_VALIDATION_RESPONSE,
                                      CROP_IMAGE_UPLOADED_RESPONSE,
                                      CROP_LIST_RESPONSE,
                                      CROP_NOT_FOUND_RESPONSE,
                                      CROP_PARTIAL_UPDATE_VALIDATION_RESPONSE,
                                      CROP_RETRIEVE_RESPONSE,
                                      CROP_UPDATE_RESPONSE,
                                      CROP_UPDATE_VALIDATION_RESPONSE)
from ..serializers import CropImageSerializer, CropSerializer
from ..utils.api import CustomAuthentication


@extend_schema_view(
    get=extend_schema(
        tags=["Crop"],
        summary="List crops",
        description=(
            "Returns a paginated list of crop records associated "
            "with the currently authenticated user. Results are "
            "scoped per user."
        ),
        responses={
            200: CROP_LIST_RESPONSE,
        },
    ),
    post=extend_schema(
        tags=["Crop"],
        summary="Create crop",
        description=(
            "Create a new crop record. The crop will automatically "
            "be associated with the authenticated user."
        ),
        examples=[
            CREATE_CROP_REQUEST_EXAMPLE,
        ],
        responses={
            201: CROP_CREATED_RESPONSE,
            400: CROP_CREATE_VALIDATION_RESPONSE,
        },
    ),
)
class CropListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    filter_backends = [SearchFilter]
    search_fields = ["name", "scientific_name"]
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CropSerializer

    def get_queryset(self):
        return Crop.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any):
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        tags=["Crop"],
        summary="Retrieve a crop",
        description="Retrieve a single crop record by ID.",
        parameters=CROP_ID_PARAM,
        responses={
            200: CROP_RETRIEVE_RESPONSE,
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    put=extend_schema(
        tags=["Crop"],
        summary="Update a crop",
        description="Updates an existing crop record by ID.",
        parameters=CROP_ID_PARAM,
        examples=[UPDATE_CROP_REQUEST_EXAMPLE],
        responses={
            200: CROP_UPDATE_RESPONSE,
            400: CROP_UPDATE_VALIDATION_RESPONSE,
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    patch=extend_schema(
        tags=["Crop"],
        summary="Partially update a crop",
        description="Partially updates an existing crop record by ID.",
        parameters=CROP_ID_PARAM,
        examples=[PARTIAL_UPDATE_CROP_REQUEST_EXAMPLE],
        responses={
            200: CROP_UPDATE_RESPONSE,
            400: CROP_PARTIAL_UPDATE_VALIDATION_RESPONSE,
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
    delete=extend_schema(
        tags=["Crop"],
        summary="Delete a crop",
        description="Deletes an existing crop record by ID.",
        parameters=CROP_ID_PARAM,
        responses={
            204: CROP_DELETE_RESPONSE,
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

    def get_queryset(self):
        return Crop.objects.filter(user=self.request.user)

    def get(self, request: Request, *args: Any, **kwargs: Any):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        return self.destroy(request, *args, **kwargs)


@extend_schema_view(
    put=extend_schema(
        tags=["Crop"],
        summary="Upload crop image",
        description="Upload crop image by ID.",
        parameters=CROP_ID_PARAM,
        examples=[CROP_UPLOAD_IMAGE_REQUEST_EXAMPLE],
        responses={
            200: CROP_IMAGE_UPLOADED_RESPONSE,
            400: CROP_IMAGE_UPLOAD_VALIDATION_RESPONSE,
            404: CROP_NOT_FOUND_RESPONSE,
        },
    ),
)
class CropUploadImageAPIView(mixins.UpdateModelMixin, GenericAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CropImageSerializer

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Crop.objects.filter(user=self.request.user)

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self.update(request, *args, **kwargs)
