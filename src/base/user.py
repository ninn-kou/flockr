"""Yuhan Yan has done all the user.py and the related tests."""
import data.data as data

import jwt
from   jwt import DecodeError

from base.auth import JWT_SECRET,check_in_users,regex_email_check, decode_token
from base.error import InputError

################################################################################
################################################################################
##
##    Yuhan Yan's work:
##    25 October, 2020
##
##      - user_profile(token, u_id));
##      - user_profile_setname(token, name_first, name_last);
##      - user_profile_setemail(token, email);
##      - user_profile_sethandle(token, handle_str);
##      - and all tests for these functions.
##
################################################################################
################################################################################

def user_profile(token, u_id):
    """For a valid user, returns information about their user_id, email, first name, last name, and handle

    Raises:
        1. InputError
            - User with u_id is not a valid user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    # Avoid someone put a string
    try:
        u_id = int(u_id)
    except Exception:
        raise InputError('terrible uid')

    user = check_in_users("u_id",data.return_users(),int(u_id))
    if user:
        return user
    # User with u_id is not a valid user
    else:
        raise InputError('not user')

def user_profile_setname(token, name_first, name_last):
    """Update the authorised user's first and last name

    Raises:
        1. InputError
            - name_first is not between 1 and 50 characters inclusively in length
            - name_last is not between 1 and 50 characters inclusively in length
    """
    # decode the token
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')

    # Check first name matches requirements.
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('invalid first name')

    # Check Last Name matches requirements.
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('invalid last name')
    user=check_in_users("email",data.return_users(),email)
    user['name_first']=name_first
    user['name_last']=name_last
    data.updateByEmail(user,email)
    return {}

def user_profile_setemail(token, email):
    """Update the authorised user's email address

    Raises:
        1. InputError
            - Email entered is not a valid email using the method provided
            - Email address is already being used by another user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email_now = person.get('email')

    regex_email_check(email)

    user=check_in_users('email', data.return_users(), email)
    if user is not None:
        raise InputError('1')

    user = check_in_users('email', data.return_users(), email_now)

    user['email']=email
    data.updateByEmail(user,email_now)
    return {}


def user_profile_sethandle(token, handle_str):
    """Update the authorised user's handle (i.e. display name)

    Raises:
        1. InputError
            - handle_str must be between 3 and 20 characters
            - handle is already used by another user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')
    # handle_str must be between 3 and 20 characters
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError('1')
    user=check_in_users("email",data.return_users(),email)
    user['handle_str']=handle_str
    data.updateByEmail(user,email)
    return {}
