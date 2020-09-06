# This file is here to help you get started

import auth
import pytest
from error import InputError

def test_login_valid():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#') # Expect to work since we registered

def test_login_invalid():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError) as e:
        auth.auth_login('didntusethis@gmail.com', '123abcd!@#') # Expect fail since never registered