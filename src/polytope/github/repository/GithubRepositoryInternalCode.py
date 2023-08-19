from enum import Enum, auto


class GithubRepositoryInternalCode(Enum):
    Success = auto()
    NullResponse = auto()
    ForbiddenNameChangeOnCreation = auto()
    ConfigValidationFailed = auto()