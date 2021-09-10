from domain.model import foo


def test_foo():
    result = foo()
    assert result == 42
