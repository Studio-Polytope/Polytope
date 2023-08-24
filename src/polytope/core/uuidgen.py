import random

# collision probability in 150,000 entries ~ 1%
# lowercase alphabet + digit except [l, 1, o, 0]
DEFAULT_ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"
DEFAULT_LENGTH = 8


class PolytopeUUID:
    """UUID generator class."""

    def __init__(
        self, alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH
    ):
        """! PolytopeUUID class initializer.

        @param alphabet     alphabet for generating uuid
        @param length       length of uuid
        """
        if len(alphabet) == 0:
            raise ValueError("alphabet must be a non-empty string.")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet must consist of distinct characters.")
        if length <= 0:
            raise ValueError("length must be positive.")

        self._alphabet = alphabet
        self._length = length

    @property
    def alphabet(self):
        """! An alphabet property for generating uuid."""
        return self._alphabet

    @property
    def length(self):
        """! A length property of uuid."""
        return self._length

    @alphabet.setter
    def alphabet(self, value: str):
        """! A getter method for alphabet property."""
        if len(value) == 0:
            raise ValueError("alphabet must be a non-empty string.")
        if len(set(value)) != len(value):
            raise ValueError("alphabet must consist of distinct characters.")

        self._alphabet = value

    @length.setter
    def length(self, value: int):
        """! A getter method for length property."""
        if value <= 0:
            raise ValueError("length must be positive.")

        self._length = value

    def uuid(self) -> str:
        """! A method for generating uuid."""
        char_list = [random.choice(self.alphabet) for _ in range(self.length)]
        return "".join(char_list)


def uuid(
    alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH
) -> str:
    generator = PolytopeUUID(alphabet, length)
    return generator.uuid()
