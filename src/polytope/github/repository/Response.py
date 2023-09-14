from dataclasses import dataclass
from typing import Optional

from .InternalCode import GithubRepositoryInternalCode


@dataclass
class GithubRepositoryResponse:
    """Response template of Github Repository CRUD."""

    #: HTTP status code. `None` if failed before HTTP request.
    status_code: Optional[int]
    #: Internal exit code.
    internal_code: GithubRepositoryInternalCode
    #: Error message from HTTP response.
    error_msg: str
    #: Detailed errors.
    errors: str
