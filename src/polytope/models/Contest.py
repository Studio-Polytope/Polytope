from dataclasses import dataclass, field
from typing import List

from .ContestProblem import ContestProblem


@dataclass(kw_only=True)
class Contest:
    """! A Polytope contest dataclass."""

    """! Contest name."""
    name: str

    """! Contest problems."""
    problems: List[ContestProblem] = field(default_factory=list)
