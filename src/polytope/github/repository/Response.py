from dataclasses import dataclass
from typing import Optional
from .InternalCode import GithubRepositoryInternalCode


@dataclass
class GithubRepositoryResponse:
    """! Response template of Github Repository CRUD.

    @field status_code: HTTP code.
    @field internal_code: internal exit code.
    """

    # HTTP status code. None if failed before HTTP request.
    status_code: Optional[int]
    # internal exit code.
    internal_code: GithubRepositoryInternalCode
    # error msg from HTTP response.
    error_msg: str
    # detailed errors.
    errors: str
