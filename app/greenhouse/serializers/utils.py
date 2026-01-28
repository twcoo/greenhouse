from rest_framework import serializers


class CustomReponseSerializer(serializers.Serializer):
    status = serializers.CharField(
        default="success",
        help_text="The status of the API response, indicating success or failure.",
    )
    message = serializers.CharField(
        allow_null=True,
        required=False,
        help_text="Optional message providing additional information about the response.",
    )
    data = serializers.JSONField(
        help_text="An object containing the data returned by the API."
    )
