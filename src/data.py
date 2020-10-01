# a collection of data structures used between programs


###########################################################################
"""
The User Data Structure
NOT SURE 

The Spec says to store it like this:
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

Issue is:
1. How to validate tokens? Are tokens stored in auth.py?
2. How to find each user in the list? Is u_id just used as a list address?

"""
users = []

# initialise the users list
def init_users():
    global users 
# append user to list
def append_users(user):
    users.append(user)

# add token to user
def add_token(token_object):
    for user in users:
        if token_object['u_id'] == user['u_id']:
            user['token'] = token_object['token']
            return user
    return None

# remove token from user
def remove_token(token):
    for user in users:
        if token == user['token']:
            user.pop('token', None)
            return user
    return None


##########################################################################################
"""
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
        'is public': True,
        'messages':[]  
    }
]

"""
channels = []

# initialise the channels list
def init_channels():
    global channels 

#add a channel in the channels list
def append_channels(channel):
    channels.append(channel)
