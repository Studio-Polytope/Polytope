from requests.structures import CaseInsensitiveDict
from typing import Any, Callable, cast, Dict, List, Optional, Protocol
from dataclasses import dataclass
from polytope.github.RequestVerb import RequestVerb

import requests

from abc import ABC, abstractmethod, abstractproperty


class RequestCallable(Protocol):
    """The request method protocol."""

    def __call__(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """Request given verb with token authorization.

        Args:
            verb (RequestVerb): A HTTPS verb.
            url (str): A full-path URL.
            **kwargs: Additional arguments for requesting.

        Returns:
            A response.
        """
        ...


class Session(ABC):
    """The request session interface."""

    @abstractproperty
    def request(self) -> RequestCallable:
        ...

    @abstractproperty
    def headers(self):
        ...

    @headers.setter
    @abstractmethod
    def headers(self, value) -> None:
        ...


class MockSession(Session):
    """Mock the session class for testing.

    Attributes:
        logs (List[MockSession.LogEntry]):
            A log list containing the argument values
            in order when the request method is called.
    """

    def __init__(self) -> None:
        self._logs: List[MockSession.LogEntry] = []
        self._headers: CaseInsensitiveDict = CaseInsensitiveDict()
        self.inject_request()

    def inject_request(
        self,
        inject_method: Optional[RequestCallable] = None,
    ) -> None:
        """Inject the given request method.

        Overwrite the injected method which is used for request.

        Args:
            inject_method (Optional[RequestCallable]):
                A request method to inject.
                If None, then use the default request method instead,
                which always returns None and does nothing.
                (default is None)
        """

        if inject_method is None:
            inject_method = cast(RequestCallable, self.__default_request)
        self._inject_method: RequestCallable = inject_method

    def request(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """Request using the injected method.

        Args:
            verb (RequestVerb): A HTTPS verb.
            url (str): A full-path URL.
            **kwargs: Additional arguments for requesting.

        Returns:
            A response.
        """

        log_entry: MockSession.LogEntry = self.LogEntry(
            verb, url, result=None, **kwargs
        )
        self._logs.append(log_entry)

        response: requests.Response = self._inject_method(verb, url, **kwargs)
        log_entry.result = response
        return response

    def __default_request(self, *args, **kwargs) -> requests.Response:
        return requests.Response()

    @dataclass()
    class LogEntry:
        """Log arguments and return value of the request method."""

        #: A HTTPS verb.
        verb: RequestVerb

        #: A full-path URL.
        url: str

        #: A response result.
        result: Optional[requests.Response]

        #: Additional arguments for requesting.
        kwargs: Dict[str, Any]

        def __repr__(self) -> str:
            return (
                f"verb = {self.verb}, "
                f"url = '{self.url}', "
                f"kwargs = {self.kwargs}, "
                f"result = {self.result}"
            )

    @property
    def headers(self) -> CaseInsensitiveDict:
        return self._headers

    @headers.setter
    def headers(self, value: CaseInsensitiveDict) -> None:
        self._headers = value

    @property
    def logs(self) -> List[LogEntry]:
        return self._logs


class RequestsSession(Session):
    """The session with requests module."""

    def __init__(self):
        self._session: requests.Session = requests.Session()

    def request(
        self,
        verb: RequestVerb,
        url: str,
        **kwargs,
    ) -> requests.Response:
        """Request given verb with token authorization.

        Args:
            verb (RequestVerb): A HTTPS verb.
            url (str): A full-path URL.
            **kwargs: Additional arguments for requesting.

        Returns:
            A response.
        """

        # Supported verbs.
        assert verb in [
            RequestVerb.GET,
            RequestVerb.HEAD,
            RequestVerb.POST,
            RequestVerb.PUT,
            RequestVerb.DELETE,
            RequestVerb.PATCH,
        ]

        request_method: Callable[..., requests.Response] = getattr(
            self._session, verb.lower()
        )
        return request_method(url, **kwargs)

    @property
    def headers(self):
        return self._session.headers

    @headers.setter
    def headers(self, value) -> None:
        self._session.headers = value
