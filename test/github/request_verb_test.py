from typing import List

from polytope.github import RequestVerb


def test_all_verbs():
    testdata: List[RequestVerb, str] = [
        [RequestVerb.GET, 'GET'],
        [RequestVerb.HEAD, 'HEAD'],
        [RequestVerb.POST, 'POST'],
        [RequestVerb.PUT, 'PUT'],
        [RequestVerb.DELETE, 'DELETE'],
        [RequestVerb.PATCH, 'PATCH'],
    ]

    """Test list of all methods."""
    assert set([req for [req, _] in testdata])\
        == set([req for req in RequestVerb])

    """Test method name."""
    for [req, name] in testdata:
        assert req == name
