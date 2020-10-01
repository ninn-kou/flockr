# this file is using for pytest of channel.py .
from channel import channel_invite, channel_details, channel_messages 
from channels import channels_create
from auth import auth_login, auth_register, auth_logout 
from error import InputError, AccessError
import  data 
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
    assert u_id1 ==  channel_test_details['all_members'][0]['u_id']
    assert u_id2 ==  channel_test_details['all_members'][1]['u_id']


def test_channel_invite_invalid_channelId():
    '''
    This test is using for check when the channel id we had is invalid
    inputError
    '''
    # create 2 users 
    user1 = auth_register("test5@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test5@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test6@test.com","check_test","steve","TAN")
    user2 = auth_login("test6@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    # testing for channel invite fuction for invalid channel id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id + 0xf, u_id2)


def test_channel_invite_invalid_userId():
    '''
    This test is using for check when the user id we had is invalid
    inputError
    '''
    # create 2 users 
    user1 = auth_register("test3@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test3@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test4@test.com","check_test","steve","TAN")
    user2 = auth_login("test4@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    # testing for channel invite fuction for invalid user id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id, u_id2 + 0xf)

def test_channel_non_member_invite():
    '''
    This test is using for check when the authorised user 
    is not already a member of the channel
    AccessError 
    '''
    # create 2 users and author people 
    user1 = auth_register("test11@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test11@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test22@test.com","check_test","steve","TAN")
    user2 = auth_login("test22@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    user3 = auth_register("test33@test.com","check_test","test","TAN")
    user3 = auth_login("test33@test.com","check_test")
    u_id3 = user3['u_id']
    u_token3 = user3['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']

    # testing for channel invite fuction for invalid token people.
    with pytest.raises(AccessError):
        channel_invite(u_token3,channel_test_id, u_id2)

def test_channel_repeate_invite():
    '''
    This test is using for check when the user has been in the program
    '''
    # create 2 users 
    user1 = auth_register("test41@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test41@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test42@test.com","check_test","steve","TAN")
    user2 = auth_login("test42@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test = channels_create(u_token1,"channel_test",True)
    channel_test_id = channel_test['channel_id']
    
    # invite people first time
    channel_invite(u_token1,channel_test_id,u_id2)
 
    # testing for invite people second time
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id, u_id2)
