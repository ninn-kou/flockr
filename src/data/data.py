'''
A collection of data structures used between programs

accessed from root/src

The approach taken in this file is terrible memory inefficient
However, it allows for basic persistent storage
'''

import json

def users_notes():
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
            'password': '',
            'session_secret': '',
            'permission_id': '',
            'profile_img_url':'',
        }
    ]

    - session_secret needs to be implemented
    - auth_register needs to be changed, so that the very first user has p_id = 1
    everyone else is created p_id = 2
    - need to make token thing
    '''

def return_users():
    ''' return all the users in the file '''

    # declare users outside
    users = None

    # open the json file
    with open('src/data/users.json', 'r') as file:
        users = json.load(file)

    # return the json information
    return users

def update_user(u_id, index, value):
    ''' update index of a user'''

    # declare users outside
    users = None

    # open current json file
    with open('src/data/users.json', 'r') as file:
        users = json.load(file)

    for user in users:
        if user.get('u_id') == u_id:
            user[index] = value
            break

    # write json to file
    with open('src/data/users.json', 'w') as file:
        json.dump(users, file)

def append_users(user):
    ''' append user to list '''

    # declare users outside
    users = None

    # open current json file
    with open('src/data/users.json', 'r') as file:
        users = json.load(file)

    # append the user
    users.append(user)

    # write json to file
    with open('src/data/users.json', 'w') as file:
        json.dump(users, file)

def clear_users():
    ''' clear out users file '''

    # write json to file
    with open('src/data/users.json', 'w') as file:
        json.dump([], file)

def updateByEmail(user, email):
    with open('src/data/users.json', 'r') as file:
        users = json.load(file)
    newusers = []
    for i in users:
        if i['email'] == email:
            i = user
        newusers.append(i)
    with open('src/data/users.json', 'w') as file:
        json.dump(newusers, file)

##########################################################################################

def return_channels():
    ''' return the channels list

    the struct using for channel
    channels = [
        {
            'name': 'Hayden',
            'channel_id':
            'owner_members': [
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
            'message':[
                {
                    'message_id': 1,
                    'channel_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                    'reacts': false,
                    'is_pinned': false
                    ''
                },
            ]
        }
    ]


    '''

    # declare users outside
    channels = None

    # open the json file
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    # return the json information
    return channels

def append_channels(channel):
    ''' append user to list '''

    # declare users outside
    channels = None

    # open current json file
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    # append the user
    channels.append(channel)

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def replace_channels(channels):
    ''' replace persistent database with input'''

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def clear_channels():
    ''' clear out channels file '''

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump([], file)


def return_messages():
    ''' return the messages list

    the struct using for messages
    'messages':[
        {
            'message_id': 1,
            'channel_id': 1,
            'u_id': 1,
            'message': 'Hello world',
            'time_created': 1582426789,
        },
    ]

    '''
    # declare messages outside
    messages = None

    # open the json file
    with open('src/data/messages.json', 'r') as file:
        messages = json.load(file)

    # return the json information
    return messages

def insert_messages(message):
    ''' insert_messages to list '''

    # declare message outside
    messages = None

    # open current json file
    with open('src/data/messages.json', 'r') as file:
        messages = json.load(file)

    # append the user
    messages.insert(0, message)

    # write json to file
    with open('src/data/messages.json', 'w') as file:
        json.dump(messages, file)

def replace_messages(message):
    ''' replace persistent database with input'''

    # write json to file
    with open('src/data/messages.json', 'w') as file:
        json.dump(message, file)

def clear_messages():
    ''' clear out channels file '''

    # write json to file
    with open('src/data/messages.json', 'w') as file:
        json.dump([], file)