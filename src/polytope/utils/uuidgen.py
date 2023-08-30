import random
import math
from typing import List

# collision probability in 150,000 entries ~ 1%
# lowercase alphabet + digit except [l, 1, o, 0]
DEFAULT_ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"
DEFAULT_LENGTH = 8


class PolytopeUUID:
    """UUID generator class."""

    def __init__(
        self, alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH
    ) -> None:
        """! PolytopeUUID class initializer.

        @param alphabet     alphabet for generating uuid
        @param length       length of uuid
        """
        self.alphabet = alphabet
        self.length = length

    @property
    def alphabet(self) -> str:
        """! An alphabet property for generating uuid."""
        return self._alphabet

    @alphabet.setter
    def alphabet(self, value: str) -> None:
        """! A setter method for alphabet property."""
        if len(value) < 10:
            raise ValueError("alphabet must be long enough.")
        if len(set(value)) != len(value):
            raise ValueError("alphabet must consist of distinct characters.")

        self._alphabet = value

    @property
    def length(self) -> int:
        """! A length property of uuid."""
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        """! A setter method for length property."""
        if value < 5:
            raise ValueError("length must be large enough.")

        self._length = value

    def uuid(self) -> str:
        """! A method for generating uuid."""
        char_list = [random.choice(self.alphabet) for _ in range(self.length)]
        return "".join(char_list)

    def uuid_bulk(self, count: int) -> List[str]:
        """! A method for bulk generating a list of distinct uuids.

        @param count    number of uuids to generate
        """
        if count < 0:
            raise ValueError("count must be non-negative.")
        if 0 == count:
            return []

        # 0.01 * (|alphabet| ** length) < count
        if math.log(count) - self.length * math.log(
            len(self.alphabet)
        ) > -math.log(100):
            raise ValueError("count is too large to generate distinct uuids")

        uuid_set: set = set()
        while len(uuid_set) < count:
            uuid = self.uuid()
            if uuid not in uuid_set:
                uuid_set.add(uuid)
        return list(uuid_set)


def uuid(
    alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH
) -> str:
    generator = PolytopeUUID(alphabet, length)
    return generator.uuid()


def uuid_bulk(
    count: int, alphabet: str = DEFAULT_ALPHABET, length: int = DEFAULT_LENGTH
) -> List[str]:
    generator = PolytopeUUID(alphabet, length)
    return generator.uuid_bulk(count)
