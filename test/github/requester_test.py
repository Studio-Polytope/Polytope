import pytest

from polytope.github import Token, RequestMethod, Requester
from polytope.github.Requester import MockSession


def test_auth_injection():
    token = Token('token-key-value')
    requester = Requester(token, 'https://api.github.com', MockSession)
    session: MockSession = requester.session
    assert session.headers['Authorization'] == token.token


def test_invalid_api_url():
    token = Token('token-key-value')
    requester = Requester(token, 'https://api.github.com')

    with pytest.raises(AssertionError):
        requester.request(RequestMethod.GET, 'user')


def test_get_user_method():
    token = Token('token-key-value')
    requester = Requester(token, 'https://api.github.com', MockSession)
    requester.request(RequestMethod.GET, '/user')

    session: MockSession = requester.session

    assert 1 == len(session.logs)

    log_entry = session.logs[0]
    assert 'https://api.github.com/user' == log_entry.url
    assert RequestMethod.GET == log_entry.method
