'''
    Other functions to help testing
'''

import data.data as data

def clear():
    ''' clear the backend state '''
    data.init_channels()

    data.channels = []
    data.clear_users()

def users_all(token):
    found = 0
    for user in data.users:                      # Check that token exists.
        if user['token'] == token:
            found = 1
            break
    if found != 1:
        raise InputError
    return data.users

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    set = []
    for channel in data.channels:
        for i in channel['messages']:
            if query_str in i['message']:
                set.append(i)
    '''            
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
    '''
    return set
