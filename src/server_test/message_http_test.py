'''
this is fucntion writeng for message.py to test all the normall cases
Writen by Xingyu Tan 26/10/2020
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
from datetime import timezone, datetime
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
def test_message_send_works(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)


    # get the sent messages in channel
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01"
    })
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_02"
    })
    # get the sent messages in channel

    resp = send_request_params('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'start': 0
    })

    # make sure the messages are the same
    assert resp['messages'][0]['message'] == "test_msg_02"
    assert resp['messages'][1]['message'] == "test_msg_01"
###################################################################

def test_message_remove(url):
    '''
    test for messsage_remove
    Test whether the msg can be sent normally
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)


    # get the sent messages in channel
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01"
    })
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_02"
    })
    message_test_id = send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_03"
    })['message_id']

    # 1. remove the message we need
    send_request('DELETE', url, 'message/remove', {
        'token': user1.get('token'),
        'message_id': message_test_id,
    })

    # get the sent messages in channel
    resp = send_request_params('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'start': 0
    })

    # make sure the messages are the same
    assert resp['messages'][0]['message'] == "test_msg_02"
    assert resp['messages'][1]['message'] == "test_msg_01"
###################################################################

def test_message_edit(url):
    '''
    test for message edit
    Test whether the msg can be sent normally
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)


    # get the sent messages in channel
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01"
    })
    send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_02"
    })
    message_test_id = send_request('POST', url, 'message/send', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_03"
    })['message_id']

    # 1. edit the message we need
    send_request('PUT', url, 'message/edit', {
        'token': user1.get('token'),
        'message_id': message_test_id,
        'message': 'test edit msg'
    })

    # get the sent messages in channel
    resp = send_request_params('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'start': 0
    })

    # make sure the messages are the same
    assert resp['messages'][0]['message'] == "test edit msg"
    assert resp['messages'][1]['message'] == "test_msg_02"
    assert resp['messages'][2]['message'] == "test_msg_01"

###################################################################
def test_message_sendlater_works(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5
    # get the sent messages in channel
    check_id = send_request('POST', url, 'message/sendlater', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01",
        'time_sent':time_furture
    })
    # get the sent messages in channel

    resp = send_request_params('GET', url, 'channel/messages', {
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'start': 0
    })

    # make sure the messages are the same
    assert resp['messages'][0]['message'] == "test_msg_01"
    assert resp['messages'][0]['time_created'] == time_furture
    assert resp['messages'][0]['message_id'] == check_id['message_id']


###################################################################
def test_message_sendlater_when_time_in_past(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    when the sent time is in the past
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp - 10
    # get the sent messages in channel
    response = requests.post(f"{url}message/sendlater", json={
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01",
        'time_sent':time_furture
    })
    assert response.status_code == 400

###################################################################
def test_message_sendlater_when_invalid_tokenid(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    when the sent time is in the past
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 10
    # get the sent messages in channel
    response = requests.post(f"{url}message/sendlater", json={
        'token': user1.get('token') + 'abc',
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01",
        'time_sent':time_furture
    })
    assert response.status_code == 400

###################################################################
def test_message_sendlater_when_invalid_channelid(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    when the sent time is in the past
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # invite second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    invite_user(url, user1, channels[0].get('channel_id'), user2)

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 10
    # get the sent messages in channel
    response = requests.post(f"{url}message/sendlater", json={
        'token': user1.get('token'),
        'channel_id': channels[0].get('channel_id') + 0xf,
        'message': "test_msg_01",
        'time_sent':time_furture
    })
    assert response.status_code == 400


###################################################################
def test_message_sendlater_access_error_token_people_wrong(url):
    '''
    test for message_send
    Test whether the msg can be sent normally
    when the sent time is in the past
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register a new user and create a new channel
    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')
    channels = create_channels(url, user1.get('token'), True, 1)

    # register second user to invite
    user2 = register_user(url, 'test2@example.com', 'emilyisshort2', 'Emily2', 'Luo2')
    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 10
    # get the sent messages in channel
    response = requests.post(f"{url}message/sendlater", json={
        'token': user2.get('token'),
        'channel_id': channels[0].get('channel_id'),
        'message': "test_msg_01",
        'time_sent':time_furture
    })
    assert response.status_code == 400
