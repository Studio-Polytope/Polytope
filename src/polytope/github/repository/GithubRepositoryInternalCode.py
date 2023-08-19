from enum import Enum, auto


class GithubRepositoryInternalCode(Enum):
    # Success.
    Success = auto()
    # create cannot modify repository name.
    ForbiddenNameChangeOnCreation = auto()
    # config validation failed.
    ConfigValidationFailed = auto()
    # creation failed on Github side.
    FailedToCreate = auto()
    # read failed on Github side.
    FailedToRead = auto()
    # creation (without template) failed on Github side.
    FailedToCreateWithoutTemplate = auto()
    # update failed on Github side.
    FailedToUpdate = auto()
    # deletion failed on Github side.
    FailedToDelete = auto()