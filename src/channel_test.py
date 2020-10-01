# this file is using for pytest of channel.py .
from channel import channel_invite, channel_details, channel_messages
from channels import channels_create
from auth import auth_login, auth_register, auth_logout 
from error import InputError, AccessError
import data 
import pytest
import other
from message import message_send



#########################################################################
#
#                     test for channel_invite function
#
##########################################################################
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
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)


    # testing for channel invite fuction
    channel_invite(u_token1,channel_test_id,u_id2)



    # Assuming we the fuction running correctly, then we do check the channel details 
    # expecially, the member infomation
    channel_member_num = 0
    data.init_channels()
    
    for i in data.channels:
        if i['channel_id'] == channel_test_id:
            channel_member_num = len(i['all_members'])
            break
    
    # check the totoal members number is 2
    assert channel_member_num ==2
    # check the diff people info correct
    assert u_id1 ==  i['all_members'][0]['u_id']
    assert u_id2 ==  i['all_members'][1]['u_id']

def test_channel_repeate_invite():
    '''
    This test is using for check when the user has been in the program
    when repeat invite, just skip it.
    '''

    # create 2 users 
    other.clear()

    user1 = auth_register("test41@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test41@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test42@test.com","check_test","steve","TAN")
    user2 = auth_login("test42@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    
    # invite people first time
    channel_invite(u_token1,channel_test_id,u_id2)
 
    # testing for invite people second time
    channel_invite(u_token1,channel_test_id, u_id2)

    channel_member_num = 0
    data.init_channels()
    
    for i in data.channels:
        if i['channel_id'] == channel_test_id:
            channel_member_num = len(i['all_members'])
            break
    
    # check the totoal members number is still 2
    assert channel_member_num ==2

 
##########  test for input error #################

def test_channel_invite_invalid_channelId_input_error():
    '''
    This test is using for check when the channel id we had is invalid
    inputError
    '''
    # create 2 users 
    other.clear()

    user1 = auth_register("test5@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test5@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test6@test.com","check_test","steve","TAN")
    user2 = auth_login("test6@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)
    

    # testing for channel invite fuction for invalid channel id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id + 0xf, u_id2)


def test_channel_invite_invalid_userId_input_error():
    '''
    This test is using for check when the user id we had is invalid
    inputError
    '''
    # create 2 users 
    other.clear()

    user1 = auth_register("test3@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test3@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test4@test.com","check_test","steve","TAN")
    user2 = auth_login("test4@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)


    # testing for channel invite fuction for invalid user id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id, u_id2 + 0xf)

#################### test for access error #####################
def test_channel_non_member_invite():
    '''
    This test is using for check when the authorised user 
    is not already a member of the channel
    AccessError 
    '''
    # create 2 users and author people 
    other.clear()

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
    channel_test_id = channels_create(u_token1,"channel_test",True)


    # testing for channel invite fuction for invalid token people.
    with pytest.raises(AccessError):
        channel_invite(u_token3,channel_test_id, u_id2)

#########################################################################
#
#                     test for channel_detail function
#
##########################################################################

# Xingyu TAN working on channel_details.py for channel_details fuction
# 29 SEP 2020

"""
channel_details()
Given a Channel with ID channel_id that the authorised user is part of

RETURNS:
provide basic details about the channel


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid


2. accessError
- the auth user is not in this channel.

"""

def test_channel_details_work():
    '''
    this test is using for check the fuction can work normally when no Errors bring.
    '''
    # create 2 users 
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    # testing for channel invite fuction
    channel_invite(u_token1,channel_test_id,u_id2)
    channel_test_details = channel_details(u_token1,channel_test_id)


    # Assuming we the fuction running correctly, then we do check the channel details 
    # expecially, the member infomation
    # check for channel_id
    assert channel_test_details['name'] == 'channel_test'
     
    # check for owner
    assert channel_test_details['owner_members'][0]['u_id'] == u_id1

    # check for members 
    assert channel_test_details['all_members'][0]['u_id'] == u_id1
    assert channel_test_details['all_members'][1]['u_id'] == u_id2



def test_channel_details_invalid_channelId():
    '''
    This test is using for check when the user id we had is invalid
    inputError
    '''
    # create 2 users 
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    channel_invite(u_token1,channel_test_id, u_id2)
    
    # testing for channel invite fuction for invalid channel id inputError
    with pytest.raises(InputError):
        channel_details(u_token1,channel_test_id + 0xf)

def test_channel_non_member_call_details():
    '''
    This test is using for check when the authorised user 
    is not already a member of the channel
    AccessError 
    '''
    # create 2 users and author people 
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    user3 = auth_register("test3@test.com","check_test","test","TAN")
    user3 = auth_login("test3@test.com","check_test")
    u_id3 = user3['u_id']
    u_token3 = user3['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)


    # testing for channel invite fuction for invalid token people.
    with pytest.raises(AccessError):
        channel_details(u_token3,channel_test_id)

    
#########################################################################
#
#                     test for channel_messages function
#
##########################################################################


# Xingyu TAN working on channel_test.py for channel_messages fuction
# 29 SEP 2020

"""
channel_messages()
Given a Channel with ID channel_id that the authorised user is part of channel, 
and return no more than 50 messages

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
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)
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
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)
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
    other.clear()
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
    channel_test_id = channels_create(u_token1,"channel_test",True)


    #adding some message in the channel
    message_send(u_token1, channel_test_id, 'hi steve')

    # testing for channel invite fuction for invalid token people.
    with pytest.raises(AccessError):
        channel_messages(u_token3,channel_test_id,0)

def test_channel_nornal_test():
    '''
    this test using for check if the channel fuction can return correctly
    1. -1 : for no more message after start
    2. check the fuction can return the message correctly.
    2.1 the [0] always the top fresh one 
    3. 0< number && number <= 50: exist messages after start and no more than 50 messages.
    4. 50 : the exist messages after start more than 50, just return the top 50 ones.
    '''
    # create 2 users 
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    # 1. return -1 : for no more message after start
    check_return_negative_one = channel_messages(u_token1,channel_test_id,0)
    assert check_return_negative_one['end'] == -1

    # 2. check the fuction can return the message correctly.
    for i in range(1,3):
        check_message_id = message_send(u_token1, channel_test_id, 'hi steve')['message_id']
        check_work_msg = channel_messages(u_token1,channel_test_id,0)
        # check the uodatest msg in [0]
        assert(check_work_msg['messages'][0]['message_id'] == check_message_id)

        #3. 0< number && number <= 50: exist messages after start and no more than 50 messages.
        assert(check_work_msg['end'] == 50)
    
    # 4. 50 : the exist messages after start more than 50, just return the top 50 ones.
    for i in range(1,50):
        message_send(u_token1, channel_test_id, 'list more than 50 msgs')['message_id']
        
    # update the last one 
    check_message_id = message_send(u_token1, channel_test_id, 'update the last one')['message_id']
    check_work_msg = channel_messages(u_token1,channel_test_id,0)
    # check the uodatest msg in [0] is the last update one.
    assert(check_work_msg['messages'][0]['message_id'] == check_message_id)





