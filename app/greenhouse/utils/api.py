from enum import Enum

from knox.auth import TokenAuthentication


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"


class CustomAuthentication(TokenAuthentication):
    pass
