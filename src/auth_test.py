# Joseph Jeong working on auth_test.py
# 24 SEP 2020

import auth
import pytest

"""
auth_register()
It should create a new account 

RETURNS:
a dict with the u_id and the token

DATA STRUCTURE:
A handle is produced that is the concentation of a islower()
first name and last name < 20 characters (NOT token or u_id)
Handle MUST be unique -> stored in local data structure

I guess it stores the user data in a local data structure?
Can modify implementation to suit user.py later down the track

THEREFORE, TEST EVERYTHING BELOW:
- Dict structure -> {u_id, token}
- u_id is an integer
- token is a string
- u_id is unique when multiple users are entered
- a valid token is returned
- spits out 'INPUT ERROR' if:
    - email is not a valid email (check with regex)
    - email address is already used
    - len(password) < 6
    - len(name_first) < 1 || len(name_first) > 50
    - len(name_last) < 1 || len(name_last) > 50

Testing Local Data Structure?
- check user data structure? Not sure how?

"""

"""
auth_login()
Allows a registered user to validate themselves
Checks with local data structure to find u_id and token
from a valid username and password

RETURNS:
A dict with u_id and token

THEREFORE, TEST EVERYTHING BELOW:
- Dict structure -> {u_id, token}
- u_id is an integer
- token is a string
- The correct u_id is returned
- a valid token is returned
- spits out 'INPUT ERROR' if:
    - email is not a valid email (check with regex)
    - email is not in data structure i.e. user isn't registered
    - password is not correct (we love storing raw passwords)
""""

"""
auth_logout()
Given an active token, invalidates the token to log the user out

RETURNS:
{is_success}
where is_success is a bool

THEREFORE, TEST EVERYTHING BELOW:
- returns false when invalid token
- returns true when valid token
""""

def test_auth():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#') # Expect to work since we registered

    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # with pytest.raises(InputError) as e:
    #     auth.auth_login('didntusethis@gmail.com', '123abcd!@#') # Expect fail since never registered

