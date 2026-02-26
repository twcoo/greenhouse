from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


@extend_schema_field({"type": "string", "format": "binary"})
class UploadableImageField(serializers.ImageField):
    pass
