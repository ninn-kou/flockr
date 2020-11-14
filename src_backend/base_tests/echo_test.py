'''
    For sanity test in echo_http_test.py
'''
import pytest

import src_backend.base.echo as echo
from src_backend.base.error import InputError

def test_echo():
    ''' test echo sanity check'''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    ''' test echo Input Error sanity check'''
    with pytest.raises(InputError):
        assert echo.echo("echo")
