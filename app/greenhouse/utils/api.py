from enum import Enum
from typing import Any, Mapping, Optional

from rest_framework.response import Response


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"
    FAIL = "fail"


# Format response data to JSend or at least something close to it
# Reference: https://github.com/omniti-labs/jsend
class CustomResponse(Response):  # type: ignore
    def __init__(  # type: ignore
        self,
        response_status: Optional[str] = "success",
        response_data: Optional[Mapping[str, Any]] = None,
        response_message: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the CustomResponse.

        :param Optional[str] response_status: The status of the response. Defaults to "success".
        :param Optional[Mapping[str, Any]] response_data: The data of the response. Defaults to None.
        :param Optional[str] response_message: The message of the response. Defaults to None.
        :param Any kwargs: Additional keyword arguments to pass to the Response.
        """
        formatted_data = {
            "status": Status(response_status).value,
            "data": response_data,
            "message": response_message,
        }

        super().__init__(formatted_data, **kwargs)


# Class for building the OpenAPI schema with the structure of JSend
# Reference: https://github.com/omniti-labs/jsend
class CustomOpenAPIResponseSchema:
    def __init__(
        self,
        response_status_example: str = "success",
        response_data_properties: Optional[Mapping[str, Any]] = None,
        response_message_example: Optional[str] = None,
        response_data_required_properties: Optional[list[str]] = None,
    ):
        """
        Initialize the CustomOpenAPIResponseSchema.

        :param str response_status_example: Example value for the 'status' field.
        :param Optional[Mapping[str, Any]] response_data_properties: Schema properties for the 'data' field.
        :param Optional[str] response_message_example: Example value for the 'message' field.
        :param Optional[list[str]] response_data_required_properties: List of required properties for the 'data' field.
        """
        self.response_status_example = Status(response_status_example).value
        self.response_data_properties = response_data_properties
        self.response_message_example = response_message_example
        self.response_data_required_properties = (
            response_data_required_properties
        )

    def get_schema(self) -> Mapping[str, Any]:
        """
        Get the OpenAPI schema for the response.

        :return: A dictionary representing the schema.
        :rtype: Mapping[str, Any]
        """
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The status of the API response, indicating success or failure.",
                    "example": self.response_status_example,
                },
                "data": {
                    "type": ["object", None],
                    "description": "An object containing the data returned by the API.",
                    **(
                        {"properties": self.response_data_properties}
                        if self.response_data_properties
                        else {}
                    ),
                    "required": self.response_data_required_properties,
                },
                "message": {
                    "type": ["string", None],
                    "description": "Optional message providing additional information about the response.",
                    "example": self.response_message_example,
                },
            },
            "required": ["status", "data", "message"],
        }
