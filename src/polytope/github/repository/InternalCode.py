from enum import Enum, auto


# TODO(TAMREF): Elaborate the reason of failure, referring to GitHub error message.
class GithubRepositoryInternalCode(Enum):
    """Internal status code of Github CRUD requests."""

    #: Success.
    Success = auto()
    #: Name attribute cannot be modified by creation.
    ForbiddenNameChangeOnCreation = auto()
    #: Failed to validate configuration.
    ConfigValidationFailed = auto()
    #: Creation failed on Github side.
    FailedToCreate = auto()
    #: Read failed on Github side.
    FailedToRead = auto()
    #: Creation (without template) failed on Github side.
    FailedToCreateWithoutTemplate = auto()
    #: Update failed on Github side.
    FailedToUpdate = auto()
    #: Deletion failed on Github side.
    FailedToDelete = auto()
    #: Cannot update repository without Polytope config file.
    UpdateWithoutPolytopeFile = auto()
    #: Cannot delete repository without Polytope config file.
    DeleteWithoutPolytopeFile = auto()
