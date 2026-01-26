from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from ..models import Crop
from ..serializers import CropSerializer
from ..utils.api import CustomAuthentication, CustomResponse


class CropDetailAPIView(GenericAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CropSerializer

    queryset = Crop.objects.all()

    def get(self, request: Request) -> CustomResponse:
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return CustomResponse(
            response_data=serializer.data, status=status.HTTP_200_OK
        )
