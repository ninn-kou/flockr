"""All other useful functions used in the flockr."""

import src.data.data as data
from src.base.auth import decode_token
from src.base.error import InputError, AccessError

def owner_from_token(token):
    """Find owner from token."""
    user = decode_token(token)
    if user is None:
        raise InputError("Couldn't Decode Token")

    return user

def clear():
    """Clear the backend state."""
    data.clear_channels()
    data.clear_messages()
    data.clear_users()
    data.clear_profiles()

def users_all(token):
    """Return all of the users list."""
    # check that token exists
    owner_from_token(token)
    users = data.return_users()
    list_users = []

    for i in users:
        user = {
            'u_id': i['u_id'],
            'email': i['email'],
            'name_first': i['name_first'],
            'name_last': i['name_last'],
            'handle_str': i['handle_str'],
            'profile_img_url': '',
        }
        list_users.append(user)

    return {
        'users': list_users
    }


def admin_userpermission_change(token, u_id, permission_id):
    """Change the permission if the admin is a owner."""
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
    """Search the message with the specific query_str."""
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

    # make the query string to all_lower
    # this will make query case insensitive
    query_str = query_str.lower()
    # make query string to ignore whitespace
    query_str = "".join(query_str.split())

    messages = data.return_messages()
    for i in messages:
        if i['channel_id'] in chan_list:   # focus on the channels which is joinned by the user
            # make the message lowercase and ignoring whitespace
            working_msg = "".join(i['message'].lower().split())

            if query_str in working_msg:
                added_message = {
                    "message_id" : i['message_id'],
                    "u_id" : i['u_id'],
                    "message" : i['message'],
                    "time_created" : i['time_created'],
                    'reacts': i['reacts'],
                    'is_pinned': i['is_pinned'],
                }
                mes_list.append(added_message)
    for msg in mes_list:
        msg['reacts'][0]['is_this_user_reacted'] = False
        if id_from in msg['reacts'][0]['u_ids']:
            msg['reacts'][0]['is_this_user_reacted'] = True

    return {
        'messages': mes_list
    }
