"""
For sanity test in echo_http_test.py
"""

from src.base.error import InputError

def echo(value):
    """ Echo back if value is echo."""
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
