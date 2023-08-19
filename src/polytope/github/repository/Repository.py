from polytope.github import Requester, RequestVerb
from polytope.github.Requester import Session, RequestsSession
from typing import TYPE_CHECKING, Optional
from dataclasses import asdict
import requests
import json
from enum import Enum, auto
from polytope.github.repository import (
    GithubRepositoryResponse,
    GithubRepositoryConfig,
    GithubRepositoryInternalCode as GHIC
)

# only for mypy.
if TYPE_CHECKING:
    from polytope.github import Token





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
            config: Optional[GithubRepositoryConfig] = None
        ) -> GithubRepositoryResponse:
        """
        Creates a github repository.
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