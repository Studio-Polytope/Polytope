from enum import Enum, auto


class GithubRepositoryInternalCode(Enum):
    # Success.
    Success = auto()
    # create cannot modify repository name.
    ForbiddenNameChangeOnCreation = auto()
    # config validation failed.
    ConfigValidationFailed = auto()
    # creation failed on HTTP side.
    FailedToCreate = auto()