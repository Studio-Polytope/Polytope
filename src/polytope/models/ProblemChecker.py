from dataclasses import dataclass, field
from typing import Optional, List

from .ProblemCheckerTest import ProblemCheckerTest
from .SourceCode import SourceCode


@dataclass
class ProblemChecker:
    """! A problem's checker dataclass."""

    """! Checker source code."""
    code: Optional[SourceCode] = None

    """! Checker test scenarios."""
    tests: List[ProblemCheckerTest] = field(default_factory=list)
