'''
Joseph Jeong 15 OCT 2020

After experimentation with Flask Blueprints, I'm setting up a server to allow auth.py
to interface with the frontend

'''

import re
from re import L
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import string
import random

import pytest

import data.data as data
from base_tests.channel_test import msg_send
from base.other import clear

# copy-pasted this straight out of echo_http_test.py
# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    ''' start server and create url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def send_request(method, url, url_extension, json_obj):
    ''' function to help send requests more easily'''
    resp = None
    if method == 'GET':
        resp = requests.get(url + url_extension, json = json_obj)
    elif method == 'POST':
        resp = requests.post(url + url_extension, json = json_obj)

    return json.loads(resp.text)

def register_user(url, email, password, name_first, name_last):
    ''' register a new user '''
    return send_request('POST', url, 'auth/register', {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

def create_channels(url, token, is_public, num):
    ''' create a specified number of channels '''

    channel_list = []

    for i in range(num):
        # add a channel
        channel_name = 'channel' + str(i)
        channel = send_request('POST', url, 'channels/create', {
            'token': token,
            'name': channel_name,
            'is_public': is_public
        })

        # add it to the channel list
        channel_list.append(channel)
    
    return channel_list

def invite_user(user1, channel_id, user2):
    ''' user1 invites user2 to channel '''
    send_request('POST', url, 'channel/invite', {
        'token': user1.get('token'),
        'channel_id': channel_id,
        'u_id': user2.get('u_id')
    })

def create_random_message(characters, i):
    ''' create a random message '''
    length = random.randint(0, 50)
    msg = ""

    # create a rando mmessage
    for _ in range(length):
        character = random.choice(characters)
        msg += character
    
    # add number to end of message
    # ensures messages are unique
    msg += str(i)

    return msg

def send_random_messages(channel_id, num):
    ''' send a number of random messages'''
    # characters to use in the message
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    # find which channels there are
    focus_channel = None
    channels = data.return_channels()
    for channel in channels:
        if channel['channel_id'] == channel_id:
            focus_channel = channel
            break
    
    # add random messages to list
    messages = []
    for i in range(num):
        msg = create_random_message(characters, i)
        return_message = {
        'message_id': i,
        'u_id': random.choice(focus_channel['all_members'])['u_id'],
        'message': msg,
        'time_created': i,
        }
        messages.append(return_message)
    
    # add the message to channel
    for i in channels:
        if i['channel_id'] == channel_id:
            i['messages'] = messages
            break
    
    # add that to persistent storage
    data.replace_channels(channels)

    return messages

def test_invite(url):
    ''' testing channel_invite requests '''

    # clear out the databases
    clear()

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # create second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')

    # invite user2
    invite_user(user1, channels[0].get('channel_id'), user2)

    # check if both members are in channel
    check = False
    for channel in data.return_channels():
        if channel['channel_id'] == channels[0]['channel_id']:
            check = set(channel['all_members']) == set(channels[0]['all_members'])
            break
    assert check

def test_details(url):
    ''' testing channel_details requests '''

    # clear out the databases
    clear()

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(user1, channels[0].get('channel_id'), user2)

    u_id_list = [user1.get('u_id'), user2.get('u_id')]

    # get channel details
    details = send_request('GET', url, 'channel/details', {
        'token': user1['token'],
        'channel_id': channels[0]['channel_id']
    })

    # check channel name
    assert details.get('name') == channels[0]['name']
    # check owner members
    assert details.get('owner_members')['u_id'] == user1['u_id']
    # check all members
    member_ids = []
    for member in details.get('all_members'):
        member_ids.append(member['u_id'])
    assert set(member_ids) == set(u_id_list)

def test_messages(url):
    ''' testing channel_messages requests '''

    # clear out the databases
    clear()

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(user1, channels[0].get('channel_id'), user2)

    # create and send 150 messages
    # in order of time from earliest to latest
    # will have the largest index as the latest message
    max_index = 149
    messages = send_random_messages(channels.get('channel_id'), max_index + 1)

    # get the sent messages in channel
    start_index = 0
    interval = 50
    resp = send_request('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels.get('channel_id'),
        'start': start_index
    })
    
    # make sure the messages are the same
    assert (set(resp['messages'][start_index: start_index + interval]) 
        == set(messages[max_index - start_index: max_index - (start_index + interval)]))

def test_leave(url):
    ''' testing channel_leave requests '''

    # clear out the databases
    clear()

def test_join(url):
    ''' testing channel_join requests '''

    # clear out the databases
    clear()

def test_addowner(url):
    ''' testing channel_join requests '''

    # clear out the databases
    clear()

def test_removeowner(url):
    ''' testing channel_removeowner requests '''

    # clear out the databases
    clear()