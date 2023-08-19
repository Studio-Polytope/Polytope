from dataclasses import dataclass
from typing import Optional
from .GithubRepositoryInternalCode import GithubRepositoryInternalCode

@dataclass
class GithubRepositoryResponse:
    """
    Response template of Github Repository CRUD.
    @field status_code: HTTP code.
    @field internal_code: internal exit code.
    """
    status_code: Optional[int]
    internal_code: GithubRepositoryInternalCode
    error_msg: str
    errors: str