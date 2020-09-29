# this file is using for pytest of channel.py .
from channel import channel_invite, channel_details, channel_messages 
from channels import channels_create
from auth import auth_login, auth_register, auth_logout 
from error import InputError, AccessError
from data import *
import pytest

# Xingyu TAN working on channel_test.py for channel_invite fuction
# 29 SEP 2020

"""
channel_invite()
the fuction Invites a user (with user id u_id) to join a channel with ID channel_id. 

RETURNS:
none


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- the user id we had is invalid

2. accessError
- the auth user is not in this channel.

"""

def test_channel_invite_work():
    '''
    this test is using for check the fuction can work normally when no Errors bring.
    '''
    # create 2 users 
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    # testing for channel invite fuction
    channel_invite(u_token1,channel_test_id,u_id2)
    channel_test_details = channel_details(u_token1,channel_test_id)


    # Assuming we the fuction running correctly, then we do check the channel details 
    # expecially, the member infomation
    assert u_id1 ==  channel_test_details[['all_members'][0]['u_id']]
    assert u_id2 ==  channel_test_details[['all_members'][1]['u_id']]


def test_channel_invite_invalid_channelId():
    '''
    This test is using for check when the channel id we had is invalid
    inputError
    '''
    # create 2 users 
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    # testing for channel invite fuction for invalid channel id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id + 0xf, u_id2)