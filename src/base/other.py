'''Some other useful functions'''
import data.data as data
from base.auth import decode_token
from base.error import InputError, AccessError


def owner_from_token(token):
    ''' find owner from token'''
    user = decode_token(token)
    if user is None:
        raise InputError("Couldn't Decode Token")

    return user

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
        raise InputError(description='The u_id is invalid.')

    if permission_id not in range(1, 3):        # Check the permission_id.
        raise InputError(description='The permission_id is invalid.')

    if i['permission_id'] != 1:                 # The admin is not a owner_num.
        raise AccessError(description='The admin is not a owner.')

    data.update_user(u_id, 'permission_id', permission_id)

    return {}

def search(token, query_str):
    '''search the message with the specific query_str'''
    # check that token exists
    user = owner_from_token(token)
    id_from = user.get('u_id')
    mes_list = []
    chan_list = []
    channels = data.return_channels()
    for i in channels:
        for j in i['all_members']:
            if id_from == j['u_id']:
                chan_list.append(i['channel_id'])
    
    messages = data.return_messages()
    for i in messages:
        if i['channel_id'] in chan_list:   # focus on the channels which is joinned by the user
            if query_str in i['message']:
                mes_list.append(i)                
    return mes_list
