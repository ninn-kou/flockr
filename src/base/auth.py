'''
    auth.py written by Joseph Jeong.
'''
import re
import random
import string
import hashlib

import data.data as data
from base.error import InputError

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

def create_token(u_id, users):
    """Create a 20 character long ascii string for token."""

    # Create list of random characters and length of token.
    valid_characters = string.ascii_letters + string.digits + string.punctuation
    token_length = 20

    # create token of that length and with specified characters
    token = "".join(random.choices(valid_characters, k = token_length))

    # check if token is already being used
    for user in users:
        if user['token'] == token:
            token = create_token(u_id, users)
            break

    return token

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

def hash(input):
    ''' create a has with input'''

    # create the hash
    hash = hashlib.sha256(input.encode()).hexdigest()
    print(hash)

    return hash

def auth_register(email, password, name_first, name_last):
    """ Function to register a new user to the program."""

    # check for errors in input
    auth_register_error_check(email, password, name_first, name_last)

    # Create a unique u_id.
    u_id = create_u_id(data.return_users())

    # creates a random and unique token.
    token = create_token(u_id, data.return_users())

    # create a unique handle
    handle = handle_generator(name_first, name_last, data.return_users())

    password = hash(password)

    # Create and store a user object.
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'token': token,
        'password': password
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

    print(focus_user)

    # Check password is correct
    if focus_user['password'] != hash(password):
        raise InputError

    # Creates an object with u_id and token.
    u_id = focus_user['u_id']
    token = create_token(u_id, data.return_users())

    token_object = {
        'u_id': u_id,
        'token': token
    }

    # Add token to program.
    data.add_token(token_object)

    return token_object

def auth_logout(token):
    """Used to log user out of program."""
    # Search for token in token dict.
    user = data.remove_token(token)

    # Returns accordingly if token is found.
    if user is None:
        return {'is_success': False}
    return {'is_success': True}
