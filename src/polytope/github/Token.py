

class Token():
    """
    Personal Access Token
    """

    def __init__(self, token: str):
        assert isinstance(token, str)
        assert 0 < len(token)

        self._token = token

    @property
    def token(self) -> str:
        return self._token
