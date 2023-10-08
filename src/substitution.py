from math import sqrt

from src.utils import lower_no_space_no_duplicate, Code, lower_no_space, CodedStr


# Todo : faire une gestion des espaces et des majuscules dans les Code et les CodedStr

class Cesar(Code):
    def __init__(self, key: int):
        super().__init__(key)
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
    def __init__(self,  key: str):
        super().__init__(key)
        if not isinstance(key, str):
            raise TypeError(f'key {key} must be a string')

    def code(self, message: str) -> str:
        coded = CodedStr(lower_no_space(message))
        return str(CodedStr(''.join([self.key[elem] for elem in coded])))

    def decode(self, message: str) -> str:
        coded = CodedStr(lower_no_space(message))
        return str(CodedStr([self.key.index(coded.alphabet[elem]) for elem in coded]))


# class Polybe(Code):
#     def __init__(self, key: str):
#         super().__init__(key)
#         if not isinstance(self.key, str):
#             raise TypeError(f'key {key} must be a string')
#
#         self.key = list(lower_no_space_no_duplicate(self.key))
#         len_key = len(self.key)
#         if len_key == 0:
#             raise ValueError('Key cannot be empty')
#
#     def build_square(self, message: CodedStr) -> list[list[str]]:
#         square = []
#         len_square = int(sqrt(len(message.alphabet)))
#         len_key = len(self.key)
#         for i, letter in enumerate(self.key):
#             if i % len_square == 0:
#                 square.append([])
#             square[i // len_square].append(letter)
#
#         missing_letters = [c for c in message.alphabet if c not in self.key]
#         if missing_letters:
#             for i, letter in enumerate(missing_letters):
#                 if (i + len_key) % len_square == 0:
#                     square.append([])
#                 square[(i + len_key) // len_square].append(letter)
#
#         return square
#
#     def print_square(self, message: CodedStr) -> str:
#         output = ''
#         square = self.build_square(message)
#         for row in square:
#             for c in row:
#                 output += f'{c} '
#             output += '\n'
#         return output
#
#     def code(self, message: str) -> str:
#         message_coded = CodedStr(message)
#         square = self.build_square(message_coded)
#         if sqrt(len(message_coded.alphabet)) != int(sqrt(len(message_coded.alphabet))):
#             raise ValueError(f'alphabet length must be perfect square, got {len(message_coded.alphabet)}')
#         if not set(self.key).issubset(set(message_coded.alphabet)):
#             raise ValueError(f'key must be in alphabet {[c for c in self.key if c not in message_coded.alphabet]}')
#         output = ''
#         for c in message:
#             if c == ' ':
#                 pass
#             else:
#                 if c not in set([elem for row in square for elem in row]):
#                     raise ValueError(f'Character {c} of message not found in Polybe square {square}')
#                 for r, row in enumerate(square):
#                     for e, elem in enumerate(row):
#                         if elem == c:
#                             output += f'{r + 1}{e + 1} '
#
#         return output
#
#     def decode(self, message: str) -> str:
#         message = message.replace(" ", "")
#         message_coded = CodedStr(message)
#         square = self.build_square(message_coded)
#         if len(message_coded) % 2 != 0:
#             raise ValueError('message is not coded with classic Polybe code')
#         else:
#             output = ''
#             for x, y in zip(message_coded[::2], message_coded[1::2]):  # We iterate coordinate 2 by 2
#                 try:
#                     x = int(x)
#                     y = int(y)
#                 except ValueError:
#                     raise ValueError('message is not coded with classic Polybe code')
#                 output += square[x-1][y-1]
#         return output


class Vigenere(Code):
    def __init__(self, key: str):
        super().__init__(key)
        if not isinstance(key, str):
            raise TypeError(f'key {key} must be a string')
        if len(key) == 0:
            raise ValueError('Key cannot be empty')
        self.key = CodedStr(lower_no_space(self.key))

    def code(self, message) -> str:
        coded_str_message = CodedStr(message.lower())
        len_key = len(self.key)
        count_key = 0
        for i, _ in enumerate(coded_str_message):
            if coded_str_message[i] == ' ':
                pass
            else:
                coded_str_message[i] += self.key[count_key % len_key]
                count_key += 1
        return str(coded_str_message)

    def decode(self, message) -> str:
        coded_str_message = CodedStr(message.lower())
        len_key = len(self.key)
        count_key = 0
        for i, _ in enumerate(coded_str_message):
            if coded_str_message[i] == ' ':
                pass
            else:
                coded_str_message[i] -= self.key[count_key % len_key]
                count_key += 1
        return str(coded_str_message)
