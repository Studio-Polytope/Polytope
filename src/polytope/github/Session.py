from requests.structures import CaseInsensitiveDict
from typing import Callable, List, Optional, Protocol
from polytope.github.RequestVerb import RequestVerb


import requests


from abc import ABC, abstractmethod, abstractproperty


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