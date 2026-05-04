import os

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


def validate_image_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png"]

    if ext not in valid_extensions:
        raise serializers.ValidationError(
            "Unsupported file extension. Please upload a " ".jpg or .png image."
        )

    filesize_limit = 2 * 1024 * 1024

    if value.size > filesize_limit:
        limit_mb = filesize_limit / (1024 * 1024)
        raise serializers.ValidationError(
            f"File too large. Size should not exceed {limit_mb}MB."
        )

    return value


@extend_schema_field({"type": "string", "format": "binary"})
class UploadableImageField(serializers.ImageField):
    pass


class UploadImageSerializer(serializers.ModelSerializer):
    image = UploadableImageField(
        required=True,
        help_text="Image file for this resource. Supported formats: JPG, PNG, GIF. Max size: 2MB",
    )

    def validate_image(self, value):
        return validate_image_file(value)
