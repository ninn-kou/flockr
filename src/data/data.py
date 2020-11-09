'''
A collection of data structures used between programs

accessed from root/src

The approach taken in this file is terrible memory inefficient
However, it allows for basic persistent storage
'''

import json
import os
import glob
from PIL import Image
from flask import request

from base.error import InputError

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
                    'reacts': [{
                        'react_id': 1,
                        'u_ids':[],
                        'is_this_user_reacted': False
                    },],
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

def update_channel_user(user_id, loca, data):
    ''' append user to list '''

    # declare users outside
    channels = None

    # open current json file
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    for i in channels:
        for owner in i['owner_members']:
            if owner['u_id'] == user_id:
                owner[loca] = data
        for member in i['all_members']:
            if member['u_id'] == user_id:
                member[loca] = data

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

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

def clear_profiles():
    ''' delete user profile pictures '''
    files = glob.glob('src/data/profiles/*')
    for f in files:
        os.remove(f)

def save_image(image, u_id):
    ''' save an image in the profiles directory'''
    path = os.getcwd() + '/src/data/profiles/' 
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + str(u_id) + '.jpg'
    image.save(path)

def get_profile_photo_path(u_id):
    ''' returns a profile picture path, and url from the u_id '''

    path = os.getcwd() + '/src/data/profiles/' + u_id + '.jpg'

    # make sure path is valid
    try:
        Image.open(path)
    except Exception as e:
        raise InputError("You don't have a profile picture") from e
    return path

def get_port():
    ''' gets the current port that the server is running on '''

    # if the file doesn't exist
    path = os.getcwd() + '/src/data/port.json'
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump({'port': '0'}, file)

    with open(path, 'r') as file:
        port = json.load(file)['port']
        print(port)
    return port

def get_profile_photo_url(u_id):
    ''' returns the profile photo url '''
    '''
    # get the url route
    # assumes we're working with a localhost url
    url = 'http://127.0.0.1:{Port}/user/profile/photo/{U_id}'.format(
        Port = get_port(),
        U_id = u_id
    )
    path = os.getcwd() + '/src/data/profiles/' + str(u_id) + '.jpg'
    if not os.path.isfile(path):
        return ''
    return url
    '''
    return str(request.url_root) + 'user/profile/photo/' + str(u_id)
    #return str(request.url_root) + '/src/data/profiles/' + str(u_id) + '.jpg'
