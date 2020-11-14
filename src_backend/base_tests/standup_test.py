'''tests for the standup'''
import time
import datetime
import src_backend.base.auth as auth
import src_backend.base.channels as channels
import pytest
import src_backend.data.data as data
from src_backend.base.error import InputError, AccessError
import src_backend.base.channel as channel
from src_backend.base.other import clear
import src_backend.base.standup as standup

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

def test_send_invalid_channel_id():
    '''test for checking the error when the channel_id is invalid'''
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
        standup.standup_send(u1_token, channel_tem,'')
        
    time.sleep(2)
        
def test_send_no_active_standup():
    '''test for checking the error when there is no standup running in the channel now'''
    clear()

    #create a user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')

    with pytest.raises(InputError):
        standup.standup_send(u1_token, channel_1_id,'')
        
def test_send_not_member():
    '''test for accessing the error when the user is not the member in the channel'''
    clear()

    #create two users and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    user2 = auth.auth_register('234@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('234@test.com', 'password')
    u2_token = user2['token']
    
    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 1)
    
    with pytest.raises(AccessError):
        standup.standup_send(u2_token, channel_1_id,'')
    
    time.sleep(1.5)
    
def test_standup_long_message():
    '''test for inputing the error that the message is more than 1000 words'''
    clear()

    #create a user and take its id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
   
    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 1)
    
    #create a string with more than 1000 words
    message_test = "aaaaa"
    message_test = 3000 * message_test
    with pytest.raises(InputError):
        standup.standup_send(u1_token, channel_1_id, message_test)
        
    time.sleep(1.5)
    
def test_standup_send():
    '''test for the send function'''
    clear()

    #create three user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN1', 'LastN1')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    user2 = auth.auth_register('234@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('234@test.com', 'password')
    u2_token = user2['token']
    u2_id = user2['u_id']
    user3 = auth.auth_register('34@test.com', 'password', 'FirstN3', 'LastN3')
    user3 = auth.auth_login('34@test.com', 'password')
    u3_token = user3['token']
    u3_id = user3['u_id']
   
    #create a channel by user1 in channels and invite other two users
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    channel.channel_invite(u1_token, channel_1_id, u2_id)
    channel.channel_invite(u1_token, channel_1_id, u3_id)
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 1)
    
    standup.standup_send(u1_token, channel_1_id, 'WE')
    standup.standup_send(u2_token, channel_1_id, 'ARE')
    standup.standup_send(u3_token, channel_1_id, 'FRIENDS')
    
    channels_t = data.return_channels()
    m_l = channels_t[0]['standup']['message_package']
    
    assert m_l == 'FirstN1: WE\nFirstN2: ARE\nFirstN3: FRIENDS\n'
    
    time.sleep(2)

def test_standup_all_message_sent_out():
    '''check if the message in message package has been sent out after ending'''
    clear()

    #create three user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN1', 'LastN1')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    user2 = auth.auth_register('234@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('234@test.com', 'password')
    u2_token = user2['token']
    u2_id = user2['u_id']
    user3 = auth.auth_register('34@test.com', 'password', 'FirstN3', 'LastN3')
    user3 = auth.auth_login('34@test.com', 'password')
    u3_token = user3['token']
    u3_id = user3['u_id']
   
    #create a channel by user1 in channels and invite other two users
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    channel.channel_invite(u1_token, channel_1_id, u2_id)
    channel.channel_invite(u1_token, channel_1_id, u3_id)
    #start a standup
    standup.standup_start(u1_token, channel_1_id, 3)
    
    standup.standup_send(u1_token, channel_1_id, 'WE')
    standup.standup_send(u2_token, channel_1_id, 'ARE')
    standup.standup_send(u3_token, channel_1_id, 'FRIENDS')
    #sleep until the standup ending
    time.sleep(5)
    channels_t = data.return_channels()

    m_c = channels_t[0]['message'][0]
    #check the message has been sent
    assert m_c['u_id'] == u1_id
    assert m_c['message'] == 'FirstN1: WE\nFirstN2: ARE\nFirstN3: FRIENDS\n'
    
def test_standup_all_message_sent_out_twice():
    '''check if the message in message package has been sent out after ending'''
    clear()

    #create three user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN1', 'LastN1')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    user2 = auth.auth_register('234@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('234@test.com', 'password')
    u2_token = user2['token']
    u2_id = user2['u_id']
    user3 = auth.auth_register('34@test.com', 'password', 'FirstN3', 'LastN3')
    user3 = auth.auth_login('34@test.com', 'password')
    u3_token = user3['token']
    u3_id = user3['u_id']
   
    #create a channel by user1 in channels and invite other two users
    channel_1_id = channels.channels_create(u1_token,'team',True).get('channel_id')
    channel.channel_invite(u1_token, channel_1_id, u2_id)
    channel.channel_invite(u1_token, channel_1_id, u3_id)
    #start a standup by u1
    standup.standup_start(u1_token, channel_1_id, 3)
    
    standup.standup_send(u1_token, channel_1_id, 'WE')
    standup.standup_send(u2_token, channel_1_id, 'ARE')
    standup.standup_send(u3_token, channel_1_id, 'FRIENDS')
    #sleep until the standup ending
    time.sleep(4)
    
    #start another standup by u2
    standup.standup_start(u2_token, channel_1_id, 3)
    
    standup.standup_send(u1_token, channel_1_id, 'SHE')
    standup.standup_send(u2_token, channel_1_id, 'HE')
    standup.standup_send(u3_token, channel_1_id, 'THEY')
    
    #sleep until the standup ending
    time.sleep(4)
    channels_t = data.return_channels()    
    m_c_1 = channels_t[0]['message'][1]
    m_c_2 = channels_t[0]['message'][0]
    #check the message has been sent
    assert m_c_1['u_id'] == u1_id
    assert m_c_2['u_id'] == u2_id
    assert m_c_1['message'] == 'FirstN1: WE\nFirstN2: ARE\nFirstN3: FRIENDS\n'
    assert m_c_2['message'] == 'FirstN1: SHE\nFirstN2: HE\nFirstN3: THEY\n'
    
    #check the message package
    assert channels_t[0]['standup']['message_package'] == 'FirstN1: SHE\nFirstN2: HE\nFirstN3: THEY\n'

