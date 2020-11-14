'''tests for the http of the standup'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
from datetime import timezone, datetime
import pytest

import src_backend.data.data as data
from src_backend.base.other import clear


# copy-pasted this straight out of echo_http_test.py
# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    ''' start server and create url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
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
    url_time = url + url_extension
    if method == 'GET':
        resp = requests.get(url_time, json=json_obj)
    elif method == 'POST':
        resp = requests.post(url_time, json=json_obj)
    elif method == 'DELETE':
        resp = requests.delete(url_time, json=json_obj)
    elif method == 'PUT':
        resp = requests.put(url_time, json=json_obj)
    return json.loads(resp.text)

def send_request_params(method, url, url_extension, json_obj):
    ''' function to help send requests more easily'''
    resp = None
    url_time = url + url_extension
    if method == 'GET':
        resp = requests.get(url_time, params=json_obj)
    elif method == 'POST':
        resp = requests.post(url_time, params=json_obj)
    elif method == 'DELETE':
        resp = requests.delete(url_time, params=json_obj)
    elif method == 'PUT':
        resp = requests.put(url_time, params=json_obj)
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
        channel_id = send_request('POST', url, 'channels/create', {
            'token': token,
            'name': channel_name,
            'is_public': is_public
        }).get('channel_id')

        # add the channel object, not just the channel itself
        for channel in data.return_channels():
            if channel['channel_id'] == channel_id:
                # add it to the channel list
                channel_list.append(channel)

    return channel_list

def invite_user(url, user1, channel_id, user2):
    ''' user1 invites user2 to channel '''
    send_request('POST', url, 'channel/invite', {
        'token': user1.get('token'),
        'channel_id': channel_id,
        'u_id': user2.get('u_id')
    })

def check_in_index(url, user1, user2, channel, index):
    ''' checks if user2 is in index from user1's perspective '''
    # find out channel from user1's perspective
    details = send_request('GET', url, 'channel/details', {
        'token': user1['token'],
        'channel_id': channel['channel_id']
    })

    # check if user2 is in channel
    check = False
    for member in details.get(index):
        if member.get('u_id') == user2.get('u_id'):
            check = True
            break
    return check
###################################################################

def test_standup_start_http(url):
    '''test for the start of the standup'''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)
    
    #start a standup and get the return item
    resp = send_request('POST', url, 'standup/start', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'length': 2
    })
    
    #get the current time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    
    assert resp['time_finish'] == timestamp + 2
    sleep(2)
    
def test_standup_active_http(url):
    '''test for the is_active funtion of the standup'''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)
    '''
    resp1 = send_request('GET', url, 'standup/active', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
    })
    '''
    resp1 = json.loads(requests.get(url + '/standup/active', 
    params = {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
    }).text)    
    assert resp1['is_active'] == False
    
    #start a standup
    send_request('POST', url, 'standup/start', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'length': 1
    })
    resp2 = json.loads(requests.get(url + '/standup/active', 
    params = {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
    }).text)    
    assert resp2['is_active'] == True
    sleep(2)
    
def test_standup_send_http(url):
    '''test for the is_active funtion of the standup'''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)
    
    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)
    
    #start a standup and get the return item
    send_request('POST', url, 'standup/start', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'length': 3
    })
    #send message to the standup
    send_request('POST', url, 'standup/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': 'We'
    })
    send_request('POST', url, 'standup/send', {
        'token': user2.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': 'are'
    })
    send_request('POST', url, 'standup/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': 'students'
    })
    sleep(3)
    #get the messages list
    resp = send_request_params('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'start': 0
    })
    assert resp['messages'][0]['message'] == 'Emily: We\nEmily2: are\nEmily: students\n'

