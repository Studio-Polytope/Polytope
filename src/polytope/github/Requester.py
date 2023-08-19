from typing import TYPE_CHECKING, Type, Any, Optional, List, Callable, Protocol, Dict
from enum import Enum, auto
from abc import ABC, abstractmethod, abstractproperty

import requests
from requests.structures import CaseInsensitiveDict

"""This clause is only processed by mypy."""
if TYPE_CHECKING:
    from .Token import Token


class RequestVerb(str, Enum):
    """! HTTP verbs enumeration class."""

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


class Session(ABC):
    """! A request session class."""

    @abstractmethod
    def request(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """! Request method with token authorization.

        This method might be wrapped or injected.

        @param verb     A HTTPS verb.
        @param url      A full-path URL.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """
        ...

    @abstractproperty
    def headers(self):
        ...

    @headers.setter
    @abstractmethod
    def headers(self, value):
        ...


class RequestsSession(Session):
    """! A session class with requests session."""

    def __init__(self):
        """! RequestsSession class initializer."""

        self._session: requests.Session = requests.Session()

    def request(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """! Request method with token authorization.

        This method might be wrapped or injected.

        @param verb     A HTTPS verb.
        @param url      A full-path URL.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """

        assert verb in [
            RequestVerb.GET,
            RequestVerb.HEAD,
            RequestVerb.POST,
            RequestVerb.PUT,
            RequestVerb.DELETE,
            RequestVerb.PATCH,
        ]

        request_method: Callable[..., requests.Response] = getattr(self._session, verb.lower())
        return request_method(url, **kwargs)

    @property
    def headers(self):
        return self._session.headers

    @headers.setter
    def headers(self, value):
        self._session.headers = value


class MockSession(Session):
    """! A mock session class for testing."""

    def __init__(self):
        """! MockSession class initializer."""

        self._logs: List[MockSession.LogEntry] = []
        self._headers: CaseInsensitiveDict = CaseInsensitiveDict()
        self.inject_request()

    def inject_request(
        self,
        inject_method: Optional["MockSession.RequestMethodCallable"] = None,
    ):
        """! Inject a request method.

        @param inject_method    A request method to inject.
        """

        if inject_method is None:
            inject_method = self.__default_request
        self._inject_method = inject_method

    def request(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """! Request using injected method.

        @param verb     A HTTPS verb.
        @param url      A full-path URL.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """

        log_entry = self.LogEntry(verb, url, result=None, **kwargs)
        self._logs.append(log_entry)

        response = self._inject_method(verb, url, **kwargs)
        log_entry.result = response
        return response

    def __default_request(self, *args, **kwargs) -> requests.Response:
        return requests.Response()

    class RequestMethodCallable(Protocol):
        """! A protocol for request method injection."""

        def __call__(
            self,
            verb: RequestVerb,
            url: str,
            **kwargs,
        ) -> requests.Response:
            ...

    class LogEntry:
        """! Logging entry class."""

        def __init__(
            self,
            verb: RequestVerb,
            url: str,
            result: Optional[requests.Response],
            **kwargs,
        ):
            """! LogEntry class initializer.

            @param verb     A HTTPS verb.
            @param url      A full-path URL.
            @param result   A response result.
            @param **kwargs Additional arguments for requesting.
            """

            self.verb = verb
            self.url = url
            self.result = result
            self.kwargs = kwargs

        def __repr__(self):
            return (
                f"verb = {self.verb}, "
                f"url = '{self.url}', "
                f"kwargs = {self.kwargs}, "
                f"result = {self.result}"
            )

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @property
    def logs(self):
        return self._logs


class Requester:
    """! API request wrapper class."""

    def __init__(
        self,
        token: "Token",
        base_url: str,
        SessionClass: Type[Session] = RequestsSession,
        headers: Optional[Dict[str, str]] = None,
    ):
        """! Requester class initializer.

        @param token            A token for authorization.
        @param base_url         A base URL of API.
        @param SessionClass     A class to use for a session.
        @param headers          Additional headers other than Authorization to fix in session.
        """

        assert 0 < len(base_url)

        self._token: "Token" = token
        self._base_url: str = base_url

        self._session: Session = SessionClass()
        self._session.headers['Authorization'] = self._token.token

        if headers:
            for k, v in headers.items():
                if k.lower() == 'authorization':
                    continue
                self._session.headers[k] = v

    def request(
        self,
        verb: RequestVerb,
        api_url: str,
        **kwargs,
    ) -> requests.Response:
        """! API request wrapper with token authorization.

        @param verb     A HTTPS verb.
        @param api_url  A relative URL of API starting with '/'.
        @param **kwargs Additional arguments for requesting.

        @return  A response.
        """

        assert 0 < len(api_url)
        assert '/' == api_url[0]

        url: str = self._base_url + api_url
        return self._session.request(verb, url, **kwargs)

    @property
    def session(self):
        return self._session
