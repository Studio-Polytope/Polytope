from dataclasses import dataclass


@dataclass(kw_only=True)
class ProblemStatement:
    """A problem statement."""

    #: Statement language.
    lang: str

    #: Statement context.
    context: str
