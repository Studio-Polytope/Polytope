from typing import Type, Optional, Dict

import requests
from polytope.github.RequestVerb import RequestVerb

from polytope.github.Session import RequestsSession, Session
from polytope.github.Token import Token


class Requester:
    """Wrap API requests.

    Attributes:
        session (Session):
            Used for API requests.
            Authorization and some other given headers are injected.
    """

    def __init__(
        self,
        token: Token,
        base_url: str,
        SessionClass: Type[Session] = RequestsSession,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the instance.

        Args:
            token (Token): A token for authorization.
            base_url (str): A non-empty base URL of API.
            SessionClass: A class to use for a session.
            headers (Dict[str, str], optional): Additional headers other than Authorization to fix in session.
        """
        assert 0 < len(base_url)

        self._token: Token = token
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
        """Wrap an API request with token authorization.

        Args:
            verb (RequestVerb): A HTTPS verb.
            api_url (str): A non-empty relative URL of API starting with '/'.
            **kwargs: Additional arguments for requesting.

        Returns:
            A response.
        """
        assert 0 < len(api_url)
        assert "/" == api_url[0]

        url: str = self._base_url + api_url
        return self._session.request(verb, url, **kwargs)

    @property
    def session(self) -> Session:
        return self._session
