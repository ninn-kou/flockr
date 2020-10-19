'''
Joseph Jeong 19 OCT 2020

After experimentation with Flask Blueprints, I'm setting up a server to allow channels.py
to interface with the frontend

'''

import re
from re import L
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests

import pytest

import data.data as data
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

def register_user_token(url, email, password, name_first, name_last):
    resp = requests.post(url + 'auth/register',
    json = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

    return json.loads(resp.text).get('token')

def test_create(url):
    ''' testing creation of channels '''
    # clear out the databases
    clear()

    # register a new user
    token = register_user_token(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')

    # create a new channel
    resp = requests.post(url + '/channels/create', 
    json = {
        'token': token,
        'name': 'wtv channel',
        'is_public': True
    })

    # load text
    text = json.loads(resp.text)

    # test that channel actually exists
    check = False
    for channel in data.return_channels():
        if channel.get('channel_id') == text.get('channel_id'):
            check = True
            break

    assert check

def create_channels(url, token, is_public, num):
    ''' create a specified number of channels '''
    # clear out the databases
    clear()

    channel_list = []

    for i in range(num):
        # add a channel
        channel_name = 'channel' + str(i)
        channel = json.loads(requests.post(url + '/channels/create', 
        json = {
            'token': token,
            'name': channel_name,
            'is_public': is_public
        })).text

        # add it to the channel list
        channel_list.append(channel)
    
    return channel_list

def test_listall(url):
    ''' testing channels_listall '''
    # clear out the databases
    clear()

    # register a new user
    token = register_user_token(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')

    # create a new channel
    channels = create_channels(url, token, True, 1)

    # list all channels
    list_all_obj = requests.get(url + 'channels/listall',
    json = {
        'token': token
    })

    # make sure that there is one channel each
    assert len(list_all_obj) == len(channels)

    # make sure that every channel is identified
    channel_list = []
    for channel in channels:
        for obj in list_all_obj:
            if channel.get('channel_id') == obj.get('channel_id'):
                # only adds it to channel_list if channels match
                channel_list.append(channel)
                break    
    assert len(channel_list) == len(channels)

def test_listall_two_users(url):
    ''' testing channels_listall with multiple users '''
    # clear out the databases
    clear()

    # register new tokens
    token1 = register_user_token(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    token2 = register_user_token(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    token3 = register_user_token(url, 'test3@example.com', 'emilyisshort3', 'Emily3', 'Luo3')

    # register new channels
    user1_channels = create_channels(url, token1, False, 10)
    user2_channels = create_channels(url, token2, True, 8)
    user3_channels = create_channels(url, token3, False, 7)

    # list all channels
    list_all_obj = requests.get(url + 'channels/listall',
    json = {
        'token': token1
    })

    # sum up all created channels
    created_channels = len(user1_channels) + len(user2_channels) + len(user3_channels)

    # check the correct number of channels is returned
    assert created_channels == len(list_all_obj)

def test_list(url):
    ''' testing channels_list'''
    # clear out the databases
    clear()

    # register new tokens
    token1 = register_user_token(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    token2 = register_user_token(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    token3 = register_user_token(url, 'test3@example.com', 'emilyisshort3', 'Emily3', 'Luo3')

    # register new channels
    user1_channels = create_channels(url, token1, False, 1)
    user2_channels = create_channels(url, token2, False, 2)
    public_channels = create_channels(url, token3, True, 1)

    # authorised channels for user1
    auth_channels1 = json.loads(requests.get(url + 'channels/list'), 
    json = {
        'token': token1
    }).text

    # user 1 should have 2 channels visible
    assert len(auth_channels1) == (len(user1_channels) + len(public_channels))

    # user 2 should have 3 channels visible
    assert len(auth_channels1) == (len(user2_channels) + len(public_channels))
    
    # user 3 should only have public channels visible
    assert len(auth_channels1) == len(public_channels)
