'''
    auth.py written by Joseph Jeong.
'''
import re
import random
import string
import hashlib
import os.path
import pickle
import jwt
from jwt import DecodeError

import data.data as data
from base.error import InputError

def create_secret():
    """Create a 50 character long ascii string for token."""
    # Create list of random characters and length of token.
    valid_characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    token_length = 50
    
    # create token of that length and with specified characters
    return "".join(random.choices(valid_characters, k = token_length))

def read_jwt_secret():
    ''' read token_secret from file '''

    # check if token file exists
    # create a new one if it doesn't
    if os.path.isfile('src/data/JWT_SECRET.p') is False:
        with open('src/data/JWT_SECRET.p', 'wb') as file:
            new_token = ''
            for _ in range(50):
                new_token += create_secret()
            pickle.dump(new_token, file)

    # read token_secret from file
    # stored in pickle so user can't read it *dab*
    with open('src/data/JWT_SECRET.p', 'rb') as file:
        token_secret = pickle.load(file)
        
    return token_secret

# reads token from file
JWT_SECRET = read_jwt_secret()

def regex_email_check(email):
    """Check that the email is validly formatted email."""

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email) is None:
        raise InputError("That's not a real email!")

def check_in_users(data_type, users, item):
    """Check for a particular data type in users list."""

    focus_user = None
    for user in users:
        if user[data_type] == item:
            focus_user = user
            break
    return focus_user

def create_u_id(users):
    """Create a random 32 bit unsigned integer to use as a u_id."""

    # Create a random 32 bit unsigned integer.
    u_id = random.randint(0, 0xFFFFFFFF)

    # Simple recursive function to check whether u_id is unique.
    for user in users:
        if user['u_id'] is u_id:
            u_id = create_u_id(users)
            break

    return u_id

def handle_generator(name_first, name_last, u_id):
    """
    Generates a unique handle.
    Much simpler than the thing I had before
    """

    u_id_len = len(str(u_id))

    # Create base concatenation.
    raw_concatenation = name_first + name_last
    # 20 is maximum lenth of handle
    cut_concatenation = raw_concatenation[0:20-u_id_len]
    # u_id is already verified to be unique
    u_id_concatenation = cut_concatenation + str(u_id)

    return u_id_concatenation

def auth_register_error_check(email, password, name_first, name_last):
    """Handles error checking for auth_register."""

    # Check for valid input.
    regex_email_check(email)

    # Check if email is already used.
    if check_in_users('email', data.return_users(), email) is not None:
        raise InputError('Email Already in Use')

    # check len(password) >= 6.
    if len(password) < 6:
        raise InputError('Password Too Short')

    # Check first name matches requirements.
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('First Name Incorrect Length')

    # Check Last Name matches requirements.
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Last Name Incorrect Length')

def hash_(_input):
    ''' create a hash with input'''

    # create the hash
    _hash = hashlib.sha256(_input.encode()).hexdigest()

    return _hash

def create_token(u_id, session_secret):
    ''' 
    encode email in jwt object

    The u_id is is in the public header
    This is used to identify the user's session_secret

    the session_secret is only valid once per login
    it is in an encrypted dict
    when logged out, the stored session_session is replaced with None

    There is also a JWT_SECRET that is used to decrypt the object

    Therefore, the user needs both the JWT_SECRET and session_secret
    to validate their login
    '''

    # payload includes email
    headers = {'u_id': u_id}
    payload = {'session_secret': session_secret}

    # encode u_id in jwt object
    encoded = jwt.encode(payload, JWT_SECRET, 
        algorithm='HS256', headers=headers).decode('utf-8')

    return encoded

def decode_token(token):
    ''' 
    Return user dict from given token
    If incorrect token or user is inputted, it returns None
    '''

    # firstly get public u_id from header
    try:
        u_id = jwt.get_unverified_header(token).get('u_id')
    except DecodeError:
        return None

    # next, get the hidden session_secret
    try:
        stored_secret = jwt.decode(token, JWT_SECRET, algorithms=['HS256']).get('session_secret')
    except DecodeError:
        # if it fails to decode token, return none
        return None
    # find user with session secret
    focus_user = None
    for user in data.return_users():
        if (user.get('session_secret') == stored_secret and user.get('u_id') == u_id):
            # if user is correct and matches the session
            focus_user = user
            break
    
    # if u_id and session_secret match, return user
    # if no user is found, it also returns None
    return focus_user

def determine_permission_id():
    ''' check first user to add permission id '''

    # check if user list is empty
    if not data.return_users():
        id = 1
    else:
        id = 2

    return id

def auth_register(email, password, name_first, name_last):
    """ Function to register a new user to the program."""

    # check for errors in input
    auth_register_error_check(email, password, name_first, name_last)

    # Create variables for new user
    u_id = create_u_id(data.return_users())
    session_secret = create_secret()
    token = create_token(u_id, session_secret)
    handle = handle_generator(name_first, name_last, u_id)
    password = hash_(password)
    permission_id = determine_permission_id()
    # Create and store a user object.
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'password': password,
        'permission_id': permission_id,
        'session_secret': session_secret
    }
    data.append_users(user)

    # Creates an object with u_id and token.
    token_object = {
        'u_id': u_id,
        'token': token
    }
    return token_object

def auth_login(email, password):
    """ Used to log user into program."""

    # check if email is valid.
    regex_email_check(email)

    # Check if email is used by user.
    focus_user = check_in_users('email', data.return_users(), email)

    # If not stored, raise an error.
    if focus_user is None:
        raise InputError('Email Is Used By Another User')

    # Check password is correct
    if focus_user['password'] != hash_(password):
        raise InputError('Incorrect Password')

    # Creates a token
    u_id = focus_user['u_id']
    session_secret = create_secret()
    token = create_token(u_id, session_secret)

    # update the session_secret in stored users
    data.update_user(u_id, 'session_secret', session_secret)

    token_object = {
        'u_id': u_id,
        'token': token
    }

    return token_object

def auth_logout(token):
    """Used to log user out of program."""

    # decode the user from the token
    user = decode_token(token)
    if user is None:
        return {'is_success': False}

    # remove the session secret in data structure
    data.update_user(user['u_id'], 'session_secret', None)

    # if user has been found while decoding the token, 
    # the process worked 100%
    return {'is_success': True}
