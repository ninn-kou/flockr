# this file is using for pytest of base/message.py .
from base.channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from base.channels import channels_create
from base.auth import auth_login, auth_register, auth_logout
from base.message import message_send, message_remove, message_edit
from base.error import InputError, AccessError
import data.data as data
import pytest
import base.other as other


#########################################################################
#
#                     test for message_send Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_send function
# 22 Oct. 2020

"""
message_send()
Send a message from authorised_user to the channel specified by channel_id

Args:
    token: the token of the sender.
    channel_id: the channel which is the target of message.
    message: the message we send.

RETURNS:
{ message_id }


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- Message is more than 1000 characters

2. accessError
- the authorised user has not joined the channel they are trying to post to
- cannot find the channel_id

"""
###########################################################################################
#######################  test for input error  #########################
def test_message_input_error():
    '''
    this test using for check if the message_send function send the message which is more than 1000 characters
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True)

    # create a message which is more than 1000 characters
    message_test = "aaaaa"
    message_test = 300 * message_test

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(InputError):
        message_send(u_token1, channel_test_id, message_test)

#######################  test for access error  #########################
def test_message_access_error_wrong_token():
    '''
    this test using for check if the authorised user has not joined the channel they are trying to post to
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    # create a message 
    message_test = "msg test"

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(AccessError):
        message_send(u_token2, channel_test_id, message_test)

###########################################################################################
def test_access_error_invalid_channelId():
    '''
    This test is using for check when channel id we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True)
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message 
    message_test = "msg test"

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(AccessError):
        message_send(u_token1, channel_test_id + 0xf, message_test)


######   test  for normally channel_messsge work and correct message_send return #########
# case 1: return -1 : for no more message after start
def test_channel_message_return_negative_one():
    '''
    this test using for check if the channel function can return correctly

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True)

    # 1. return -1 : for no more message after start
    check_return_negative_one = channel_messages(u_token1, channel_test_id, 0)
    assert check_return_negative_one['end'] == -1

###########################################################################################

# case 2: return 50; check the end return alway (start + 50) when message less than 50
def test_channel_message_return50_end():
    '''
    this test using for check if the channel function can return correctly

    3. 0< number && number <= 50: exist messages after start and no more than 50 messages.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True)

    # check the function can return the message correctly.
    message_send(u_token1, channel_test_id, "msg test 01")

    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    #0< number && number <= 50: exist messages after start and no more than 50 messages.
    assert(check_work_msg['end'] == 50)

# case 3: return 50; test for the newest one when total msg more than 50
def test_channel_message_newest_one_index():
    '''
    this test using for check if the channel function can return correctly

    return 50 : the exist messages after start more than 50, just return the top 50 ones.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True)


    # the exist messages after start more than 50, just return the top 50 ones.
    for i in range(1,60):
        message_send(u_token1, channel_test_id, 'list more than 50 msgs')

    # update the last one
    message_send(u_token1, channel_test_id, 'the next one')
    
    # check the uodatest msg in [0] is the last update one.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert(check_work_msg['messages'][0]['message'] == 'the next one')

###########################################################################################


# case 4: test if we can show the correct channel_message information
def test_channel_message_correct_message_infors():
    '''
    this test using for check if the channel function can return correctly
    2. check the function can return the message correctly.
    2.1 the [0] always the top fresh one
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_send(u_token1, channel_test_id, "msg test 03")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert(check_work_msg['messages'][0]['message'] == 'msg test 03')
    assert(check_work_msg['messages'][1]['message'] == 'msg test 02')
    assert(check_work_msg['messages'][2]['message'] == 'msg test 01')

    