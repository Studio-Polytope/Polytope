import pytest

from polytope.github import Token


def test_empty_token():
    with pytest.raises(AssertionError):
        Token(token='')


def test_int_token():
    with pytest.raises(TypeError):
        Token(token=3)


def test_valid_token():
    key = 'eyJpc3MiOiJ2ZWxvcGVydC5jb20iLCJleHAiOiIxNDg1MjcwMDA'
    token = Token(token=key)
    assert ('Bearer %s' % key) == token.token


def test_length_one_token():
    token = Token('A')
    assert 'A' == token.token.split()[-1]


def test_token_readonly():
    token = Token('exampleTokenValue')

    with pytest.raises(AttributeError):
        token.token = 'anotherTokenValue'
