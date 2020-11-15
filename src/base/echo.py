'''
    For sanity test in echo_http_test.py
'''

<<<<<<< HEAD:src/base/echo.py
from base.error import InputError
=======
from src.base.error import InputError
>>>>>>> deployment:src_backend/base/echo.py

def echo(value):
    ''' echo back if value is echo'''
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
