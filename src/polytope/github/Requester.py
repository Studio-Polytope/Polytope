from typing import Type, Optional, Dict

import requests
from polytope.github.RequestVerb import RequestVerb

from polytope.github.Session import RequestsSession, Session
from polytope.github.Token import Token


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
        self._session.headers["Authorization"] = self._token.token

        if headers:
            for k, v in headers.items():
                if k.lower() == "authorization":
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
        assert "/" == api_url[0]

        url: str = self._base_url + api_url
        return self._session.request(verb, url, **kwargs)

    @property
    def session(self):
        return self._session
