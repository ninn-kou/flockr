# this file is using for pytest of channel.py .
from channel import channel_invite, channel_details, channel_messages 
from channels import channels_create
from auth import auth_login, auth_register, auth_logout 
from error import InputError, AccessError
from data import *
import pytest
from message import message_send



# Xingyu TAN working on channel_test.py for channel_messages fuction
# 29 SEP 2020

"""
channel_messages()
Given a Channel with ID channel_id that the authorised user is part of channel, and return no more than 50 messages

RETURNS:
-1 : for no more message after start
0< number && number <= 50: exist messages after start and no more than 50 messages.
50 : the exist messages after start more than 50, just return the top 50 ones.


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- start is greater than the total number of messages in the channel

2. accessError
- the auth user is not in this channel.

"""
def test_inputError_channel_message_channelId_start_invalid():
    '''
    This test is using for check when channel id we had is invalid
    inputError
    '''
    # create 2 users 
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']
    channel_invite(u_token1,channel_test_id, u_id2)
    
    # testing for channel message fuction for invalid message start
    with pytest.raises(InputError):
        channel_messages(u_token1,channel_test_id, 10)

def test_inputError_channel_message_invalid_channelId():
    '''
    This test is using for check when channel id we had is invalid
    inputError
    '''
    # create 2 users 
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']
    channel_invite(u_token1,channel_test_id, u_id2)

    message_send(u_token1, channel_test_id, 'hi steve')

    
    # testing for channel message fuction for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages(u_token1,channel_test_id + 0xf, 0)

def test_channel_non_member_call_details():
    '''
    This test is using for check when the authorised user 
    is not already a member of the channel
    AccessError 
    '''
    # create 2 users and author people 
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_token2 = user2['token']

    user3 = auth_register("test3@test.com","check_test","test","TAN")
    user3 = auth_login("test3@test.com","check_test")
    u_token3 = user3['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    #adding some message in the channel
    message_send(u_token1, channel_test_id, 'hi steve')

    # testing for channel invite fuction for invalid token people.
    with pytest.raises(AccessError):
        channel_messages(u_token3,channel_test_id,0)



