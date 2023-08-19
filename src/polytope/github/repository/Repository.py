from polytope.github import Requester, RequestVerb
from polytope.github.Requester import Session, RequestsSession
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, asdict
import json

# only for mypy.
if TYPE_CHECKING:
    from polytope.github import Token


@dataclass
class GithubRepositoryConfig:
    name: str
    description: str = ""
    homepage: str = ""
    private: bool = True
    has_issues: bool = True
    has_projects: bool = True
    has_wiki: bool = True
    has_discussions: bool = True
    auto_init: bool = False
    gitignore_template: str = ""
    license_template: str = ""
    allow_squash_merge: bool = True
    allow_merge_commit: bool = True
    allow_rebase_merge: bool = True
    allow_auto_merge: bool = False
    delete_branch_on_merge: bool = False
    squash_merge_commit_title: str = "PR_TITLE"
    squash_merge_commit_message: str = "COMMIT_MESSAGES"
    merge_commit_title: str = "PR_TITLE"
    merge_commit_message: str = "PR_BODY"
    has_downloads: bool = True
    is_template: bool = False

    def validate(self) -> bool:
        # TODO : adopt github's own validation rules in advance
        if len(self.name) == 0:
            return False
        
        # validate squash commit combo
        squash_commit_combo = (self.squash_merge_commit_title, self.squash_merge_commit_message)
        if squash_commit_combo not in (
            ("PR_TITLE", "PR_BODY"),
            ("PR_TITLE", "BLANK"),
            ("PR_TITLE", "COMMIT_MESSAGES"),
            ("COMMIT_OR_PR_TITLE", "COMMIT_MESSAGES"),
        ):
            print(squash_commit_combo, "is not valid")
            return False

        return True
        return len(self.name) > 0

"""
Controller of Github Repository.
"""
class GithubRepository:
    """
    Initializer of Github Repository.
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
        ):
        """
        Creates a github repository.
        Wraps [REST API for Github Repository](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user)
        @param config: overrides default configuration for repository. Cannot modify name here.
        """

        if config and config.validate():
            # For safety, we forbid changing name in create stage.
            if self.config.name != config.name:
                # TODO clarify error
                return None
            
            self.config = config

        if not self.config.validate():
            print("Die")
            # TODO clarify error
            return None
        
        data = asdict(self.config)

        result = self._requester.request(
            verb=RequestVerb.POST,
            api_url='/user/repos',
            data=json.dumps(data)
        )

        # TODO: refine return structure
        return result
    
    def get(self):
        """
        Get a repository named {owner}/{repo}.
        """
        api_url = f'/repos/{self.owner}/{self.config.name}'
        result = self._requester.request(
            verb=RequestVerb.GET,
            api_url=api_url
        )

        return result
    
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

        return result
    
    def delete(self):
        """
        Deletes repository.
        """

        api_url = f'/repos/{self.owner}/{self.config.name}'
        result = self._requester.request(
            verb=RequestVerb.DELETE,
            api_url=api_url
        )

        return result