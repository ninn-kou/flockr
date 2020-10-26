'''
Hao Ren
26 October, 2020
'''

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests

import pytest

import data.data as data
import base.other as other
import server.other_http as other_http

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

################################################################################

def test_clear(url):
    send_request('DELETE', url, 'other/clear', {})
################################################################################

def test_user_all(url):

    send_request('DELETE', url, 'other/clear', {})


    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    user3 = register_user(url, 'test3@example.com', 'emilyisshort3', 'Emily3', 'Luo3')
    user4 = register_user(url, 'test4@example.com', 'emilyisshort4', 'Emily4', 'Luo4')

    u1_token = user1['token']
    u2_token = user2['token']
    u3_token = user3['token']
    u4_token = user4['token']
    #i = other.users_all(u1_token)
    i = send_request('GET', url, 'other/users_all', {
        'token': user1.get('token'),
    })

    assert u1_token != u2_token != u3_token != u4_token
    assert len(i) == 4
    assert i[0]['email'] == 'test@example.com'
    assert i[1]['name_first'] == 'Emily2'
    assert i[2]['name_first'] == 'Emily3'
    assert i[3]['name_last'] == 'Luo4'
################################################################################

def test_userpermission_change(url):
    send_request('DELETE', url, 'other/clear', {})

    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')

    resp = send_request('POST', url, 'other/permission_change', {
        'token': user1.get('token'),
        'u_id': user2.get('u_id'),
        'permission_id': 1
    })
    #i = other.users_all(u1_token)
    i = send_request('GET', url, 'other/users_all', {
        'token': user1.get('token'),
    })
    i_user1 = i[0]
    i_user2 = i[1]
    assert i_user1['permission_id'] == 1
    assert i_user2['permission_id'] == 1

################################################################################


def test_search(url):

    send_request('DELETE', url, 'other/clear', {})


    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    channels = create_channels(url, user1.get('token'), True, 1)
    invite_user(url, user1, channels[0].get('channel_id'), user2)

    # get the sent messages in channel
    send_request('POST', url, 'meg/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "I am tired."
    })
    send_request('POST', url, 'meg/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "Great day."
    })
    send_request('POST', url, 'meg/send', {
        'token': user2.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "It sounds bad."
    })
    send_request('POST', url, 'meg/send', {
        'token': user2.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "If you are tired, you need go sleep."
    })

    resp = send_request('GET', url, 'other/search', {
        'token': user1.get('token'),
        'query_str': 'tired'
    })

    assert len(resp) == 1
    assert resp[0]['message'] == 'I am tired.'

