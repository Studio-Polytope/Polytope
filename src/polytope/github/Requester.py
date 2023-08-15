from typing import TYPE_CHECKING, Any, Optional, List, Callable, Protocol
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
        **kwargs,
    ) -> requests.Response:
        """! API request wrapper with token authorization.

        @param method   A HTTPS method.
        @param api_url  A relative URL of API.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """

        assert 0 < len(api_url)

        url: str = self._base_url + api_url
        return self._actual_request(method, url, **kwargs)

    def _actual_request(
        self,
        method: RequestMethod,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """! Request method with token authorization.

        This method might be wrapped or injected.

        @param method   A HTTPS method.
        @param url      A full-path URL.
        @param **kwargs Additional arguments for requesting.

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

        request_method: Callable[..., requests.Response] = getattr(self._session, method.lower())
        return request_method(url, **kwargs)


class RequestMethodCallable(Protocol):
    """! A protocol for request method injection."""

    def __call__(
        self,
        method: RequestMethod,
        url: str,
        **kwargs,
    ) -> requests.Response:
        ...


class RequesterDebugger(Requester):
    """! A class for debugging Requester class."""

    def __init__(
        self,
        token: "Token",
        base_url: str,
        inject_method: Optional[RequestMethodCallable] = None,
    ):
        """! Requester class initializer.

        @param token            A token for authorization.
        @param base_url         A base URL of API.
        @param inject_method    A request method to inject.
        """

        super().__init__(token, base_url)

        self._logs: List[RequesterDebugger.LogEntry] = []

        if inject_method is None:
            inject_method = super()._actual_request

        self._inject_method: RequestMethodCallable = inject_method

    def _actual_request(
        self,
        method: RequestMethod,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """! Wrapped request method.

        @param method   A HTTPS method.
        @param url      A full-path URL.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """

        log_entry = self.LogEntry(method, url, result=None, **kwargs)
        self._logs.append(log_entry)

        response = self._inject_method(method, url, **kwargs)
        log_entry.result = response

        return response

    class LogEntry:
        """! Logging entry class."""

        def __init__(
            self,
            method: RequestMethod,
            url: str,
            result: Optional[requests.Response],
            **kwargs,
        ):
            """! LogEntry class initializer.

            @param method   A HTTPS method.
            @param url      A full-path URL.
            @param result   A response result.
            @param **kwargs Additional arguments for requesting.
            """

            self.method = method
            self.url = url
            self.result = result
            self.kwargs = kwargs

        def __repr__(self):
            return (
                f"method = {self.method}, "
                f"url = '{self.url}', "
                f"kwargs = {self.kwargs}, "
                f"result = {self.result}"
            )

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def logs(self):
        return self._logs
