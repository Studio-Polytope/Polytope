from dataclasses import dataclass
from typing import Optional

import requests

@dataclass
class GithubRepositoryResponse:
    """
    Response template of Github Repository CRUD.
    @field status_code: HTTP code.
    @field internal_code: internal exit code.
    """
    status_code: Optional[int]
    internal_code: int
    error_msg: str
    errors: str