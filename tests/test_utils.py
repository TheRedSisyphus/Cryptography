import pytest

from src import utils
from src.utils import NotInAlphabetError


# Test utils function

def test_alphabet_removal_0():
    assert utils.alphabet_removal(remove='az', alphabet=utils.ALPHABET) == 'bcdefghijklmnopqrstuvwxy'


def test_alphabet_removal_1():
    with pytest.raises(ValueError) as e:
        utils.alphabet_removal(remove='az 1 ç', alphabet=utils.ALPHABET)
    assert str(e.value) == "Trying to remove characters not in alphabet : ['1', 'ç']"


def test_lower_no_space():
    assert utils.lower_no_space('Adsdf ewq!wE') == 'adsdfewq!we'


def test_lower_no_space_no_duplicate():
    assert utils.lower_no_space_no_duplicate('A AzZ ') == 'az'


# Test Code class

def test_Code_init_0():
    c = utils.Code(key=1, alphabet='12345')
    assert c.alphabet == '12345'


def test_Code_init_1():
    c = utils.Code(key='my key', alphabet='12345')
    assert c.key == 'my key'


def test_Code_init_2():
    with pytest.raises(TypeError) as e:
        _ = utils.Code(key=None)
    assert str(e.value) == 'key None must be an int or a string'


def test_Code_init_3():
    with pytest.raises(ValueError) as e:
        _ = utils.Code(key=1, alphabet='123451')
    assert str(e.value) == "alphabet can't have duplicate"


def test_Code_code():
    c = utils.Code(key=1)
    with pytest.raises(NotImplementedError):
        c.code('hello')


def test_Code_decode():
    c = utils.Code(key='a')
    with pytest.raises(NotImplementedError):
        c.decode('world')


# Test utils.CodedStr class

def test_CodedStr_init_0():
    with pytest.raises(TypeError) as e:
        _ = utils.CodedStr(mes=None)
    assert "Parameter mes None should be type str or list (of int and spaces), not <class 'NoneType'>" == str(
        e.value)


def test_CodedStr_init_1():
    with pytest.raises(TypeError) as e:
        _ = utils.CodedStr(mes=1)
    assert "Parameter mes 1 should be type str or list (of int and spaces), not <class 'int'>" == str(e.value)


def test_CodedStr_init_2():
    with pytest.raises(TypeError) as e:
        _ = utils.CodedStr(mes=[1, 2, 3, 4, None])
    assert "Parameter mes [1, 2, 3, 4, None] should be type str or list (of int and spaces), not <class 'list'>" == str(
        e.value)


def test_CodedStr_init_3():
    with pytest.raises(TypeError) as e:
        _ = utils.CodedStr(mes=['a', 'b', 'c', 'd'])
    assert "Parameter mes ['a', 'b', 'c', 'd'] should be type str or list (of int and spaces), not <class 'list'>" == str(
        e.value)


def test_CodedStr_init_4():
    with pytest.raises(ValueError) as e:
        _ = utils.CodedStr(mes='not in alphabet :/')
    assert 'One or more character(s) from "not in alphabet :/" are not in "abcdefghijklmnopqrstuvwxyz"' == str(
        e.value)


def test_CodedStr_init_5():
    code = utils.CodedStr(mes='my message')
    assert code.mes == [12, 24, ' ', 12, 4, 18, 18, 0, 6, 4]


def test_CodedStr_init_6():
    code = utils.CodedStr(mes=' my   message ')
    assert code.mes == [' ', 12, 24, ' ', ' ', ' ', 12, 4, 18, 18, 0, 6, 4, ' ']


def test_CodedStr_init_7():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 6, 34, -2])
    assert code.mes == [1, 2, 3, 4, 5, 6, 8, 24]


def test_CodedStr_get():
    code = utils.CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    assert code[0] == 1
    assert code[4] == ' '


def test_CodedStr_set():
    code = utils.CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    code[1] = ' '
    assert code == utils.CodedStr([1, ' ', 3, 4, ' ', 5, 6])


def test_CodedStr_set_not_in_alphabet():
    code = utils.CodedStr(mes=[1, 2])
    value = 'lol'
    with pytest.raises(utils.NotInAlphabetError) as e:
        code[1] = value
    assert "Invalid value lol not in range of 0 len(abcdefghijklmnopqrstuvwxyz)" == str(e.value)


def test_CodedStr_repr():
    code = utils.CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    assert repr(code) == "[1, 2, 3, 4, ' ', 5, 6]"


def test_CodedStr_str_0():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 25, 26, ' '])
    assert str(code) == 'bcdefza '


def test_CodedStr_str_1():
    code = utils.CodedStr(mes='1', alphabet='1234')
    code[0] = None
    with pytest.raises(NotInAlphabetError) as e:
        _ = str(code)
    assert str(e.value) == 'Invalid value None in 1234'


def test_CodedStr_iter():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 6])
    out = ''
    for elem in code:
        out += str(elem)
    assert out == '123456'


def test_CodedStr_len():
    code = utils.CodedStr(mes=[1, 2])
    assert len(code) == 2


def test_CodedStr_eq():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 6])
    code_2 = utils.CodedStr(mes='bcdefg')
    assert code == code_2


def test_CodedStr_ne():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 6])
    code_2 = utils.CodedStr(mes=[0, 1, 2, 3, 4, 5, 6])
    assert code != code_2


def test_CodedStr_lt():
    assert not utils.CodedStr('aaa') < utils.CodedStr('aaa')
    assert utils.CodedStr('abdca') < utils.CodedStr('abdc')


def test_CodedStr_lte():
    assert utils.CodedStr('abdca') <= utils.CodedStr('abdc')
    assert utils.CodedStr('abdca') <= utils.CodedStr('abdca')


def test_CodedStr_gt():
    assert not utils.CodedStr('aaa') > utils.CodedStr('aaa')
    assert utils.CodedStr('zzz') > utils.CodedStr('aaa')


def test_CodedStr_gte():
    assert utils.CodedStr('zzz') >= utils.CodedStr('aaa')
    assert utils.CodedStr('zzz') >= utils.CodedStr('zzz')


def test_CodedStr_pos():
    code = utils.CodedStr(mes=[1, 2, 3, 4, 5, 6])
    assert +code == code


def test_CodedStr_neg_0():
    code = utils.CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    code_minus = utils.CodedStr(mes=[26, 25, 24, 23, ' ', 22, 21, 1, 0])
    assert -code == code_minus


def test_CodedStr_neg_1():
    code = utils.CodedStr(mes='1', alphabet='1234')
    code[0] = None
    with pytest.raises(NotInAlphabetError) as e:
        _ = -code
    assert str(e.value) == 'Invalid value None in 1234'


def test_CodedStr_iadd_0():
    code = utils.CodedStr(mes='abc dz')
    code += 2
    assert code == utils.CodedStr(mes='cde fb')


def test_CodedStr_iadd_1():
    code = utils.CodedStr(mes='1', alphabet='1234')
    code[0] = None
    with pytest.raises(NotInAlphabetError) as e:
        code += 1
    assert str(e.value) == 'Invalid value None in 1234'


def test_CodedStr_isub_0():
    code = utils.CodedStr(mes='azcdefb ')
    code -= 2
    assert code == utils.CodedStr(mes='yxabcdz ')


def test_CodedStr_isub_1():
    code = utils.CodedStr(mes='1', alphabet='1234')
    code[0] = None
    with pytest.raises(NotInAlphabetError) as e:
        code -= 1
    assert str(e.value) == 'Invalid value None in 1234'


def test_CodedStr_revert():
    code = utils.CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    code.revert()
    assert code == utils.CodedStr(mes=[26, 25, 5, 4, ' ', 3, 2, 1, 0])


def test_CodedStr_index_0():
    code = utils.CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    assert code.index(5) == 6


def test_CodedStr_index_1():
    code = utils.CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    assert code.index(' ') == 4


def test_CodedStr_index_2():
    code = utils.CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    with pytest.raises(ValueError) as e:
        code.index(13)
    assert str(e.value) == '13 is not in CodedStr'
