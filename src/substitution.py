from math import ceil, sqrt

from src.utils import ALPHABET_25_W, lower_no_space_no_duplicate, Code, lower_no_space, ALPHABET, CodedStr


class Cesar(Code):
    def __init__(self, key: int, alphabet: str = ALPHABET):
        super().__init__(key, alphabet)
        if not isinstance(key, int):
            raise TypeError(f'key {key} must be an int')

    def code(self, message: str) -> str:
        coded = CodedStr(message)
        coded += self.key
        return str(coded)

    def decode(self, message: str) -> str:
        coded = CodedStr(message)
        coded -= self.key
        return str(coded)


class Bazaar(Code):
    def __init__(self,  key: str, alphabet: str = ALPHABET):
        super().__init__(key, alphabet)
        if not isinstance(key, str):
            raise TypeError(f'key {key} must be a string')

    def code(self, message: str) -> str:
        coded = CodedStr(lower_no_space_no_duplicate(message))
        return str(CodedStr([self.key[elem] for elem in coded]))

    def decode(self, message: str) -> str:
        coded = CodedStr(lower_no_space_no_duplicate(message))
        return str(CodedStr([self.key.index(elem) for elem in coded]))


class Polybe(Code):
    def __init__(self, key: str, alphabet=ALPHABET_25_W):
        super().__init__(key, alphabet)
        if not isinstance(self.key, str):
            raise TypeError(f'key {key} must be a string')
        else:
            self.key = list(lower_no_space_no_duplicate(self.key))
            len_key = len(self.key)
            square = []
            len_square = ceil(sqrt(len_key))
            for i, letter in enumerate(self.key):
                if i % len_square == 0:
                    square.append([])
                square[i // len_square].append(letter)

            if len_key < len(alphabet):
                missing_letters = [c for c in alphabet if c not in self.key]
                for i, letter in enumerate(missing_letters):
                    if (i + len_key) % len_square == 0:
                        square.append([])
                    square[(i + len_key) // len_square].append(letter)

            self.square = square

    def __repr__(self):
        return str(self.square)

    def __str__(self):
        output = ''
        for row in self.square:
            for c in row:
                output += f'{c} '
            output += '\n'
        return output

    def code(self, message: str) -> str:
        output = ''
        for c in message:
            if c == ' ':
                pass
            else:
                match = False
                for r, row in enumerate(self.square):
                    for e, elem in enumerate(row):
                        if elem == c:
                            output += f'{r + 1}{e + 1} '
                            match = True
                            break
                    if match:
                        break
                if not match:
                    raise ValueError(f'Character {c} is not in {self.square}')

        return output

    def decode(self, message: str) -> str:
        message = message.replace(" ", "")
        if len(message) % 2 != 0:
            raise ValueError('message is not coded with classic Polybe code')
        else:
            output = ''
            for x, y in zip(message[::2], message[1::2]):  # We iterate coordinate 2 by 2
                try:
                    x = int(x)
                    y = int(y)
                except ValueError:
                    raise ValueError('message is not coded with classic Polybe code')
                output += self.square[x-1][y-1]
        return output


class Vigenere(Code):
    def __init__(self, key: str, alphabet: str = ALPHABET):
        super().__init__(key, alphabet)
        if not isinstance(key, str):
            raise TypeError(f'key {key} must be a string')
        self.key = CodedStr(lower_no_space(self.key))

    def code(self, message) -> str:
        coded_str_message = CodedStr(lower_no_space(message))
        len_key = len(self.key)
        for i, _ in enumerate(coded_str_message):
            coded_str_message[i] += self.key[i % len_key]
        return str(coded_str_message)

    def decode(self, message) -> str:
        coded_str_message = CodedStr(message)
        len_key = len(self.key)
        for i, _ in enumerate(coded_str_message):
            coded_str_message[i] -= self.key[i % len_key]
        return str(coded_str_message)
