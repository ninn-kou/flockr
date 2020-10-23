'''
    auth.py written by Joseph Jeong.
'''
import re
import random
import string
import hashlib
import jwt
from jwt import DecodeError, decode

import data.data as data
from base.error import InputError

def create_secret():
    """Create a 50 character long ascii string for token."""
    # Create list of random characters and length of token.
    valid_characters = string.ascii_letters + string.digits + string.punctuation
    token_length = 50

    # create token of that length and with specified characters
    return "".join(random.choices(valid_characters, k = token_length))

def create_token_secret():
    ''' create secret and create file 
    not currently being used'''

    # double long server secret
    token_secret = create_secret() + create_secret()

    with open('src/data/JWT_SECRET.txt', 'w') as file:
        file.write(token_secret)

    return token_secret

# a new JWT_SECRET every time the server restarts
# may not be the most practical, but it is secure :)
# double the length of every other secret to be even more secure
JWT_SECRET = create_secret() + create_secret()

def regex_email_check(email):
    """Check that the email is validly formatted email."""

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email) is None:
        raise InputError('terrible email')

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

def handle_variabliser(handle, variabliser_num, variabliser, users):
    """
    Creates variable numbers at the end of the string, flawed because it isn't
    optimal randomisation. BUT it does the job -> every handle will ALWAYS be unique,
    even 10,000 of the same name...
    """
    # Check if the handle is unique, if not modify it further.
    check = check_in_users('handle_str', users, handle)

    if check is not None:
        # Check if there are any variabliser characters to iterate through,
        # if not, variabilise more characters.
        if not variabliser:
            variabliser = string.ascii_letters + string.digits
            # need to modify it further
            variabliser_num += 1

        # If true, try other variable characters.
        else:
            # Variabilise the string accordingly.
            handle = handle[0:(-1 * variabliser_num)]

            for _ in range(variabliser_num):
                character = random.choice(variabliser)
                variabliser = variabliser.replace(character, '')
                handle = handle + character

        handle = handle_variabliser(handle, variabliser_num, variabliser, users)
    return handle

def handle_generator(name_first, name_last, users):
    """Generates a unique handle."""

    # Create base concatenation.
    raw_concatenation = name_first + name_last

    if len(raw_concatenation) > 20:
        raw_concatenation = raw_concatenation[:20]
    # make sure handle is unique
    handle = handle_variabliser(raw_concatenation, 0, '', users)

    return handle

def auth_register_error_check(email, password, name_first, name_last):
    """Handles error checking for auth_register."""

    # Check for valid input.
    regex_email_check(email)

    # Check if email is already used.
    if check_in_users('email', data.return_users(), email) is not None:
        raise InputError('1')

    # check len(password) >= 6.
    if len(password) < 6:
        raise InputError('1')

    # Check first name matches requirements.
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('1')

    # Check Last Name matches requirements.
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('1')

def hash_(_input):
    ''' create a hash with input'''

    # create the hash
    _hash = hashlib.sha256(_input.encode()).hexdigest()

    return _hash

def create_token(u_id, session_secret):
    ''' encode email in jwt object'''
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
        if user.get('session_secret') is None:
            continue
        elif (user.get('u_id') == u_id and user.get('session_secret') == stored_secret):
            # if user is correct and matches the session
            focus_user = user
            break
    
    # if u_id and session_secret match, return user
    # if no user is found, it also returns None
    return focus_user

def auth_register(email, password, name_first, name_last):
    """ Function to register a new user to the program."""

    # check for errors in input
    auth_register_error_check(email, password, name_first, name_last)

    # Create a unique u_id.
    u_id = create_u_id(data.return_users())

    # creates a random and unique token.
    session_secret = create_secret()
    token = create_token(u_id, session_secret)

    # create a unique handle
    handle = handle_generator(name_first, name_last, data.return_users())

    # hash password
    password = hash_(password)

    # Create and store a user object.
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'password': password,
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
        raise InputError

    # Check password is correct
    if focus_user['password'] != hash_(password):
        raise InputError

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

    focus_user = None

    # decode the email from the token
    decode = decode_token(token)
    if decode is None:
        return {'is_success': False}
    email = decode.get('email')

    # find email
    for user in data.return_users():
        print(user)
        if user['email'] == email:
            focus_user = user
            break

    # Returns accordingly if token is found.
    if focus_user is None:
        return {'is_success': False}
    return {'is_success': True}
