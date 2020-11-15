'''
    For sanity test in echo_http_test.py
'''
import pytest

<<<<<<< HEAD:src/base_tests/echo_test.py
import base.echo as echo
from base.error import InputError
=======
import src.base.echo as echo
from src.base.error import InputError
>>>>>>> deployment:src_backend/base_tests/echo_test.py

def test_echo():
    ''' test echo sanity check'''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    ''' test echo Input Error sanity check'''
    with pytest.raises(InputError):
        assert echo.echo("echo")
