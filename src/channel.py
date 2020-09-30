import data
from error import InputError, accessError
import channels
import random

# Xingyu TAN working on channel.py for channel_invite fuction
# 29 SEP 2020

"""
channel_invite()
the fuction Invites a user (with user id u_id) to join a channel with ID channel_id. 

RETURNS:
{}


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- the user id we had is invalid

2. accessError
- the auth user is not in this channel.

"""
######  help  fuction  ####
global users
global channels
def token_into_user_id(token):
    
   

    user_id = False
    for i in data.users:
        if i['token'] == token:
            user_id = i['u_id']
            break
    
    return user_id
    
def find_channel(channel_id):
    
    answer = False
    for i in data.channels:
        if i['channel_id'] == channel_id:
            answer = i
            break
    
    return answer

def find_user(user_id):
    

    u_id = False
    for i in data.users:
        if i['u_id'] == user_id:
            u_id = True
            break
    
    return user_id



def fin_one_in_channel(channel, u_id):
    for i in channel['all_members']


def channel_invite(token, channel_id, u_id):
    auth_id = token_into_user_id(token)
    if auth_id == False:
        #- the user id we had is invalid
        raise(InputError)

    channel = find_channel(channel_id)
    if channel == False:
        #- the channel id we had is invalid
        raise(InputError)

    user = find_user(u_id)
    if user == False:
        #the u_id is invalid
        raise(InputError)

    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
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
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }