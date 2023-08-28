import json
from dataclasses import asdict
from typing import Optional, Tuple, Type
from typing_extensions import assert_type

import re
import requests

from polytope.github import Requester
from polytope.github.RequestVerb import RequestVerb
from polytope.github.Session import RequestsSession
from polytope.github.Session import Session
from polytope.github.Token import Token

from .InternalCode import GithubRepositoryInternalCode as GHIC
from .RepositoryConfig import GithubRepositoryConfig
from .Response import GithubRepositoryResponse


# Alphanumeric or hyphen, starts & ends with alphanumeric
GITHUB_USERNAME_REGEX = r"^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,37}[a-zA-Z\d]$"
# Alphanumeric, hyphen, underscore. starts & ends with alphanumeric.
GITHUB_REPONAME_REGEX = r"^[a-z0-9]+(?:(?:(?:[._]|__|[-]*)[a-z0-9]+)+)?$"


class GithubRepository:
    """Control a GitHub Repository.

    Attributes:
        owner (str): Github Username of Repository Owner.
        config (GithubRepositoryConfig): Repository configurations.
    """

    def __init__(
        self,
        owner: str,
        name: str,
        token: Token,
        session_cls: Type[Session] = RequestsSession,
    ) -> None:
        """Initialize the instance.

        Args:
            owner (str): Github Username of Repository Owner.
            name (str): Name of the repository.
            token (Token): Personal Access Token.
            session_cls: Type of session.
        """
        assert 0 < len(owner)
        assert is_valid_github_user_name(owner)
        assert 0 < len(name)
        assert is_valid_github_repository_name(name)

        self._requester: Requester = Requester(
            token=token,
            base_url="https://api.github.com",
            headers={
                "Accept": "application/vnd.github+json",
                "X-Github-Api-Version": "2022-11-28",
            },
            SessionClass=session_cls,
        )

        self.owner: str = owner
        self.config: GithubRepositoryConfig = GithubRepositoryConfig(name)
        self._has_polytope_config_file: Optional[bool] = None

    @property
    def create_url(self) -> str:
        """URL for repository creation."""
        return "/repos/Studio-Polytope/Polytope-repository-template/generate"

    def create(
        self, description: str = "", private: bool = True
    ) -> GithubRepositoryResponse:
        """Create a repository using our template repository.

        See the template repository at
        https://github.com/Studio-Polytope/Polytope-repository-template

        Args:
            description (str, optional): Short repository description.
            private (bool): `True` if repository needs to be kept private. (Default is `True`.)
        """
        api_url: str = self.create_url
        data = {
            "owner": self.owner,
            "name": self.config.name,
            "description": description,
            "private": private,
            "include_all_branches": False,  # Constantly kept false to protect template
        }

        result = self._requester.request(
            RequestVerb.POST, api_url=api_url, data=json.dumps(data)
        )

        if result.status_code == 201:
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors="",
            )
        else:
            return post_process_error_response(result, GHIC.FailedToCreate)

    @property
    def create_without_template_url(self) -> str:
        return "/user/repos"

    def create_without_template(
        self, config: Optional[GithubRepositoryConfig] = None
    ) -> GithubRepositoryResponse:
        """Create a github repository.

        Not a first option to consider.

        Wrap REST API for Github Repository. See details at
        https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user

        Args:
            config (optional): Override default configuration for repository. Cannot modify name here.
        """
        if config is None:
            config = self.config

        valid_config, validation_msg = config.validate()
        assert_type(valid_config, bool)
        assert_type(validation_msg, str)

        if not valid_config:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.ConfigValidationFailed,
                error_msg=f'config validation failed while creation: "{validation_msg}"',
                errors="",
            )

        # For safety, we forbid changing name in create stage.
        if self.config.name != config.name:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.ForbiddenNameChangeOnCreation,
                error_msg="cannot modify name on creation step",
                errors="",
            )

        data = asdict(config)

        result = self._requester.request(
            verb=RequestVerb.POST,
            api_url=self.create_without_template_url,
            data=json.dumps(data),
        )

        if result.status_code == 201:
            self.config = config
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors="",
            )
        else:
            return post_process_error_response(
                result, GHIC.FailedToCreateWithoutTemplate
            )

    @property
    def get_url(self) -> str:
        """URL to get repository info."""
        return f"/repos/{self.owner}/{self.config.name}"

    def get(self) -> GithubRepositoryResponse:
        """Get a repository named {owner}/{repo}."""
        result = self._requester.request(verb=RequestVerb.GET, api_url=self.get_url)

        # TODO(TAMREF): Define content to read

        if result.status_code == 200:
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors="",
            )
        else:
            return post_process_error_response(result, GHIC.FailedToRead)

    @property
    def update_url(self) -> str:
        """URL for update."""
        return f"/repos/{self.owner}/{self.config.name}"

    def update(
        self, config: Optional[GithubRepositoryConfig] = None
    ) -> GithubRepositoryResponse:
        """Update repository by `config`.

        Args:
            config: GithubRepositoryConfig class. Includes name.
        """

        has_polytope_config_file, reason = self.fetch_polytope_config_file()
        assert_type(has_polytope_config_file, bool)
        assert_type(reason, str)

        if not has_polytope_config_file:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.UpdateWithoutPolytopeFile,
                error_msg=reason,
                errors="",
            )

        if config is None:
            config = self.config

        valid_config, validation_result = config.validate()
        assert_type(valid_config, bool)
        assert_type(validation_result, str)

        if not valid_config:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.ConfigValidationFailed,
                error_msg=f'config for update is invalid: "{validation_result}"',
                errors="",
            )

        data = asdict(config)

        result = self._requester.request(
            verb=RequestVerb.PATCH,
            api_url=self.update_url,
            data=json.dumps(data),
        )

        # Succeeded to update.
        if result.status_code == 200:
            # Update local config only if update is succeeded.
            self.config = config
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors="",
            )
        else:
            return post_process_error_response(result, GHIC.FailedToUpdate)

    @property
    def delete_url(self) -> str:
        """URL for delete."""
        return f"/repos/{self.owner}/{self.config.name}"

    def delete(self) -> GithubRepositoryResponse:
        """Delete the repository."""
        has_polytope_config_file, reason = self.fetch_polytope_config_file()
        assert_type(has_polytope_config_file, bool)
        assert_type(reason, str)

        if not has_polytope_config_file:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.DeleteWithoutPolytopeFile,
                error_msg=reason,
                errors="",
            )

        result = self._requester.request(
            verb=RequestVerb.DELETE, api_url=self.delete_url
        )

        # Succeeded to update.
        if result.status_code == 204:
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors="",
            )
        else:
            return post_process_error_response(result, GHIC.FailedToDelete)

    @property
    def fetch_contents_url(self) -> str:
        """URL to fetch contents."""
        return f"/repos/{self.owner}/{self.config.name}/contents"

    # Fetch Polytope config file (polytope.yaml)
    def fetch_polytope_config_file(
        self, ignore_cache: bool = False
    ) -> Tuple[bool, str]:
        """Fetch Polytope config file (currently `polytope.yaml`).

        Args:
            ignore_cache: If set to `False`, use cached value instead of sending requests.

        Returns:
            tuple: A tuple containing:
                * (bool): Existence of Polytope config file.
                * (str): Reason message.
        """

        # believe cached result
        if self._has_polytope_config_file is not None and not ignore_cache:
            return self._has_polytope_config_file, "cached response"

        # clear cache
        self._has_polytope_config_file = None

        result = self._requester.request(
            verb=RequestVerb.GET, api_url=self.fetch_contents_url
        )

        if result.status_code == 200:
            (
                self._has_polytope_config_file,
                reason,
            ) = parse_polytope_config_file(result.content)
            return self._has_polytope_config_file, reason

        else:
            self._has_polytope_config_file = False
            return self._has_polytope_config_file, "unsuccessful response"


# Utility functions


def is_valid_github_repository_name(name: str) -> bool:
    return re.match(GITHUB_REPONAME_REGEX, name) is not None


def is_valid_github_user_name(name: str) -> bool:
    return re.match(GITHUB_USERNAME_REGEX, name) is not None


def fetch_message_and_errors(
    result: requests.Response,
) -> Tuple[str, str] | Tuple[None, None]:
    """Post-processor of erroneous request.Response."""
    if not result.content:
        return None, None

    # TODO handle error while decoding json
    dic = json.loads(result.content)

    if not isinstance(dic, dict):
        return None, None

    if "message" in dic.keys() and "errors" in dic.keys():
        return (json.dumps(dic["message"]), json.dumps(dic["errors"]))

    return None, None


def parse_polytope_config_file(
    resp_content: str | bytes | bytearray | None,
) -> Tuple[bool, str]:
    """Parse http response content from Github root directory.

    Args:
        resp_content: Content of http response.

    Returns:
        tuple: A tuple containing:
            * (bool): Whether if there is a Polytope config file.
            * (str): Error message while finding configs.
    """
    if not resp_content:
        return False, "empty response content"

    # TODO(TAMREF): Error handling while json unmarshal
    contents = json.loads(resp_content)

    if not isinstance(contents, list):
        return False, "non-list response for contents"

    sanity = (
        lambda content: isinstance(content, dict)
        and content["type"] == "file"
        and content["name"] == "polytope.yaml"
    )
    contents = list(filter(sanity, contents))

    if len(contents) > 0:
        return True, "detected polytope.yaml file"
    else:
        return False, "could not detect polytope.yaml file"


def post_process_error_response(
    result: requests.Response, code: GHIC
) -> GithubRepositoryResponse:
    msg, errors = fetch_message_and_errors(result)
    if (msg, errors) != (None, None):
        assert msg is not None
        assert errors is not None
        return GithubRepositoryResponse(
            status_code=result.status_code,
            internal_code=code,
            error_msg=msg,
            errors=errors,
        )
    else:
        return _make_unparsed_error_response(result, code)


# Translate http response to github response, when we failed to parse it.
def _make_unparsed_error_response(
    result: requests.Response, code: GHIC
) -> GithubRepositoryResponse:
    # Leave errors unparsed
    error_msg = ""
    if result.content:
        error_msg = bytes.decode(result.content)

    return GithubRepositoryResponse(
        status_code=result.status_code,
        internal_code=code,
        error_msg=error_msg,
        errors="",
    )
