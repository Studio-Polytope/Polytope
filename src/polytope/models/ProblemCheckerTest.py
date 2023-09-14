from dataclasses import dataclass
from enum import Enum, auto


class ProblemCheckerVerdict(Enum):
    """Verdicts of problem checkers."""

    #: Output is correct.
    Correct = auto()
    #: Output is incorrect.
    Incorrect = auto()
    #: Output format is incorrect.
    PresentationError = auto()
    #: Checker crashes.
    Crashed = auto()
    #: Unsupported verdict or behavior.
    UnsupportedResult = auto()


@dataclass(kw_only=True)
class ProblemCheckerTest:
    """A test scenario of problem checker."""

    _id: str
    """Test ID.

    * It must be auto-generated by using UUID.
    * It must be read-only.
    """

    #: Input data.
    input: str

    #: Custom output data.
    output: str

    #: Correct output data.
    answer: str

    #: Expected verdict of checker.
    expected: ProblemCheckerVerdict

    @property
    def id(self) -> str:
        return self._id
