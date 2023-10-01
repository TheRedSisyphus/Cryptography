import pytest

from src.utils import CodedStr, NotInAlphabetError


def test_init_0():
    with pytest.raises(TypeError) as e_info:
        _ = CodedStr(mes=None)
    assert "Parameter mes None should be type str or list (of int and spaces), not <class 'NoneType'>" == str(
        e_info.value)


def test_init_1():
    with pytest.raises(TypeError) as e_info:
        _ = CodedStr(mes=1)
    assert "Parameter mes 1 should be type str or list (of int and spaces), not <class 'int'>" == str(e_info.value)


def test_init_2():
    with pytest.raises(TypeError) as e_info:
        _ = CodedStr(mes=[1, 2, 3, 4, None])
    assert "Parameter mes [1, 2, 3, 4, None] should be type str or list (of int and spaces), not <class 'list'>" == str(
        e_info.value)


def test_init_3():
    with pytest.raises(TypeError) as e_info:
        _ = CodedStr(mes=['a', 'b', 'c', 'd'])
    assert "Parameter mes ['a', 'b', 'c', 'd'] should be type str or list (of int and spaces), not <class 'list'>" == str(
        e_info.value)


def test_init_4():
    with pytest.raises(ValueError) as e_info:
        _ = CodedStr(mes='not in alphabet :/')
    assert 'One or more character(s) from [not in alphabet :/] are not in [abcdefghijklmnopqrstuvwxyz]' == str(
        e_info.value)


def test_init_5():
    code = CodedStr(mes='my message')
    assert code.mes == [12, 24, ' ', 12, 4, 18, 18, 0, 6, 4]


def test_init_6():
    code = CodedStr(mes=' my   message ')
    assert code.mes == [' ', 12, 24, ' ', ' ', ' ', 12, 4, 18, 18, 0, 6, 4, ' ']


def test_init_7():
    code = CodedStr(mes=[1, 2, 3, 4, 5, 6, 34, -2])
    assert code.mes == [1, 2, 3, 4, 5, 6, 8, 24]


def test_get():
    code = CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    assert code[0] == 1
    assert code[4] == ' '


def test_set():
    code = CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    code[1] = ' '
    assert code == CodedStr([1, ' ', 3, 4, ' ', 5, 6])


def test_set_not_in_alphabet():
    code = CodedStr(mes=[1, 2])
    value = 'lol'
    with pytest.raises(NotInAlphabetError) as e_info:
        code[1] = value
    assert "Invalid value lol not in range of 0 len(abcdefghijklmnopqrstuvwxyz)" == str(e_info.value)


def test_repr():
    code = CodedStr(mes=[1, 2, 3, 4, ' ', 5, 6])
    assert repr(code) == "[1, 2, 3, 4, ' ', 5, 6]"


def test_str():
    code = CodedStr(mes=[1, 2, 3, 4, 5, 25, 26, ' '])
    assert str(code) == 'bcdefza '


def test_str_not_in_alphabet_0():
    code = CodedStr(mes=[1, 2, 28, ' '])
    code[2] = 26
    with pytest.raises(NotInAlphabetError) as e_info:
        str(code)
    assert 'Invalid value 26 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_str_not_in_alphabet_1():
    code = CodedStr(mes=[1, 2, 28, ' '])
    code[2] = -1
    with pytest.raises(NotInAlphabetError) as e_info:
        str(code)
    assert 'Invalid value -1 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_eq():
    code = CodedStr(mes=[1, 2, 3, 4, 5, 6])
    code_2 = CodedStr(mes='bcdefg')
    assert code == code_2


def test_ne():
    code = CodedStr(mes=[1, 2, 3, 4, 5, 6])
    code_2 = CodedStr(mes=[0, 1, 2, 3, 4, 5, 6])
    assert code != code_2


def test_lt():
    assert not CodedStr('aaa') < CodedStr('aaa')
    assert CodedStr('abdca') < CodedStr('abdc')


def test_lte():
    assert CodedStr('abdca') <= CodedStr('abdc')
    assert CodedStr('abdca') <= CodedStr('abdca')


def test_gt():
    assert not CodedStr('aaa') > CodedStr('aaa')
    assert CodedStr('zzz') > CodedStr('aaa')


def test_gte():
    assert CodedStr('zzz') >= CodedStr('aaa')
    assert CodedStr('zzz') >= CodedStr('zzz')


def test_pos():
    code = CodedStr(mes=[1, 2, 3, 4, 5, 6])
    assert +code == code


def test_neg():
    code = CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    code_minus = CodedStr(mes=[26, 25, 24, 23, ' ', 22, 21, 1, 0])
    assert -code == code_minus


def test_neg_not_in_alphabet_0():
    code = CodedStr(mes=[1, 2, 28, ' '])
    code[2] = 26
    with pytest.raises(NotInAlphabetError) as e_info:
        -code
    assert 'Invalid value 26 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_neg_not_in_alphabet_1():
    code = CodedStr(mes=[1, 2, 28, ' '])
    code[2] = -1
    with pytest.raises(NotInAlphabetError) as e_info:
        -code
    assert 'Invalid value -1 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_iadd():
    code = CodedStr(mes='abc dz')
    code += 2
    assert code == CodedStr(mes='cde fb')


def test_iadd_not_in_alphabet():
    code = CodedStr(mes='abc dz')
    code[0] = 27
    with pytest.raises(NotInAlphabetError) as e_info:
        code += 1
    assert 'Invalid value 27 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_isub():
    code = CodedStr(mes='azcdefb ')
    code -= 2
    assert code == CodedStr(mes='yxabcdz ')


def test_isub_not_in_alphabet_0():
    code = CodedStr(mes='abc dz')
    code[0] = 26
    with pytest.raises(NotInAlphabetError) as e_info:
        code -= 1
    assert 'Invalid value 26 in abcdefghijklmnopqrstuvwxyz' == str(e_info.value)


def test_isub_not_in_alphabet_1():
    code = CodedStr(mes='abc dz')
    code[0] = -1
    with pytest.raises(NotInAlphabetError):
        code -= 1


def test_revert():
    code = CodedStr(mes=[0, 1, 2, 3, ' ', 4, 5, 25, 26])
    code.revert()
    assert code == CodedStr(mes=[26, 25, 5, 4, ' ', 3, 2, 1, 0])
