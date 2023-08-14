from typing import TYPE_CHECKING, Any, List, Callable
from enum import Enum, auto

import requests

if TYPE_CHECKING:
    from .Token import Token


class RequestMethod(str, Enum):
    """! HTTP methods enumeration class."""

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: List[Any],
    ) -> str:
        return name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class Requester:
    """! API request wrapper class."""

    def __init__(
        self,
        token: "Token",
        base_url: str,
    ):
        """! Requester class initializer.

        @param token    A token for authorization.
        @param base_url A base URL of API.
        """

        assert 0 < len(base_url)

        self._token: "Token" = token
        self._base_url: str = base_url

        self._session: requests.Session = requests.Session()
        self._session.headers['Authorization'] = self._token.token

    def request(
        self,
        method: RequestMethod,
        api_url: str,
        *args,
    ) -> requests.Response:
        """! API request wrapper with token authorization.

        @param method   A HTTPS method.
        @param api_url  A relative URL of API.
        @param *args    Additional arguments for requesting.

        @return  A response.
        """

        assert method in [
            RequestMethod.GET,
            RequestMethod.HEAD,
            RequestMethod.POST,
            RequestMethod.PUT,
            RequestMethod.DELETE,
            RequestMethod.PATCH,
        ]
        assert 0 < len(api_url)

        request_method: Callable[..., requests.Response] = getattr(self._session, method.lower())
        url: str = self._base_url + api_url

        return request_method(url, *args)
