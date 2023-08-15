import requests

from polytope.github import Token, RequestMethod
from polytope.github.Requester import RequesterDebugger


def test_auth_injection():
    token = Token('token-key-value')
    requester = RequesterDebugger(token, 'https://api.github.com')
    assert requester.session.headers['Authorization'] == token.token


def test_get_user_method():
    token = Token('token-key-value')

    def inject_method(
        method: RequestMethod,
        url: str,
        **kwargs,
    ) -> requests.Response:
        return requests.Response()

    requester = RequesterDebugger(token, 'https://api.github.com', inject_method)

    requester.request(RequestMethod.GET, '/user')

    assert 1 == len(requester.logs)

    log_entry = requester.logs[0]

    assert 'https://api.github.com/user' == log_entry.url
    assert RequestMethod.GET == log_entry.method
