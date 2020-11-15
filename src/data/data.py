'''
A collection of data structures used between programs

accessed from root/src

The approach taken in this file is terrible memory inefficient
However, it allows for basic persistent storage
'''

import json
import os
import glob
import pickle
from PIL import Image
from flask import request

from src.base.error import InputError

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
            'password_reset': {
                'origin': datetime object,
                'code': ''
            }
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

    # open the pickle file
    path = os.getcwd() + '/src/data/users.p'

    # create file if it doesn't exist
    if not os.path.exists(path):
        with open(path, 'wb') as file:
            pickle.dump([], file)

    with open(path, 'rb') as file:
        users = pickle.load(file)

    # return the json information
    return users

def update_user(u_id, index, value):
    ''' update index of a user'''

    # declare users outside
    users = None

    # open current pickle file
    path = os.getcwd() + '/src/data/users.p'
    with open(path, 'rb') as file:
        users = pickle.load(file)

    for user in users:
        if user.get('u_id') == u_id:
            user[index] = value
    # write pickle to file
    with open('src/data/users.p', 'wb') as file:
        pickle.dump(users, file)

def append_users(user):
    ''' append user to list '''

    # declare users outside
    users = None

    # open current pickle file
    path = os.getcwd() + '/src/data/users.p'
    with open(path, 'rb') as file:
        users = pickle.load(file)

    # append the user
    users.append(user)

    # write json to file
    with open('src/data/users.p', 'wb') as file:
        pickle.dump(users, file)

def clear_users():
    ''' clear out users file '''

    # write json to file
    path = os.getcwd() + '/src/data/users.p'
    with open(path, 'wb') as file:
        pickle.dump([], file)

def updateByEmail(user, email):
    ''' update users by email '''

    path = os.getcwd() + '/src/data/users.p'
    with open(path, 'rb') as file:
        users = pickle.load(file)

    newusers = []
    for i in users:
        if i['email'] == email:
            i = user
        newusers.append(i)

    with open('src/data/users.p', 'wb') as file:
        pickle.dump(newusers, file)

def add_password_reset(u_id):
    pass


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
                    'profile_img_url'
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

    # if file doesn't exist, create it
    path = os.getcwd() + '/src/data/channels.json'
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file)

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

    # if file doesn't exist, create it
    path = os.getcwd() + '/src/data/messages.json'
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file)

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

def get_profile_photo_url(u_id):
    ''' returns the profile photo url '''
    path = os.getcwd() + '/src/data/profiles/' + str(u_id) + '.jpg'
    if not os.path.isfile(path):
        return ''
    return str(request.url_root) + 'user/profile/photo/' + str(u_id)

def change_finish_time(channel_id, time_int):
    '''change the finich time of the channel'''

    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #find the channel_id
    for i in channels:
        if i['channel_id'] == channel_id:
            #change the value
            i['standup']['finish_time'] = time_int

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def message_package_add(channel_id, message):
    '''add the message in the message_package'''

    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #find the channel_id
    for i in channels:
        if i['channel_id'] == channel_id:
            i['standup']['message_package'] += message

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def message_package_empty(channel_id):
    '''empty the message of the specific channel'''

    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #find the channel_id
    for i in channels:
        if i['channel_id'] == channel_id:
            i['standup']['message_package'] = ''

    # write json to file
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def return_password_reset_email():
    ''' returns the text of the password_reset_email.txt '''

    with open('src/data/password_reset_email.txt', 'r') as file:
        email = file.read()
        return email
    