import json
from dataclasses import asdict
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional, Tuple

import requests

from polytope.github import Requester, RequestVerb
from polytope.github.Requester import RequestsSession, Session

from .GithubRepositoryInternalCode import GithubRepositoryInternalCode as GHIC
from .RepositoryConfig import GithubRepositoryConfig
from .Response import GithubRepositoryResponse

# only for mypy.
if TYPE_CHECKING:
    from polytope.github import Token


def fetch_message_and_errors(result: requests.Response) -> Tuple[str, str]:
    dic = json.loads(result.content)

    if "message" in dic.keys() and "errors" in dic.keys():
        return (
            json.dumps(dic["message"]),
            json.dumps(dic["errors"])
        )
    
    return None, None


class GithubRepository:
    """
    Controller of Github Repository.
    @param token: Personal Access Token.
    @param owner: Github Username of Repository Owner.
    @param name: Name of the repository.
    """
    def __init__(
            self,
            owner: str,
            name: str,
            token: "Token",
            session: Session = RequestsSession
        ) -> None:
        
        self._requester = Requester(
            token=token,
            base_url=f"https://api.github.com",
            headers = {
                "Accept": "application/vnd.github+json",
                "X-Github-Api-Version": "2022-11-28",
            },
            SessionClass=session
        )
        self.owner : str = owner
        self.config : GithubRepositoryConfig = GithubRepositoryConfig(name)

    def create(
            self,
            description: str = "",
            private: bool = True
        ) -> GithubRepositoryResponse:
        """
        Creates a repository using our [template repository](https://github.com/Studio-Polytope/Polytope-repository-template)
        @param description: short repository description.
        @param private: true if repository needs to be kept private.
        """

        api_url = '/repos/Studio-Polytope/Polytope-repository-template/generate'
        data = {
            "owner": self.owner,
            "name": self.config.name,
            "description": description,
            "private": private,
            "include_all_branches": False, # constantly kept false to protect template
        }

        result = self._requester.request(
            RequestVerb.POST,
            api_url=api_url,
            data=json.dumps(data)
        )

        if result.status_code == 201:
            return GithubRepositoryResponse(
                status_code=result.status_code,
                internal_code=GHIC.Success,
                error_msg="",
                errors=""
            )
        else:
            msg, errors = fetch_message_and_errors(result)
            if (msg, errors) != (None, None):
                return GithubRepositoryResponse(
                    status_code=result.status_code,
                    internal_code=GHIC.FailedToCreate,
                    error_msg=msg,
                    errors=errors
                )
            else:
                # Leave errors non-parsed
                return GithubRepositoryResponse(
                    status_code=result.status_code,
                    internal_code=GHIC.FailedToCreate,
                    error_msg=bytes.decode(result.content),
                    errors=""
                )

    def create_without_template(
            self,
            config: Optional[GithubRepositoryConfig] = None
        ) -> GithubRepositoryResponse:
        """
        Creates a github repository. Not a first option to consider.
        Wraps [REST API for Github Repository](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user)
        @param config: overrides default configuration for repository. Cannot modify name here.
        """

        if config and config.validate():
            # For safety, we forbid changing name in create stage.
            if self.config.name != config.name:
                return GithubRepositoryResponse(
                    status_code=None,
                    internal_code=GHIC.ForbiddenNameChangeOnCreation,
                    error_msg="cannot modify name on creation step",
                    errors=""
                )
            
            self.config = config

        valid_config, validation_msg = self.config.validate()
        if not valid_config:
            return GithubRepositoryResponse(
                status_code=None,
                internal_code=GHIC.ConfigValidationFailed,
                error_msg=f'config validation failed while creation: "{validation_msg}"',
                errors=""
            )
        
        data = asdict(self.config)

        result = self._requester.request(
            verb=RequestVerb.POST,
            api_url='/user/repos',
            data=json.dumps(data)
        )

        # TODO post validation

        return GithubRepositoryResponse(
            status_code=result.status_code,
            internal_code=GHIC.Success,
            error_msg="",
            errors=""
        )
    
    def get(self):
        """
        Get a repository named {owner}/{repo}.
        """
        api_url = f'/repos/{self.owner}/{self.config.name}'
        result = self._requester.request(
            verb=RequestVerb.GET,
            api_url=api_url
        )

        # TODO post validation

        return GithubRepositoryResponse(
            status_code=result.status_code,
            internal_code=GHIC.Success,
            error_msg="",
            errors=""
        )
    
    def update(
            self,
            config: Optional[GithubRepositoryConfig] = None
        ):
        """
        Updates repository by config.
        @param config: GithubRepositoryConfig class. Includes name.
        """

        api_url = f'/repos/{self.owner}/{self.config.name}'
        if config and config.validate():
            self.config = config

        data = asdict(self.config)

        result = self._requester.request(
            verb=RequestVerb.PATCH,
            api_url=api_url,
            data=json.dumps(data)
        )

        # TODO post validation

        return GithubRepositoryResponse(
            status_code=result.status_code,
            internal_code=GHIC.Success,
            error_msg="",
            errors=""
        )
    
    def delete(self):
        """
        Deletes repository.
        """

        api_url = f'/repos/{self.owner}/{self.config.name}'
        result = self._requester.request(
            verb=RequestVerb.DELETE,
            api_url=api_url
        )

        # TODO post validation

        return GithubRepositoryResponse(
            status_code=result.status_code,
            internal_code=GHIC.Success,
            error_msg="",
            errors=""
        )