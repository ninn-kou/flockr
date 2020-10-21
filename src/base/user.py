import data.data as data

import jwt
from   jwt import DecodeError

from base.auth import JWT_SECRET,check_in_users,regex_email_check
from base.error import InputError

def user_profile(token, u_id):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except DecodeError:
        return {'is_success': False}
    try:
        u_id=int(u_id)
    except Exception:
        raise InputError('terrible uid')
    user=check_in_users("u_id",data.return_users(),u_id)
    if user:
        return user
    else:
        raise InputError('not user')

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }