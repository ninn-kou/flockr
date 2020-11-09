'''functions for standup'''
import json
import time
import datetime
import threading
import data.data as data
import base.channel as channel_addowner
import base.message as message
from base.auth import decode_token
from base.error import InputError, AccessError

def token_into_user_id(token):
    """Transfer the token into the user id."""

    user = decode_token(token)
    if user is None:
        return -1
    au_id = user.get('u_id')

    return au_id
def token_into_name(token):
    """Transfer the token into the first name"""

    user = decode_token(token)
    if user is None:
        return ''
    au_fname = user.get('name_first')

    return au_fname
def find_channel(channel_id):
    """Interate the channels list by its id, return the channel we need."""
    answer = None
    for i in data.return_channels():
        if i['channel_id'] == channel_id:
            answer = i
            break
    return answer
def time_difference(timeint1, timeint2):
    '''find the difference between two timestr'''
    return int(timeint1 - timeint2)
def send_message_package(token, channel_id):

    m = find_channel(channel_id)['standup']['message_package']
    message.message_send(token, channel_id, m)
def standup_start(token, channel_id, length):
    auth_id = token_into_user_id(token)     # invalid token.
    if auth_id == -1:
        raise InputError(description='invalid token')

    c1 = find_channel(channel_id)  #  invalid channel_id.
    if c1 is None:
        raise InputError(description='invalid channel_id')
    
    now = datetime.datetime.utcnow()
    timestamp = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    '''
    if time_difference(c1['standup']['finish_time'], timestamp) > 0:
        raise InputError(description='An active standup is currently running in this channel')
    '''
    is_act = standup_active(token, channel_id).get('is_active')
    if is_act == True:
        raise InputError(description='An active standup is currently running in this channel')
    
    #Firstly, empty the message package
    data.message_package_empty(channel_id)

    #last_time = datetime.datetime.strptime(f_time,'%Y-%m-%d %H:%M:%S')
    next_time = timestamp + length

    data.change_finish_time(channel_id, next_time)

    #send the message at the end of the standup
    threading.Timer(length, send_message_package,(token, channel_id,)).start()

    return {
        'time_finish': next_time,
    }
def standup_active(token, channel_id):

    channel_got = find_channel(channel_id)  #  invalid channel_id.
    if channel_got is None:
        raise InputError(description='invalid channel_id')

    now = datetime.datetime.utcnow()
    timestamp = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    diff = time_difference(channel_got['standup']['finish_time'], timestamp)
    if diff > 0:
        is_active = True
        time_finish = channel_got['standup']['finish_time']
    else :
        is_active = False
        time_finish = None
    return {
        'is_active': is_active,
        'time_finish': time_finish,
    }
def standup_send(token, channel_id, message):
    c = find_channel(channel_id)
    if c is None:          #  invalid channel_id.
        raise InputError(description='invalid channel_id')

    now = datetime.datetime.utcnow()
    timestamp = int(now.replace(tzinfo=datetime.timezone.utc).timestamp()) #  no no active standup is runing in the given channel
    diff = time_difference(c['standup']['finish_time'], timestamp)
    if diff <= 0:
        raise InputError(description='No active standup is runing in this channel')

    if len(message) > 1000:                 #message is more than 1000 characters
        raise InputError(description='Message is more than 1000 characters')

    u1_id = token_into_user_id(token)       #the user is not a member of the channel
    l = []
    for i in c['all_members']:
        l.append(i['u_id'])
    if u1_id not in l:
        raise AccessError(description='The authorised user is not a member of the channel')

    u_fname = token_into_name(token)
    mess_send = u_fname + ': ' + message + '\n'       #in the form like "Steve: I like soft candy"
    data.message_package_add(channel_id, mess_send)

    return {}
