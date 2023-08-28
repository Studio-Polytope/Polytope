from dataclasses import dataclass
from enum import Enum, auto


class SourceCodeLanguage(Enum):
    """! Languages of source codes enumeration class."""

    # Bash (Unix shell)
    Bash = auto()
    # Text (cat)
    Text = auto()
    # C11 (gcc)
    C11 = auto()
    # C++20 (g++)
    Cpp20 = auto()
    # Python3.10
    Python3_10 = auto()


@dataclass(kw_only=True)
class SourceCode:
    """! A source code dataclass."""

    """! Source code context."""
    context: str

    """! Source code langauge."""
    lang: SourceCodeLanguage
