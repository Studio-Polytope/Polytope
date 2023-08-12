from typing import List

from polytope.github import RequestMethod


def test_all_methods():
    testdata: List[RequestMethod, str] = [
        [RequestMethod.GET, 'GET'],
        [RequestMethod.HEAD, 'HEAD'],
        [RequestMethod.POST, 'POST'],
        [RequestMethod.PUT, 'PUT'],
        [RequestMethod.DELETE, 'DELETE'],
        [RequestMethod.PATCH, 'PATCH'],
    ]

    """Test list of all methods."""
    assert set([req for [req, _] in testdata])\
        == set([req for req in RequestMethod])

    """Test method name."""
    for [req, name] in testdata:
        assert req == name
