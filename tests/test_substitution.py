from src.substitution import Cesar


def test_cesar_code_full_cycle():
    code_c = Cesar(key=26)
    assert code_c.code('bonjour') == 'bonjour'


def test_cesar_code_reverse_cycle():
    code_c_0 = Cesar(key=25)
    code_c_1 = Cesar(key=-1)
    assert code_c_0.code('bonjour') == code_c_1.code('bonjour')


def test_cesar_code():
    code_c = Cesar(key=2)
    assert code_c.code('bonjour ') == 'dqplqwt '


def test_cesar_decode():
    code_c = Cesar(key=2)
    assert code_c.decode('  dqplqwt ') == '  bonjour '


def test_cesar_code_decode():
    code_c = Cesar(key=12)
    assert code_c.decode(code_c.code('je suis le meme')) == 'je suis le meme'
    assert code_c.code(code_c.decode('je suis le meme')) == 'je suis le meme'
