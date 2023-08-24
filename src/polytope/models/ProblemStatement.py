from dataclasses import dataclass


@dataclass
class ProblemStatement:
    """! A problem statement dataclass."""

    """! Statement language."""
    lang: str

    """! Statement context."""
    context: str
