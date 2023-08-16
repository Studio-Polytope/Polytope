

class Token:
    """! Personal access token class."""

    def __init__(self, token: str):
        """! Token class initializer.

        @param token    A personal access token string.
        """

        assert 0 < len(token)

        self._token: str = token

    @property
    def token(self) -> str:
        return 'Bearer ' + self._token
