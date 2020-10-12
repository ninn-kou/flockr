'''
A collection of data structures used between programs
'''

users = []

def init_users():
    '''
    initialise users as a global variable

    The User Data Structure
    Stored Like This:
    users = [
        user: {
            'u_id':
            'email': ''
            'name_first':'',
            'name_last':'',
            'handle_str': '',
            'token': '',
            'password': ''
        }
    ]
    '''
    global users

def append_users(user):
    ''' append user to list '''
    users.append(user)

def add_token(token_object):
    ''' add token to user '''
    for user in users:
        if token_object['u_id'] == user['u_id']:
            user['token'] = token_object['token']
            return user
    return None

def remove_token(token):
    ''' remove token from user '''
    for user in users:
        if token == user['token']:
            user.pop('token', None)
            return user
    return None


##########################################################################################

channels = []

def init_channels():
    ''' initialise the channels list

    the struct using for channel
    channels = [
        channel:  {
            'name': 'Hayden',
            'channel_id':
            'owner': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'is_public': True,
            'messages':[]
        }
    ]

    '''
    global channels

def append_channels(channel):
    ''' add a channel in the channels list '''
    channels.append(channel)
