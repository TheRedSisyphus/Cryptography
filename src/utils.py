from typing import OrderedDict, Union, Iterable

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class NotInAlphabetError(Exception):
    pass


def alphabet_removal(remove: str, alphabet: str = ALPHABET, ) -> str:
    to_remove = remove.replace(" ", "")
    if not set(to_remove).issubset(set(alphabet)):
        raise ValueError(f'Trying to remove characters not in alphabet : {[c for c in to_remove if c not in alphabet]}')
    return ''.join([c for c in alphabet if c not in to_remove])


def lower_no_space(string) -> str:
    return string.lower().replace(" ", "")


def duplicates(string) -> list:
    return list(set([elem for elem in string if string.count(elem) > 1]))


def lower_no_space_no_duplicate(string) -> str:
    string_lower_no_space = string.lower().replace(" ", "")
    return ''.join(list(OrderedDict.fromkeys(string_lower_no_space)))  # remove duplicates and keep order


class Code:
    def __init__(self, key: Union[str, int]):
        if isinstance(key, int) or isinstance(key, str):
            self.key = key
        else:
            raise TypeError(f'key {key} must be an int or a string')

    def code(self, message: str) -> str:
        raise NotImplementedError

    def decode(self, message: str) -> str:
        raise NotImplementedError


class CodedStr:
    """
    CodedStr is a list of int and space character, representing a coded message in a given alphabet.
    For example, 'my secret message' is [12, 24, ' ', 18, 4, 2, 17, 4, 19, ' ', 12, 4, 18, 18, 0, 6, 4]
    """

    def __init__(self, mes: Union[str, list], alphabet=ALPHABET):
        if dupl := duplicates(alphabet):
            raise ValueError(f"alphabet can't have duplicate, got {dupl}")
        self.alphabet = alphabet
        self.cycle = len(alphabet)
        if isinstance(mes, str):
            try:
                self.mes = [' ' if c == ' ' else self.alphabet.index(c) for c in mes]
            except ValueError:
                raise ValueError(f'One or more character(s) from "{mes}" are not in "{self.alphabet}"')

        elif isinstance(mes, Iterable) and all([((type(c) == int) or (c == ' ')) for c in mes]):
            # E.g. If mes is 48, it gets transformed in 22 = 48 - 26
            self.mes = [' ' if c == ' ' else c % self.cycle for c in mes]
        else:
            raise TypeError(f'Parameter mes {mes} should be type str or list (of int and spaces), not {type(mes)}')

    def __getitem__(self, item: int) -> Union[str, int]:
        return self.mes[item]

    def __setitem__(self, item: int, value: Union[str, int]) -> None:
        if isinstance(value, str) and value != ' ':
            raise NotInAlphabetError(f'Invalid value {value} not in range of 0 len({self.alphabet})')
        self.mes[item] = value

    def __repr__(self) -> str:
        return str(self.mes)

    def __str__(self) -> str:
        output = ''
        for elem in self.mes:
            if elem == ' ':
                output += ' '
            elif type(elem) == int:
                output += self.alphabet[elem % self.cycle]
            else:
                raise NotInAlphabetError(f'Invalid value {elem} in {self.alphabet}')
        return output

    def __iter__(self):
        for elem in self.mes:
            yield elem

    def __len__(self):
        return len(self.mes)

    def __eq__(self, other) -> bool:
        return self.mes == other.mes

    def __ne__(self, other) -> bool:
        return self.mes != other.mes

    # lexicographic order
    def __lt__(self, other) -> bool:
        return str(self.mes) < str(other.mes)

    def __le__(self, other) -> bool:
        return str(self.mes) <= str(other.mes)

    def __gt__(self, other) -> bool:
        return str(self.mes) > str(other.mes)

    def __ge__(self, other) -> bool:
        return str(self.mes) >= str(other.mes)

    def __pos__(self):
        return self

    def __neg__(self):
        output = ''
        for i, elem in enumerate(self.mes):
            if elem == ' ':
                output += elem
            elif type(elem) == int:
                output += self.alphabet[(-elem) % self.cycle]
            else:
                raise NotInAlphabetError(f'Invalid value {elem} in {self.alphabet}')
        return CodedStr(output)

    def __iadd__(self, key: int):
        for i, elem in enumerate(self.mes):
            if elem == ' ':
                pass
            elif type(elem) == int:
                self[i] = (elem + key) % self.cycle
            else:
                raise NotInAlphabetError(f'Invalid value {elem} in {self.alphabet}')
        return self

    def __isub__(self, key: int):
        for i, elem in enumerate(self.mes):
            if elem == ' ':
                pass
            elif type(elem) == int:
                self[i] = (elem - key) % self.cycle
            else:
                raise NotInAlphabetError(f'Invalid value {elem} in {self.alphabet}')
        return self

    def revert(self):
        self.mes.reverse()

    def index(self, elem):
        for i, c in enumerate(self):
            if c == elem:
                return i
        raise ValueError(f'{elem} is not in CodedStr')
