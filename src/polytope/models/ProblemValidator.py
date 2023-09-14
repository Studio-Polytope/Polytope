from dataclasses import dataclass, field
from typing import Optional, List

from .ProblemValidatorTest import ProblemValidatorTest
from .SourceCode import SourceCode


@dataclass(kw_only=True)
class ProblemValidator:
    """A problem's validator."""

    #: Validator source code.
    code: Optional[SourceCode] = None

    #: Validator test scenarios.
    tests: List[ProblemValidatorTest] = field(default_factory=list)
