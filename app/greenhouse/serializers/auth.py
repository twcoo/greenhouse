from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
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
        write_only=True, help_text="The password of the user."
    )
