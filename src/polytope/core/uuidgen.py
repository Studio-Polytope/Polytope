import random

# collision probability in 150,000 entries ~ 1%
# lowercase alphabet + digit except [l, 1, o, 0]
DEFAULT_ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"
DEFAULT_LENGTH = 8


class PolytopeUUID:
    """UUID generator class."""

    def __init__(self, alphabet: str = None, length: int = 0):
        """! PolytopeUUID class initializer.

        @param alphabet     alphabet for generating uuid
        @param length       length of uuid
        """
        if alphabet is None:
            self._alphabet = DEFAULT_ALPHABET
        else:
            self._alphabet = alphabet

        if length == 0:
            self._length = DEFAULT_LENGTH
        else:
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
    def alphabet(self, value):
        """! A getter method for alphabet property."""
        self._alphabet = value

    @length.setter
    def length(self, value):
        """! A getter method for length property."""
        self._length = value

    def uuid(self) -> str:
        """! A method for generating uuid."""
        char_list = [random.choice(self.alphabet) for _ in range(self.length)]
        return "".join(char_list)


def uuid(alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH):
    generator = PolytopeUUID(alphabet, length)
    return generator.uuid()
