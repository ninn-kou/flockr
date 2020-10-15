'''
Joseph Jeong made auth_test.py
'''
import pytest

import auth
from error import InputError
import data
from other import clear

def coverate_notes():
    """
    Notes on coverage:
    - Impossible to make the token checking alogorithm to check reliably by definition (line 39-40)
    - Impossible to make the u_id checking alogorithm to check reliably by definition (line 52-53)
    - Impossible to create a general test for handles being less than 20 characters
    """

def auth_register_notes():
    """
    auth_register()
    It should create a new account

    RETURNS:
    a dict with the u_id and the token

    DATA STRUCTURE:
    A handle is produced that is the concentation of a islower()
    first name and last name < 20 characters (NOT token or u_id)
    Handle MUST be unique -> stored in local data structure

    Probably want to store user data in a data.py file stored locally

    THEREFORE, TEST EVERYTHING BELOW:
    - Dict structure -> {u_id, token}
    - u_id is an integer
    - token is a string
    - u_id is unique when multiple users are entered
    - a valid token is returned
    - a unique handle is produced
    - spits out 'InputError' if: (raise InputError)
        - email is not a valid email (check with regex)
        - email address is already used
        - len(password) < 6
        - len(name_first) < 1 || len(name_first) > 50
        - len(name_last) < 1 || len(name_last) > 50
    """
def test_auth_register_correct_return():
    """
    check that correct data structure is returned
    """
    clear()

    # - Dict structure -> {u_id, token}
    auth_dict_test = auth.auth_register('test@example.com', 'emilyisshort', 'Emily', 'Luo?')
    assert isinstance(auth_dict_test, dict)
    assert auth_dict_test['u_id']
    assert auth_dict_test['token']

    # - u_id is an integer
    assert isinstance(auth_dict_test['u_id'], int)

    # - token is a string
    assert isinstance(auth_dict_test['token'], str)

def test_auth_register_multiple_users():
    """
    - u_id is unique when multiple users are entered
    creates a large  number of u_id's and make sure none of them conflict
    tested it up to 10,000 array_size but takes a while, can go higher for sure
    """

    clear()

    array_size = 1000
    array = [0] * array_size

    i = 0
    while i < array_size:
        array[i] = (auth.auth_register('test' + str(i)
        + '@example.com', 'password', 'Test', 'Person')['u_id'])

        i += 1

    assert len(array) == len(set(array))

    # a unique handle is produced
    new_list = []
    data.init_users()
    for user in data.users:
        new_list.append(user['handle_str'])
    assert len(new_list) == len(set(new_list))

def test_auth_register_input_error_valid_email():
    ''' tests whether register checks valid emails'''

    clear()
    ##########################################################################
    # - spits out 'InputError' if: (raise InputError)
    # - email is not a valid email (check with regex)
    with pytest.raises(InputError):
        auth.auth_register('invalidexample.com', 'password', 'Mate', 'Old')
    with pytest.raises(InputError):
        auth.auth_register('invalid@example', 'password', 'Mate', 'Old')

def test_auth_register_input_error_existing_email():
    ''' tests whether register checks existing emails'''

    clear()

    # - email address is already used
    # this is the email registered at the top of the test function
    auth.auth_register('test@examples.com', 'emilyisshort', 'Emily', 'Luo?')
    with pytest.raises(InputError):
        auth.auth_register('test@examples.com', 'emilyisshort', 'Emily', 'Luo?')

def test_auth_register_input_error_short_password():
    ''' tests whether register checks short passwords'''
    clear()
    # - len(password) < 6
    with pytest.raises(InputError):
        auth.auth_register('validemail@example.com', 'boo', 'Test', 'Person')

def test_auth_register_input_error_wrong_len_name_first():
    '''tests whether register checks wrong first name length'''
    clear()
    # - len(name_first) < 1 || len(name_first) > 50
    # make a long name
    long_first_name = ""
    for _ in range(55):
        long_first_name += "a"
    with pytest.raises(InputError):
        auth.auth_register('validemailagain@example.com', 'password', long_first_name, 'Person')
    # make a short name
    with pytest.raises(InputError):
        auth.auth_register('validemailagain2@example.com', 'password', '', 'Person')

def test_auth_register_input_error_wrong_len_name_last():
    ''' tests whether register checks wrong last name length'''
    clear()
    # - len(name_last) < 1 || len(name_last) > 50
    long_last_name = ""
    for _ in range(55):
        long_last_name += "a"
    with pytest.raises(InputError):
        auth.auth_register('validemailagain@example.com', 'password', 'Test', long_last_name)
    # make a short name
    with pytest.raises(InputError):
        auth.auth_register('validemailagain2@example.com', 'password', 'Test', '')

def auth_login_notes():
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
    - spits out 'InputError' if:
        - email is not a valid email (check with regex)
        - email is not in data structure i.e. user isn't registered
        - password is not correct (we love storing raw passwords)
    """

def test_auth_login_correct_return():
    ''' checks correct return from login'''
    clear()
    # register a user
    auth_register_test = auth.auth_register('tests@example.com', 'password', 'Test Person', 'Bam')

    # - Dict structure -> {u_id, token}
    auth_login_test = auth.auth_login('tests@example.com', 'password')
    assert isinstance(auth_login_test, dict)
    assert auth_login_test['u_id']
    assert auth_login_test['token']

    # - u_id is an integer
    assert isinstance(auth_login_test['u_id'], int)

    # - token is a string
    assert isinstance(auth_login_test['token'], str)

    # - The correct u_id is returned
    assert auth_login_test['u_id'] == auth_register_test['u_id']

    # - a valid token is returned
    assert len(auth_login_test['token']) == 20

def test_auth_login_input_error_invalid_email():
    ''' tests if login checks valid email'''
    clear()
    # - spits out 'InputError' if:
    # - email is not a valid email (check with regex)
    with pytest.raises(InputError):
        auth.auth_login('invalidexample.com', 'password')
    with pytest.raises(InputError):
        auth.auth_login('invalid@example', 'password')

def test_auth_login_input_error_nonexistent_email():
    ''' tests whether login checks nonexistent emails'''
    clear()
    # - email is not in data structure i.e. user isn't registered
    with pytest.raises(InputError):
        # this was never registered previously
        auth.auth_login('nottest@example.com', 'password')

def test_auth_login_input_error_incorrect_password():
    ''' tests whether login checks password'''
    clear()
    auth.auth_register('tests@examples.com', 'correct_password', 'test', 'person')

    # - password is not correct (we love storing raw passwords)
    # correct password is 'password'
    with pytest.raises(InputError):
        auth.auth_login('tests@examples.com', 'incorrect_password')

def auth_loguout_notes():
    """
    auth_logout()
    Given an active token, invalidates the token to log the user out

    RETURNS:
    {is_success}
    where is_success is a bool

    THEREFORE, TEST EVERYTHING BELOW:
    - returns false when invalid token
    - returns true when valid token
    """

def test_auth_logout():
    ''' tests whether user is actually logged out'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    # registration = auth.auth_login('valid@example.com', 'password')
    token = registration['token']

    # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')

    is_success = auth.auth_logout(invalid_token)
    assert is_success['is_success'] is False

    # - returns true when valid token
    is_success = auth.auth_logout(token)
    assert is_success['is_success']
