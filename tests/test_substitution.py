import pytest

import src.substitution as s
from src.utils import alphabet_removal, ALPHABET


# CESAR

def test_cesar_wrong_init():
    with pytest.raises(TypeError) as e:
        _ = s.Cesar(key='bad')
    assert str(e.value) == 'key bad must be an int'


def test_cesar_code_full_cycle():
    code_c = s.Cesar(key=26)
    assert code_c.code('bonjour') == 'bonjour'


def test_cesar_code_reverse_cycle():
    code_c_0 = s.Cesar(key=25)
    code_c_1 = s.Cesar(key=-1)
    assert code_c_0.code('bonjour') == code_c_1.code('bonjour')


def test_cesar_code():
    code_c = s.Cesar(key=2)
    assert code_c.code('bonjour ') == 'dqplqwt '


def test_cesar_decode():
    code_c = s.Cesar(key=2)
    assert code_c.decode('  dqplqwt ') == '  bonjour '


def test_cesar_code_decode():
    code_c = s.Cesar(key=12)
    assert code_c.decode(code_c.code('je suis le meme')) == 'je suis le meme'
    assert code_c.code(code_c.decode('pareil je suis identique')) == 'pareil je suis identique'


# BAZAAR

def test_bazaar_wrong_init():
    with pytest.raises(TypeError) as e:
        _ = s.Bazaar(key=1)
    assert str(e.value) == 'key 1 must be a string'


def test_bazaar_code():
    code_c = s.Bazaar(key='motizngylwfhjcsxrbdkvpqaue')
    assert code_c.code('bon jour') == 'oscwsvb'


def test_bazaar_decode():
    code_c = s.Bazaar(key='motizngylwfhjcsxrbdkvpqaue')
    assert code_c.decode(' oscwsvb ') == 'bonjour'


def test_bazaar_code_decode():
    code_c = s.Bazaar(key='motizngylwfhjcsxrbdkvpqaue')
    assert code_c.decode(code_c.code('je suis le meme')) == 'jesuislememe'
    assert code_c.code(code_c.decode('pareil je suis identique')) == 'pareiljesuisidentique'


# POLYBE

def test_polybe_wrong_init_0():
    with pytest.raises(TypeError) as e:
        _ = s.Polybe(key=1)
    assert str(e.value) == 'key 1 must be a string'


def test_polybe_wrong_init_1():
    with pytest.raises(ValueError) as e:
        _ = s.Polybe(key='')
    assert str(e.value) == 'Key cannot be empty'


def test_polybe_code_0():
    code_c = s.Polybe(key=alphabet_removal(alphabet=ALPHABET, remove='p'))
    with pytest.raises(ValueError) as e:
        code_c.code('pour')
    assert str(e.value) == "Character p is not in [['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'], ['k', 'l', 'm', 'n', 'o'], ['q', 'r', 's', 't', 'u'], ['v', 'w', 'x', 'y', 'z']]"


def test_polybe_code_1():
    code_c = s.Polybe(key='depuis')
    assert code_c.code('bon jour') == '32 63 62 51 63 21 72 '
    assert code_c.alphabet == alphabet_removal('w', ALPHABET)


def test_polybe_repr():
    code_c = s.Polybe(key=alphabet_removal(alphabet=ALPHABET, remove='w'))
    assert repr(code_c) == "[['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'], ['k', 'l', 'm', 'n', 'o'], ['p', 'q', 'r', 's', 't'], ['u', 'v', 'x', 'y', 'z']]"


def test_polybe_str():
    code_c = s.Polybe(key=alphabet_removal(alphabet=ALPHABET, remove='w'))
    assert str(code_c) == "a b c d e \nf g h i j \nk l m n o \np q r s t \nu v x y z \n"


def test_polybe_decode_0():
    code_c = s.Polybe(key='motizngylwfhjcsxrbdkvpqaue')
    with pytest.raises(ValueError) as e:
        code_c.decode('15 41 33 24 ab')
    assert str(e.value) == 'message is not coded with classic Polybe code'


def test_polybe_decode_1():
    code_c = s.Polybe(key='motizngylwfhjcsxrbdkvpqaue')
    with pytest.raises(ValueError) as e:
        code_c.decode('15 41 33 24 a')
    assert str(e.value) == 'message is not coded with classic Polybe code'


def test_polybe_decode_2():
    code_c = s.Polybe(key='motizngylwfhjcsxrbdkvpqaue')
    assert code_c.decode('15 41 33 24') == 'zdsw'


def test_polybe_code_decode():
    code_c = s.Polybe(key='motizngylwfhjcsxrbdkvpqaue')
    assert code_c.decode(code_c.code('je suis le meme')) == 'jesuislememe'

    assert code_c.code(code_c.decode('12 35 34 25 35 51 43 ')) == '12 35 34 25 35 51 43 '


# VIGENERE

def test_vigenere_wrong_init_0():
    with pytest.raises(TypeError) as e:
        _ = s.Vigenere(key=1)
    assert str(e.value) == 'key 1 must be a string'


def test_vigenere_wrong_init_1():
    with pytest.raises(ValueError) as e:
        _ = s.Vigenere(key='')
    assert str(e.value) == 'Key cannot be empty'


def test_vigenere_code():
    code_c = s.Vigenere(key='chiffre')
    assert code_c.code('Je dedicace ce livre') == 'll ljizgcjm hj cmxym'


def test_vigenere_decode():
    code_c = s.Vigenere(key='cle')
    assert code_c.decode('afddfsgdfaa') == 'yuzbuoesbyp'


def test_vigenere_code_decode():
    code_c = s.Vigenere(key='chiffre')
    assert code_c.decode(code_c.code('Je dedicace ce livre')) == 'je dedicace ce livre'

    assert code_c.code(code_c.decode('Je dedicace ce livre')) == 'je dedicace ce livre'
