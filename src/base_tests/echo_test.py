import base.echo as echo
import pytest
from base.error import InputError

def test_echo():
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    with pytest.raises(InputError):
        assert echo.echo("echo")
