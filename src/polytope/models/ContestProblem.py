from dataclasses import dataclass

from .Problem import Problem


@dataclass(kw_only=True)
class ContestProblem:
    """! A Polytope contest's problem dataclass."""

    """! Problem index in the contest.

    * Every index in the same contest should be distinct.
    * It must be non-empty and alphanumeric.
    """
    index: str

    """! Actual problem context."""
    problem: Problem
