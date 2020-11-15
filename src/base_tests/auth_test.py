'''
Joseph Jeong made auth_test.py
'''
from datetime import timedelta
import pytest
import datetime

<<<<<<< HEAD:src/base_tests/auth_test.py
import data.data as data
import base.auth as auth
from base.error import InputError
from base.other import clear
=======
import src.data.data as data
import src.base.auth as auth
from src.base.error import InputError
from src.base.other import clear
>>>>>>> deployment:src_backend/base_tests/auth_test.py

def coverate_notes():
    """
    Notes on coverage:
    - Impossible to make the token checking alogorithm to check reliably by definition (line 39-40)
    - Impossible to make the u_id checking alogorithm to check reliably by definition (line 52-53)
    - Impossible to create a general test for handles being less than 20 characters
    """

def iteration_2_notes():
    """
    TOKENS:
    using jwt
    need to store

    PASSWORDS:
    Stored as hashed strings

    DATA:
    Persistent storage

    functionally, things should still work the same
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

    # token is a string
    assert isinstance(auth_dict_test['token'], str)

def user_from_u_id(u_id):
    ''' return user from given u_id'''

    focus_user = None
    for user in data.return_users():
        if user['u_id'] == u_id:
            focus_user = user
            break
    return focus_user

def test_auth_register_permission_id():
    ''' checks that the correct permission_id's are given '''
    clear()

    u_id1 = auth.auth_register('test@example.com', 'emilyisshort', 'Emily', 'Luo?').get('u_id')
    u_id2 = auth.auth_register('test2@example.com', 'emilyisshor2t', 'Emil2y', 'Luo2?').get('u_id')
    u_id3 = auth.auth_register('test32@example.com', 'emilyissh3or2t', 'Emi3l2y', 'Lu3o2?').get('u_id')

    # test permission_id's are correct
    assert user_from_u_id(u_id1).get('permission_id') == 1
    assert user_from_u_id(u_id2).get('permission_id') == 2
    assert user_from_u_id(u_id3).get('permission_id') == 2


def test_auth_register_multiple_users():
    """
    - u_id is unique when multiple users are entered
    creates a large  number of u_id's and make sure none of them conflict
    tested it up to 10,000 array_size but takes a while, can go higher for sure
    """

    clear()

    array_size = 100
    array = [0] * array_size

    i = 0
    while i < array_size:
        array[i] = (auth.auth_register('test' + str(i)
        + '@example.com', 'password', 'Test', 'Personmanperson')['u_id'])
        i += 1

    assert len(array) == len(set(array))

    # a unique handle is produced
    new_list = []
    for user in data.return_users():
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
    # assert len(auth_login_test['token']) == 20

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
    # correct password is 'correct_password'
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
    token = registration['token']

    # # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')

    is_success = auth.auth_logout(invalid_token)
    assert is_success['is_success'] is False

    # - returns true when valid token
    is_success = auth.auth_logout(token)
    assert is_success['is_success']

def test_auth_logout_wrong_session():
    ''' tests logout for user with invalid token '''
    clear()

    # register the first time
    registration1 = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token1 = registration1['token']

    # log them out
    assert auth.auth_logout(token1)['is_success']

    # try logging them out again (doesn't work)
    assert auth.auth_logout(token1)['is_success'] is False

    # log the same user back in
    registration2 = auth.auth_login('valid@example.com', 'password')
    token2 = registration2['token']

    # try logging out with the first token
    assert auth.auth_logout(token1)['is_success'] is False

    # try logging out with the second token
    assert auth.auth_logout(token2)['is_success']

def get_reset_code(u_id):
    ''' helper function to get the password code '''
    
    for user in data.return_users():
        if user['u_id'] == u_id:
            return user.get('password_reset')

def test_passwordreset_not_real_user():
    '''
    Given an email address, if the user is a registered user, 
    send's them a an email containing a specific secret code, that 
    when entered in auth_passwordreset_reset, shows that the user 
    trying to reset the password is the one who got sent this email.

    This will test what happens when user is not real
    '''
    clear()

    # no users registered
    with pytest.raises(InputError):
        auth.passwordreset_request('invalidemail@google.com')

def test_passwordreset_real_user():
    '''
    This will test what happens when user is real
    '''
    clear()

    # register a user
    u_id = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old').get('u_id')
    
    auth.passwordreset_request('valid@example.com')
    code = get_reset_code(u_id).get('code')
    now = datetime.datetime.utcnow()

    # check that the code stored was the same as given code
    valid = False
    for user in data.return_users():
        if (user.get('password_reset').get('code') == code
        and abs((now - user.get('password_reset').get('origin')).total_seconds()) < 500):
            valid = True
            break
    # if code wasn't stored, or it was an incorrect code, it's not valid
    # if password_reset doesn't have an acceptable time delta, it is not valid
    assert valid

def test_passwordreset_reset_invalid_code():
    '''
    Given a reset code for a user, set that user's new password to the password provided
    '''
    clear()

    # register a user
    u_id = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old').get('u_id')

    # send the password reset
    auth.passwordreset_request('valid@example.com')
    code = get_reset_code(u_id).get('code')

    # make sure new code is incorrect
    new_code = 'hahagetcooked'
    if code == new_code:
        raise Exception('This is the same code coincidentally')

    with pytest.raises(InputError):
        auth.passwordreset_reset(new_code, 'passwordTime')

def test_passwordreset_reset_invalid_new_password():
    '''
    Given a reset code for a user, set that user's new password to the password provided
    '''
    clear()

    # register a user
    u_id = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old').get('u_id')

    # send the password reset
    auth.passwordreset_request('valid@example.com')
    code = get_reset_code(u_id).get('code') 

    # if password doesn't pass new password checks
    with pytest.raises(InputError):
        auth.passwordreset_reset(code, 'f')

def test_passwordreset_reset_invalid_time():
    '''
    Given a reset code for a user, set that user's new password to the password provided
    '''
    clear()

    # register a user
    u_id = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old').get('u_id')

    # send the password reset
    auth.passwordreset_request('valid@example.com')
    code = get_reset_code(u_id).get('code') 

    # make the time an hour before
    now = datetime.datetime.utcnow()
    before = now - datetime.timedelta(hours=2)
    data.update_user(u_id, 'password_reset', {
        'origin': before,
        'code': code
    })
    
    # check there's an inputerror
    with pytest.raises(InputError):
        auth.passwordreset_reset(code, 'passwordTime')

def test_passwordreset_reset_valid_code():
    ''' test passwordreset with a valid code '''
    clear()

    # register a user
    u_id = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old').get('u_id')

    # send the password reset
    auth.passwordreset_request('valid@example.com')
    code = get_reset_code(u_id).get('code')
    now = datetime.datetime.utcnow()

    # reset the password
    assert auth.passwordreset_reset(code, 'passwordTime') is not None

    new_hash = auth.hash_('passwordTime')

    # check the password
    valid = False
    for user in data.return_users():
        if (user.get('password') == new_hash
        and abs((now - user.get('password_reset').get('origin')).total_seconds()) < 500):
            valid = True
            break
    # if new password wasn't stored, assert
    assert valid