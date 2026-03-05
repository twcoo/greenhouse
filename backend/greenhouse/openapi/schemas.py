from typing import Any, Mapping, Optional, Type

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import serializers

from ..serializers import (CropSerializer, KnoxLoginResponseSerializer,
                           PlantingLocationImageSerializer,
                           PlantingLocationSerializer)
from ..utils.api import Status


# Class for building the OpenAPI schema with the structure of JSend
# Reference: https://github.com/omniti-labs/jsend
class CustomOpenAPIResponseSchema:
    def __init__(
        self,
        response_status_example: str = "success",
        data_serializer: Optional[Type[serializers.Serializer]] = None,
        response_message_example: Optional[Any] = None,
        additional_required_data_fields: Optional[list[str]] = [],
    ):
        self.response_status_example = Status(response_status_example).value
        self.data_serializer = data_serializer
        self.response_message_example = response_message_example
        self.additional_required_data_fields = additional_required_data_fields

    def _map_field(self, field: serializers.Field) -> dict[str, Any]:
        schema: dict[str, Any] = {}

        if isinstance(field, serializers.IntegerField):
            schema["type"] = "integer"
        elif isinstance(field, serializers.BooleanField):
            schema["type"] = "boolean"
        elif isinstance(field, serializers.FloatField):
            schema["type"] = "number"
        elif isinstance(field, serializers.ListField):
            schema["type"] = "array"
        elif isinstance(field, serializers.JSONField):
            schema["type"] = ["object", "string", None]
        elif isinstance(field, serializers.DateTimeField):
            schema["type"] = "string"
            schema["format"] = "date-time"
        elif isinstance(field, serializers.ImageField):
            schema["type"] = "string"
            schema["format"] = "uri"
        else:
            schema["type"] = "string"

        if field.help_text:
            schema["description"] = field.help_text

        return schema

    def _map_serializer_fields(
        self, serializer: serializers.BaseSerializer
    ) -> dict[str, Any]:
        properties = {}
        required = []

        for field_name, field in serializer.fields.items():
            properties[field_name] = self._map_field(field)

            if getattr(field, "required", False) or (
                self.additional_required_data_fields
                and field_name in self.additional_required_data_fields
            ):
                required.append(field_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def _serializer_to_schema(self) -> Mapping[str, Any]:
        if not self.data_serializer:
            return {}

        if isinstance(self.data_serializer, serializers.ListSerializer):
            return {
                "type": "array",
                "items": self._map_serializer_fields(
                    serializer=self.data_serializer.child
                ),
            }

        return self._map_serializer_fields(serializer=self.data_serializer())

    def get_schema(self) -> Mapping[str, Any]:
        data_schema = (
            self._serializer_to_schema()
            if self.data_serializer
            else {"type": ["object", None]}
        )

        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The status of the API response.",
                    "example": self.response_status_example,
                },
                "data": {
                    "description": "An object containing the data returned by the API.",
                    **data_schema,
                },
                "message": {
                    "type": ["string", "object", None],
                    "description": "Optional message or detail providing additional information about the response.",
                    "example": self.response_message_example,
                },
            },
            "required": ["status", "data", "message"],
        }


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "greenhouse.utils.api.CustomAuthentication"
    name = "AuthToken"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token authentication. Format: `Token <token>`",
        }


CROP_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=CropSerializer,
    additional_required_data_fields=["id", "category", "sunlight_requirement"],
).get_schema()

AUTH_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=KnoxLoginResponseSerializer,
).get_schema()

PLANTING_LOCATION_RESPONSE_DATA_SCHEMA = CustomOpenAPIResponseSchema(
    data_serializer=PlantingLocationSerializer,
).get_schema()

PLANTING_LOCATION_UPLOADED_IMAGE_RESPONSE_DATA_SCHEMA = (
    CustomOpenAPIResponseSchema(
        data_serializer=PlantingLocationImageSerializer,
    ).get_schema()
)
