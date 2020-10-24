'''
    Other functions to help testing
'''
import jwt
import data.data as data
from base.error import InputError, AccessError


def owner_from_token(token):
    ''' find owner from token'''
    # Adding in a little bit here to improve token handling
    with open('src/data/JWT_SECRET.txt', 'r') as file:
        jwt_secret = file.read()

    try:
        email = jwt.decode(token, jwt_secret, algorithms=['HS256']).get('email')
    except jwt.DecodeError as error:
        raise InputError("Couldn't Decode Token") from error

    au_id = None
    for i in data.return_users():
        if i['email'] == email:
            au_id = i

    # make sure user is actually returned
    if au_id is None:
        raise InputError

    return au_id

def clear():
    ''' clear the backend state '''

    data.clear_channels()
    data.clear_messages()
    data.clear_users()

def users_all(token):
    '''return all of the users list'''
    # check that token exists
    owner_from_token(token)
    users = data.return_users()
    return users

def admin_userpermission_change(token, u_id, permission_id):
    '''change the permission if the admin is a owner'''
    i = owner_from_token(token)                     # check that token exists

    users = data.return_users()
    found = 0
    for user in users:                          # Check that u_id is valid.
        if user['u_id'] == u_id:
            found = 1
            break
    if found != 1:
        raise InputError

    if permission_id != 1 or permission_id != 2:
        raise InputError                        # Check the permission_id.

    if i['permission_id'] != 1:                 # The admin is not a owner_num
        raise AccessError

    for user in users:                          # Find the user.
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id

    return {}

def search(token, query_str):
    '''search the message with the specific query_str'''
    # check that token exists
    user = owner_from_token(token)
    mes_list = []
    messages = data.return_messages()
    for i in messages:
        if user['u_id'] == messages['u_id']:    # focus on the messages which is joinned by the user
            if query_str in i['message']:
                mes_list.append(i)
    return mes_list
