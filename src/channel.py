import data
from error import InputError, AccessError
import channels
#############################################
######          channel_invite       ########
#############################################

# Xingyu TAN working on channel.py for channel_invite fuction
# 2 OCT 2020

"""
channel_invite()
the fuction Invites a user (with user id u_id) to join a channel with ID channel_id. 

RETURNS:
{}


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- the user id we had is invalid

- the user token is invalid

2. accessError
- the auth user is not in this channel.

3. repeated invite
- repeated invite one person who is already in.

"""
#############################################
######          help  fuction        ########
#############################################
# adding one member into the channel
def add_one_in_channel(channel_id,user):
    for i in data.channels:
        if i['channel_id'] == channel_id:
            i['all_members'].append(user)
            break
        
    return
# transfer the token into user id
def token_into_user_id(token):
    au_id = -1
    for i in data.users:
        if i['token'] == token:
            au_id = i['u_id']

    return au_id

# interation the whole channels, grab the channel we need
def find_channel(channel_id):
    
    answer = None
    for i in data.channels:
        if i['channel_id'] == channel_id:
            answer = i
            break
    
    return answer

# find user info by search one's id
def find_user(user_id):
    u_id = -1
    for i in data.users:
        if i['u_id'] == user_id:
            u_id = i
            break
    
    return u_id

# check one if in the channel already
def find_one_in_channel(channel, u_id):
    for i in channel['all_members']:
        if i['u_id'] == u_id:
            return True
    return False

def channel_invite(token, channel_id, u_id):
    # apply global variable we need
    data.init_channels()
    data.init_users()
    # case 1        // InputError
    # grab the au_id by transfer token
    auth_id = token_into_user_id(token)
    # the token id we had is invalid
    if auth_id == -1:
        raise(InputError)
    
    # case 2        // InputError
    # search the channel_id to check if the channel 
    # is in the channels list
    channel_got = find_channel(channel_id)
    # the channel id we had is invalid
    if channel_got == None:
        raise(InputError)

    # case 3        // InputError
    # check if the user is valid
    user = find_user(u_id)
    if user == -1:
        #the u_id is invalid
        raise(InputError)

    # case 4        // AccessError
    # check if the author is a member in this channel
    if find_one_in_channel(channel_got, auth_id) == False:
        raise(AccessError)

    # case 5
    # check if the user already in the channel, skip adding
    if find_one_in_channel(channel_got, u_id) == True:
        return {
    }
    

    # case 6
    #excluding all the error, then add the member
    # create new member struct
    user_struct = find_user(u_id)
    user = {
        'u_id': u_id,
        'name_first': user_struct['name_first'],
        'name_last': user_struct['name_last'],
    }

    # add the new member into channel
    add_one_in_channel(channel_id,user)
    
    return {
    }

#############################################
######         channel_details       ########
#############################################
# Xingyu TAN working on channel_details.py for channel_details fuction
# 2 Oct 2020

"""
channel_details()
Given a Channel with ID channel_id that the authorised user is part of

RETURNS:
provide basic details about the channel


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel is invalid
- the user_token is invalid


2. accessError
- the auth user is not in this channel.



"""
def channel_details(token, channel_id):
    # apply global variable we need
    data.init_channels()
    data.init_users()
    # case 1           //Input error
    # grab the au_id by transfer token
    auth_id = token_into_user_id(token)
    # the token id we had is invalid
    if auth_id == -1:
        raise(InputError)
    
    # case 2            // Input Error
    # search the channel_id to check if the channel 
    # is in the channels list
    channel_got = find_channel(channel_id)
    # the channel id we had is invalid
    if channel_got == None:
        raise(InputError)

    # case 3            // AccessError
    # check if the author is a member in this channel
    if find_one_in_channel(channel_got, auth_id) == False:
        raise(AccessError)

    return {
        'name': channel_got['name'],
        'owner_members':channel_got['owner'],
        'all_members': channel_got['all_members'],
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