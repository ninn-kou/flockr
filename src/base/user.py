import data.data as data

import jwt
from   jwt import DecodeError

from base.auth import JWT_SECRET,check_in_users,regex_email_check, decode_token
from base.error import InputError

def user_profile(token, u_id):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except DecodeError:
        return {'is_success': False}

    user = check_in_users("u_id",data.return_users(),u_id)
    if user:
        return user
    else:
        raise InputError('not user')

def user_profile_setname(token, name_first, name_last):
    
    # decode the token
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')

    # Check first name matches requirements.
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('1')

    # Check Last Name matches requirements.
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('1')
    user=check_in_users("email",data.return_users(),email)
    user['name_first']=name_first
    user['name_last']=name_last
    data.updateByEmail(user,email)
    return {}

def user_profile_setemail(token, email):
    
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

    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')
    
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError('1')
    user=check_in_users("email",data.return_users(),email)
    user['handle_str']=handle_str
    data.updateByEmail(user,email)
    return {}
