from typing import Final


class Token:
    """The personal access token.

    Attributes:
        token (str): A read-only personal access token string.
    """

    def __init__(self, token: str) -> None:
        """Initialize the instance based on given token key.

        Args:
            token (str): A personal access token string.
        """
        assert 0 < len(token)

        self._token: Final[str] = token

    @property
    def token(self) -> str:
        """Return the Bearer token string."""
        return f"Bearer {self._token}"
