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
import datetime
from jwt import DecodeError

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build

import src.data.data as data
from src.base.error import InputError

def create_secret(token_length, whitespace = True):
    """Create a specified length character long ascii string for token."""
    # Create list of random characters and length of token.
    valid_characters = string.ascii_letters + string.digits
    if whitespace:
        valid_characters += string.punctuation + string.whitespace

    # create token of that length and with specified characters
    return "".join(random.choices(valid_characters, k = token_length))

def read_jwt_secret():
    ''' read token_secret from file '''

    # check if token file exists
    # create a new one if it doesn't
    jwt_path = os.getcwd() + '/src/data/JWT_SECRET.p'
    if os.path.isfile(jwt_path) is False:
        with open(jwt_path, 'wb') as file:
            new_token = create_secret(10000)
            pickle.dump(new_token, file)

    # read token_secret from file
    # stored in pickle so user can't read it *dab*
    with open('src/data/JWT_SECRET.p', 'rb') as file:
        token_secret = pickle.load(file)

    return token_secret

# reads token from file
JWT_SECRET = read_jwt_secret()

def regex_email_check(email):
    """
    Check that the email is validly formatted email.
    Not using the given regex method as it tells me that my own
    actual email is not a real email
    """

    regex = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"  
    # regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

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

    # Create base concatenation.
    raw_concatenation = name_first + name_last
    raw_concatenation = raw_concatenation[:20]
    if check_in_users('handle_str', data.return_users(), raw_concatenation) is None:
        return raw_concatenation

    # add u_id if handle is not already unique
    u_id_len = len(str(u_id))
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
    id = 2
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
    session_secret = create_secret(50)
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
        'session_secret': session_secret,
        'profile_img_url':'',
    }
    data.append_users(user)

    # Creates an object with u_id and token.
    token_object = {
        'u_id': u_id,
        'token': token,
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
        raise InputError('Email is not for a registered user')

    # Check password is correct
    if focus_user['password'] != hash_(password):
        raise InputError('Incorrect Password')

    # Creates a token
    u_id = focus_user['u_id']
    session_secret = create_secret(50)
    token = create_token(u_id, session_secret)

    # update the session_secret in stored users
    data.update_user(u_id, 'session_secret', session_secret)

    token_object = {
        'u_id': u_id,
        'token': token,
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

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    message = (service.users().messages().send(userId=user_id, body=message)
            .execute())
    return message

def send_email(email, html):
    
    # authorise gmail
    path = os.getcwd() + '/src/data/gmail_token.p'
    with open(path, 'rb') as auth_token:
        creds = pickle.load(auth_token)
    
    gmail = build('gmail', 'v1', credentials=creds)

    # create the email
    msg = create_message(
        'joseph@josephjeo.ng', # hi, please don't destroy me
        email,    # the person receiving email
        'Your Flockr Password Reset Code',
        html
    )

    # send the email
    send_message(gmail, 'me', msg)

def passwordreset_request(email):
    ''' password reseting '''

    # find the user in question
    focus_user = None
    for user in data.return_users():
        if user['email'] == email:
            focus_user = user
            break
    if focus_user is None:
        raise InputError('This is an incorrect email')

    # create the secret code
    code = create_secret(10, whitespace=False)

    # store the code
    u_id = focus_user['u_id']
    data.update_user(u_id, 'password_reset', {
        'origin': datetime.datetime.utcnow(),
        'code': code
    })

    # get the html formatted
    html = data.return_password_reset_email().format(
        PREVIEWTEXT = 'This is your password reset code',
        FIRSTNAME = focus_user.get('name_first'),
        CODE = code
    )

    # send the email
    send_email(email, html)
    return {}

def passwordreset_reset(reset_code, new_password):
    ''' check if reset_code is correct '''

    # check that password is valid length
    if len(new_password) < 6:
        raise InputError('Password Too Short')
    now = datetime.datetime.utcnow()

    # check that the code stored was the same as given code
    focus_user = None
    for user in data.return_users():
        if (user.get('password_reset').get('code') == reset_code
        and abs((now - user.get('password_reset').get('origin')).total_seconds()) < 500):
            focus_user = user
            break
    # raise input error if person is faulty
    if focus_user is None:
        raise InputError('Invalid Reset Code')

    # store the new password
    data.update_user(focus_user['u_id'], 'password', hash_(new_password))

    return {}