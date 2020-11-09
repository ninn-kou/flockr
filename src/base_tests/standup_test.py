'''tests for the standup'''
import random
import string
import time
import datetime
import base.auth as auth
import base.channels as channels
import pytest
import data.data as data
from base.error import InputError, AccessError
import base.channel as channel
from base.other import clear
import base.standup as standup

def time_difference(timeint1, timeint2):
    '''find the difference between two timestr'''
    
    return timeint1 - timeint2
    
def test_token_to_user():
    '''test for the token_to_user function'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    
    assert standup.token_into_user_id(u1_token) != -1
    
def test_token_into_name():
    '''test for the transformation from token into first name'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    
    assert standup.token_into_name(u1_token) == 'FirstN'
    
def test_find_channel():
    '''test for the find_channel function'''
    clear()
    
    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create two channels by user1 in channels and return their channel id
    channels.channels_create(u1_token,'team',True)
    channel_2_id = channels.channels_create(u1_token,'team1',True).get('channel_id')

    
    d = standup.find_channel(channel_2_id)
    assert d['name'] == 'team1'
    
def test_standup_start_invalid_token():
    '''check the error input when the token is invalid'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    token_tem = u1_token + ' '
    with pytest.raises(InputError):
        standup.standup_start(token_tem, channel_1_id, 1)

def test_standup_start_invalid_channel_id():
    '''check the error input when the channel_id is invalid'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    channel_tem = channel_1_id + 1
    with pytest.raises(InputError):
        standup.standup_start(u1_token, channel_tem, 1)
        
def test_standup_start_occupied():
    '''check the error input when an active standup has been started'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    standup.standup_start(u1_token, channel_1_id, 3)

    time.sleep(2)  #sleep for 2s for test
    
    with pytest.raises(InputError):
        standup.standup_start(u1_token, channel_1_id, 1)
        
    time.sleep(2)
    
def test_standup_start():
    '''test for start function'''
    clear()

    #create a user and take the token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    channels_t = data.return_channels()
    
    time_str1 = channels_t[0]['standup']['finish_time']     #get the finish time before the standup starts
    
    now = datetime.datetime.utcnow()
    timestamp = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    time_str3 = timestamp
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 1)
    
    channels_t = data.return_channels()
    time_str2 = channels_t[0]['standup']['finish_time']     #get the finish time after the standup starts
    
    assert time_difference(time_str1, time_str2) < 0
    assert time_difference(time_str2, time_str3) == 1
    
    time.sleep(2)

def test_standup_active_invalid_channel_id():
    '''test for error that the channel_id is invalid'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 1)
    
    channel_tem = channel_1_id + 1
    with pytest.raises(InputError):
        standup.standup_active(u1_token, channel_tem)
        
    time.sleep(2)
        
def test_standup_active():
    '''test for the active function'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create two channels by user1 in channels and return their channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    channel_2_id = channels.channels_create(u1_token,'team1',True).get('channel_id')
    
    standup_1 = standup.standup_start(u1_token, channel_1_id, 2)      #start a standup in channel_1 but not in channel_2_id
    
    res1 = standup.standup_active(u1_token, channel_1_id)
    assert res1['is_active'] == True
    assert res1['time_finish'] == standup_1['time_finish']
    
    res2 = standup.standup_active(u1_token, channel_2_id)
    assert res2['is_active'] == False
    assert res2['time_finish'] == None
    
    time.sleep(2.5)

