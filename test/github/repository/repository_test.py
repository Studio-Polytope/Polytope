import pytest
import requests
import json

from polytope.github.RequestVerb import RequestVerb as RV
from polytope.github.Session import MockSession
from polytope.github.Token import Token

from polytope.github.repository.Repository import GithubRepository
from polytope.github.repository.RepositoryConfig import GithubRepositoryConfig
from polytope.github.repository.InternalCode import GithubRepositoryInternalCode as GHIC

def get_test_repository():
    return GithubRepository(
        owner="test-owner",
        name="test_repo_name",
        token=Token("test_token"),
        session=MockSession
    )

def get_test_repository_with_full_response():
    repo = GithubRepository(
        owner="test-owner",
        name="test_repo_name",
        token=Token("test_token"),
        session=MockSession
    )

    def mock_request(verb: RV, url: str, **kwargs) -> requests.Response:
        resp = requests.Response()
        if (verb, url) == (RV.POST, repo._requester._base_url + repo.create_url):
            resp.status_code = 201
        if (verb, url) == (RV.POST, repo._requester._base_url + repo.create_without_template_url):
            resp.status_code = 201
        if (verb, url) == (RV.GET, repo._requester._base_url + repo.get_url):
            resp.status_code = 200
        if (verb, url) == (RV.PATCH, repo._requester._base_url + repo.update_url):
            resp.status_code = 200
        if (verb, url) == (RV.DELETE, repo._requester._base_url + repo.delete_url):
            resp.status_code = 204
        if (verb, url) == (RV.GET, repo._requester._base_url + repo.fetch_contents_url):
            resp.status_code = 200
            resp._content = json.dumps(
                [
                    {
                        "type": "file",
                        "name": "polytope.yaml"
                    }
                ]
            )

        return resp

    repo._requester._session.inject_request(mock_request)

    return repo

# Basic valid cases.

def test_create_repository():
    ghr = get_test_repository()
    assert ghr.create_url == '/repos/Studio-Polytope/Polytope-repository-template/generate'
    resp = ghr.create()
    assert resp.internal_code == GHIC.FailedToCreate

def test_create_repository_success():
    ghr = get_test_repository_with_full_response()
    resp = ghr.create()
    assert resp.status_code == 201
    assert resp.internal_code == GHIC.Success

def test_create_repository_without_template():
    ghr = get_test_repository()
    assert ghr.create_without_template_url == '/user/repos'
    resp = ghr.create_without_template()
    assert resp.internal_code == GHIC.FailedToCreateWithoutTemplate

def test_create_repository_without_template_success():
    ghr = get_test_repository_with_full_response()
    resp = ghr.create_without_template()
    assert resp.status_code == 201
    assert resp.internal_code == GHIC.Success

def test_update_repository():
    ghr = get_test_repository()
    assert ghr.update_url == '/repos/test-owner/test_repo_name'
    # bypass check polytope config file
    ghr._has_polytope_config_file = True

    upd_config = GithubRepositoryConfig("another_repo_name")
    resp = ghr.update(upd_config)
    # not changed, since update is failed
    assert ghr.update_url == '/repos/test-owner/test_repo_name'
    assert resp.internal_code == GHIC.FailedToUpdate

def test_update_repository_success():
    ghr = get_test_repository_with_full_response()
    # should succeed without bypass
    resp = ghr.update()
    assert resp.status_code == 200
    assert resp.internal_code == GHIC.Success

def test_delete_repository():
    ghr = get_test_repository()
    assert ghr.update_url == '/repos/test-owner/test_repo_name'
    ghr._has_polytope_config_file = True
    resp = ghr.delete()
    assert resp.internal_code == GHIC.FailedToDelete

def test_delete_repository_success():
    ghr = get_test_repository_with_full_response()
    # should succeed without bypass
    resp = ghr.delete()
    assert resp.status_code == 204
    assert resp.internal_code == GHIC.Success

# Invalid cases

def test_update_repository_with_invalid_config():
    ghr = get_test_repository()

    ghr._has_polytope_config_file = True

    upd_config = GithubRepositoryConfig(name="") # empty name: invalid config
    resp = ghr.update(upd_config)

    assert resp.internal_code == GHIC.ConfigValidationFailed

def test_update_repository_without_polytope_config():
    ghr = get_test_repository()

    resp = ghr.update()

    assert resp.internal_code == GHIC.UpdateWithoutPolytopeFile

    resp = ghr.delete()
    assert resp.internal_code == GHIC.DeleteWithoutPolytopeFile

# Error cases
def test_invalid_repo_init():
    # empty owner
    with pytest.raises(AssertionError):
        _ = GithubRepository("", "test_name", Token("test_token"), MockSession)

    # empty name
    with pytest.raises(AssertionError):
        _ = GithubRepository("test_owner", "", Token("test_token"), MockSession)

    # invalid owner name
    with pytest.raises(AssertionError):
        _ = GithubRepository("--o-o----o-", "test_name", Token("test_token"), MockSession)

    # invalid user name
    with pytest.raises(AssertionError):
        _ = GithubRepository("test-owner", "malicious/endpoint/like/user?name=kk", Token("test_token"), MockSession)
