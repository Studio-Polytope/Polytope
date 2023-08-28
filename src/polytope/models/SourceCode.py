from dataclasses import dataclass
from enum import Enum, auto


class SourceCodeLanguage(Enum):
    """! Languages of source codes enumeration class."""

    # Unix shell bash.
    Bash = auto()
    # C11 (gcc)
    C11 = auto()
    # C++20 (g++)
    Cpp20 = auto()
    # Python3
    Python3 = auto()


@dataclass(kw_only=True)
class SourceCode:
    """! A source code dataclass."""

    """! Source code context."""
    context: str

    """! Source code langauge."""
    lang: SourceCodeLanguage
