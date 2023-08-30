import random
import math
from typing import List, Dict

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
        if len(value) < 2:
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
        if value <= 0:
            raise ValueError("length must be positive.")

        self._length = value

    def uuid(self) -> str:
        """! A method for generating uuid."""
        char_list = [random.choice(self.alphabet) for _ in range(self.length)]
        return "".join(char_list)

    def __uuid_bulk_large(self, count: int) -> List[str]:
        if count <= 0:
            raise ValueError("count must be positive.")
        if math.log(count) - self.length * math.log(
            len(self.alphabet)
        ) > -math.log(2):
            raise ValueError("count is too large to generate distinct uuids")

        uuid_set: set = set()
        while len(uuid_set) < count:
            uuid = self.uuid()
            if uuid not in uuid_set:
                uuid_set.add(uuid)
        return list(uuid_set)

    def uuid_bulk(self, count: int) -> List[str]:
        """! A method for bulk generating a list of distinct uuids.

        @param count    number of uuids to generate
        """
        if count <= 0:
            raise ValueError("count must be positive.")

        if self.length * math.log(len(self.alphabet), 2) > 31:
            return self.__uuid_bulk_large(count)

        total: int = len(self.alphabet) ** self.length

        if count > total:
            raise ValueError("count is too large to generate distinct uuids")

        # generate distinct integers in range [0, total)
        num_list: List[int] = []
        replacement: Dict[int, int] = {}

        def index(i: int) -> int:
            return replacement.get(i) or i

        for i in range(count):
            max_value: int = total - i - 1
            rnd = random.randrange(0, max_value + 1)
            num_list.append(index(rnd))
            if rnd != max_value:
                replacement[rnd] = index(max_value)

        uuid_list: List[str] = []
        for num in num_list:
            uuid = ""
            for _ in range(self.length):
                uuid += self.alphabet[num % len(self.alphabet)]
                num //= len(self.alphabet)
            uuid_list.append(uuid)

        return uuid_list


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
