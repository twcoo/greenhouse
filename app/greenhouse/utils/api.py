from enum import Enum
from typing import Any, Mapping, Optional

from knox.auth import TokenAuthentication
from rest_framework.response import Response


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"
    FAIL = "fail"


# Format response data to JSend or at least something close to it
# Reference: https://github.com/omniti-labs/jsend
class CustomResponse(Response):
    def __init__(
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


class CustomAuthentication(TokenAuthentication):
    pass
