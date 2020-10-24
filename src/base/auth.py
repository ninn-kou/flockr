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

def to_string(list_):
    string_ = ''
    for char in list_:
        string_ += char
    return string_

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

def add_random_character_to_index(users, handle, og_index, iter):
    ''' adds random character to specified index'''

    # valid characters to add to string
    variabliser = string.digits + string.ascii_letters

    # iterate through every character and see if handle created is unique
    for i in range(iter):
        index = og_index - i + 1
        for char in variabliser:
            handle[index] = char
            if check_in_users('handle_str', users, to_string(handle)) is None:
                return handle
        # if it iterates through all all of them, there is no valid character 
        # in that index
        return None

def add_characters_to_handle(users, handle, num_additive_chars, max_index_len):
    # try adding characters first
    for i in range(num_additive_chars):
        index = max_index_len + i
        result = add_random_character_to_index(users, handle, index, i)
        # if it is a valid handle, return it
        if result is not None:
            return result
    return None

def handle_variabliser(handle, users):
    ''' make sure every handle is unique (I spent way too much time on this)'''

    # if handle is unique, return it straight away
    if check_in_users('handle_str', users, to_string(handle)) is None:
        return handle

    len_handle = 0
    for char in handle:
        if char == '':
            break
        len_handle += 1

    # find the maximum index of original handle
    max_index_len = len_handle

    # specify max index of string
    max_index = 19
    num_additive_chars = max_index - max_index_len + 1

    # try adding characters to handle first
    result = add_characters_to_handle(users, handle, num_additive_chars, max_index_len)
    if result is not None:
        return result

    # if it reaches end of previous loop, it means that it can no longer add characters
    # therefore, we must start destroying previous characters
    # however, each destroyed character can also add characters
    # for every subtractive character, try adding additional characters
    for i in range(max_index_len):
        index = max_index_len - i
        # try changing the last index
        result = add_random_character_to_index(users, handle, index)
        if result is not None:
            return result
        # if simply changing previous characters doesn't work, try adding to it
        result = add_characters_to_handle(users, handle, num_additive_chars, max_index_len)
        if result is not None:
            return result

    # if it reaches end of previous loop, it means that there are literall no possible handles
    # I guess we'll just return no handle
    return None


# def handle_variabliser(handle, variabliser_num, variabliser, users, original_len):
#     """
#     Creates variable numbers at the end of the string, flawed because it isn't
#     optimal randomisation. BUT it does the job -> every handle will ALWAYS be unique,
#     even 10,000 of the same name...
#     """
#     # Check if the handle is unique, if not modify it further.
#     check = check_in_users('handle_str', users, handle)

#     if check is not None:
#         # Check if there are any variabliser characters to iterate through,
#         # if not, variabilise more characters.
#         if not variabliser:
#             variabliser = string.ascii_letters + string.digits
#             # need to modify it further
#             variabliser_num += 1

#         # If true, try other variable characters.
#         else:
#             if len(handle) < 20:
#                 handle += random.choice(variabliser)
#             else:
#                 # Variabilise the string accordingly.
#                 handle_ending = [(original_len - 1), 19]
#                 handle = handle[0:(original_len - 1)]

#                 for _ in range(variabliser_num):
#                     character = random.choice(variabliser)
#                     variabliser = variabliser.replace(character, '')
#                     handle = handle + character + handle_ending

#         handle = handle_variabliser(handle, variabliser_num, variabliser, users, original_len)
#     return handle

def handle_generator(name_first, name_last, users):
    """Generates a unique handle."""

    # Create base concatenation.
    raw_concatenation = name_first + name_last

    if len(raw_concatenation) > 20:
        raw_concatenation = raw_concatenation[:20]
    raw_concatenation = list(raw_concatenation)
    for _ in range(20 - len(raw_concatenation)):
        raw_concatenation.append('')
    # make sure handle is unique
    # original_len = len(raw_concatenation)
    # handle = handle_variabliser(raw_concatenation, 0, '', users, original_len)
    handle = to_string(handle_variabliser(raw_concatenation, users))

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
    handle = handle_generator(name_first, name_last, data.return_users())
    password = hash_(password)
    permission_id = determine_permission_id()
    print(handle)
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

    # decode the user from the token
    user = decode_token(token)
    if user is None:
        return {'is_success': False}

    # remove the session secret in data structure
    data.update_user(user['u_id'], 'session_secret', None)

    # if user has been found while decoding the token, 
    # the process worked 100%
    return {'is_success': True}
