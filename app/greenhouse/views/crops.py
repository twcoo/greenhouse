from typing import Any

from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..serializers import CropSerializer
from ..utils.api import CustomAuthentication, CustomResponse


class CropDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CropSerializer
    queryset = Crop.objects.all()

    def get(self, request: Request, *args: Any, **kwargs: Any) -> CustomResponse:
        if "pk" in self.kwargs:
            response = self.retrieve(request, *args, **kwargs)
        else:
            response = self.list(request, *args, **kwargs)

        return CustomResponse(response_data=response.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> CustomResponse:
        response = self.create(request, args, kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_201_CREATED
        )

    def put(self, request: Request, *args: Any, **kwargs: Any) -> CustomResponse:
        response = self.update(request, args, kwargs)

        return CustomResponse(response_data=response.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> CustomResponse:
        response = self.partial_update(request, args, kwargs)

        return CustomResponse(response_data=response.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> CustomResponse:
        response = self.destroy(request, args, kwargs)

        return CustomResponse(
            response_data=response.data, status=status.HTTP_204_NO_CONTENT
        )
