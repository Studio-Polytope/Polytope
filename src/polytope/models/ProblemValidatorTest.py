from dataclasses import dataclass
from enum import Enum, auto


class ProblemValidatorVerdict(Enum):
    """! Verdicts of problem validators enumeration class."""

    # Input is valid.
    Valid = auto()
    # Input is invalid.
    Invalid = auto()
    # Validator crashes.
    Crashed = auto()
    # Unsupported verdict or behavior.
    UnsupportedResult = auto()


@dataclass(kw_only=True)
class ProblemValidatorTest:
    """! A test scenario of problem validator dataclass."""

    """! Test ID.

    * It must be auto-generated by using UUID.
    * It must be read-only.

    TODO: Set UUID generator as a default_factory.
    """
    _id: str

    """! Input data."""
    input: str

    """! Expected verdict of validator."""
    expected: ProblemValidatorVerdict
