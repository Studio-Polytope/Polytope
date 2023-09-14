from dataclasses import dataclass, field
from typing import Optional, List

from .ProblemCheckerTest import ProblemCheckerTest
from .SourceCode import SourceCode


@dataclass(kw_only=True)
class ProblemChecker:
    """A problem's checker."""

    #: Checker source code.
    code: Optional[SourceCode] = None

    #: Checker test scenarios.
    tests: List[ProblemCheckerTest] = field(default_factory=list)
