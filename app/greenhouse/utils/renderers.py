from typing import Any

from rest_framework.renderers import JSONRenderer

from .api import Status


# Format response data to JSend or at least something close to it
# Reference: https://github.com/omniti-labs/jsend
class JSendRenderer(JSONRenderer):
    def render(
        self,
        data,
        accepted_media_type: Any = None,
        renderer_context: Any = None,
    ):
        response = renderer_context.get("response")

        if response.status_code >= 400:
            res_status = Status.ERROR.value
        else:
            res_status = Status.SUCCESS.value

        message = None
        if isinstance(data, dict):
            message = data.pop("message", data.pop("detail", None))

            # If the response data is empty or contains a 'data' key with a None value,
            # ensure we normalize it to None.
            if not data or ("data" in data and data.get("data") is None):
                data = None

        formatted_data = {
            "status": res_status,
            "data": data,
            "message": message,
        }

        return super().render(formatted_data, accepted_media_type, renderer_context)
