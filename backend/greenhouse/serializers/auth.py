from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Enter a strong password (minimum 8 characters).",
    )
    password2 = serializers.CharField(
        write_only=True,
        help_text="Enter the same password again for confirmation.",
    )

    def validate(self, attrs):
        if User.objects.filter(is_superuser=True, is_staff=False).exists():
            raise serializers.ValidationError(
                "Admin user already exists. Setup cannot be run again."
            )

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Passwords do not match."}
            )

        return attrs

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            is_superuser=True,
            is_staff=False,
        )

        return user


class KnoxLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(
        help_text="Authentication token issued upon successful login or registration. "
    )
    expiry = serializers.DateTimeField(
        help_text="ISO 8601 timestamp indicating when the authentication token will expire."
    )


class KnoxLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, help_text="The username of the user trying to log in."
    )
    password = serializers.CharField(
        write_only=True, min_length=8, help_text="The password of the user."
    )
