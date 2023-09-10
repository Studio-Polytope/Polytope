from dataclasses import dataclass, field
from typing import Dict, List

from .ProblemStatement import ProblemStatement
from .ProblemChecker import ProblemChecker
from .ProblemValidator import ProblemValidator
from .ProblemTest import ProblemPublicTest, ProblemTest
from .ProblemSolution import ProblemSolution


@dataclass(kw_only=True)
class Problem:
    """! A Polytope problem dataclass."""

    """! Problem ID.

    * It must be auto-generated by using UUID.
    * It must be read-only.
    """
    _id: str

    """! Problem name.

    * It must be non-empty.
    """
    name: str

    """! Draft note for the problem."""
    note: str

    """! Time limit in milliseconds.

    * It must be positive.
    """
    time_limit_in_ms: int

    """! Memory limit in mebibytes.

    * It must be positive.
    """
    memory_limit_in_mib: int

    """! Problem tags.

    * Tags must be distinct.
    * Each tag must be non-empty.
    """
    tags: List[str]

    """! Problem owners.

    * Owners must be distinct.
    * Each owner must be non-empty.
    """
    owners: List[str]

    """! Problem statements.

    * Key is `ProblemStatment.lang`.
    """
    statements: Dict[str, ProblemStatement] = field(default_factory=dict)

    """! Problem checker."""
    checker: ProblemChecker

    """! Problem validator."""
    validator: ProblemValidator

    """! Public test data for statement."""
    public_tests: List[ProblemPublicTest] = field(default_factory=list)

    """! Secret test data for evaluation."""
    tests: List[ProblemTest] = field(default_factory=list)

    """! Problem solutions."""
    solutions: List[ProblemSolution] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self._id
