from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The status of the API response.",
                    "example": "success",
                },
                "message": {
                    "type": ["string", "object", None],
                    "description": "Optional message or detail providing additional information about the response.",
                    "example": None,
                },
                "data": {
                    "description": "An object containing the data returned by the API.",
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "example": 1,
                            "description": "The total number of items available across all pages.",
                        },
                        "next": {
                            "type": "string",
                            "format": "uri",
                            "nullable": True,
                            "example": f"http://api.example.com/{settings.API_VERSION}/resources/?{self.page_query_param}=4",
                            "description": "URL of the next page of results, or null.",
                        },
                        "previous": {
                            "type": "string",
                            "format": "uri",
                            "nullable": True,
                            "example": f"http://api.example.com/{settings.API_VERSION}/resources/?{self.page_query_param}=2",
                            "description": "URL of the previous page of results, or null.",
                        },
                        "results": schema,
                    },
                    "required": [
                        "next",
                        "previous",
                        "count",
                        "results",
                    ],
                },
            },
            "required": ["status", "data", "message"],
        }
