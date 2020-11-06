''' this file is using for pytest of base/message.py .'''
from datetime import timezone, datetime
import pytest
from base.channel import channel_invite, channel_messages
from base.channels import channels_create
from base.auth import auth_login, auth_register, auth_logout
from base.message import message_send, message_remove, message_edit
from base.message import message_sendlater
, message_pin#, message_unpin, message_react, message_unreact
from base.error import InputError, AccessError
import base.other as other



#########################################################################
#
#                     test for message_send Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_send function
# 22 Oct. 2020

##########################################################################
#    message_send()
#    Send a message from authorised_user to the channel specified by channel_id
#
#    Args:
#        token: the token of the sender.
#        channel_id: the channel which is the target of message.
#        message: the message we send.
#
#    RETURNS:
#    { message_id }
#
#
#    THEREFORE, TEST EVERYTHING BELOW:
#    1. inputError
#    - Message is more than 1000 characters
#
#    2. accessError
#    - the authorised user has not joined the channel they are trying to post to
#    - cannot find the channel_id
############################################################################

########################################################################
#######################  test for input error  #########################
def test_message_input_error():
    '''
    this test using for check if the message_send function
    send the message which is more than 1000 characters
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
    message_test = 3000 * message_test

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(InputError):
        message_send(u_token1, channel_test_id, message_test)

    auth_logout(u_token1)

#######################  test for access error  #########################
def test_message_access_error_wrong_token():
    '''
    this test using for check if the authorised user
    has not joined the channel they are trying to post to
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # create a message
    message_test = "msg test"

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(AccessError):
        message_send(u_token2, channel_test_id, message_test)

    auth_logout(u_token1)
    auth_logout(u_token2)

###########################################################################################
def test_access_error_invalid_channelid():
    '''
    This test is using for check when channel id we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message
    message_test = "msg test"

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(AccessError):
        message_send(u_token1, channel_test_id + 0xf, message_test)

    auth_logout(u_token1)

###########################################################################################
def test_access_error_invalid_tokenid():
    '''
    This test is using for check when token we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message
    message_test = "msg test"

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        message_send(u_token1 + 'abc', channel_test_id, message_test)

    auth_logout(u_token1)

######   test  for normally channel_messsge work and correct message_send return #########
# case 1: return -1 : for no more message after start
def test_channel_message_return_negative_one():
    '''
    this test using for check if the channel function can return correctly

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # 1. return -1 : for no more message after start
    check_return_negative_one = channel_messages(u_token1, channel_test_id, 0)
    assert check_return_negative_one['end'] == -1

    auth_logout(u_token1)
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
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # check the function can return the message correctly.
    message_send(u_token1, channel_test_id, "msg test 01")

    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    #0< number && number <= 50: exist messages after start and no more than 50 messages.
    assert check_work_msg['end'] == 50

    auth_logout(u_token1)
###########################################################################################

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
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')


    # the exist messages after start more than 50, just return the top 50 ones.
    for _ in range(1, 60):
        message_send(u_token1, channel_test_id, 'list more than 50 msgs')

    # update the last one
    assert isinstance(message_send(u_token1, channel_test_id, 'the next one'), dict)

    # check the uodatest msg in [0] is the last update one.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'the next one'

    auth_logout(u_token1)
###########################################################################################
# case 4: test if we can show the correct message_send information
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
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_send(u_token1, channel_test_id, "msg test 03")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 03'
    assert check_work_msg['messages'][1]['message'] == 'msg test 02'
    assert check_work_msg['messages'][2]['message'] == 'msg test 01'

    auth_logout(u_token1)
###########################################################################################
# case 5: test if we can show the correct messsage_send return
def test_channel_message_correct_send_return_id():
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
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed and check return
    assert message_send(u_token1, channel_test_id, "msg test 01")['message_id'] == 1
    assert message_send(u_token1, channel_test_id, "msg test 02")['message_id'] == 2
    assert message_send(u_token1, channel_test_id, "msg test 03")['message_id'] == 3
    auth_logout(u_token1)

#########################################################################
#
#                     test for message_remove Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_remove function
# 22 Oct. 2020

##########################################################################
#    message_remove()
#    Given a message_id for a message, this message is removed from the channel
#
#    Args:
#        token: the token of the people who authority.
#        channel_id: the channel which is the target of message.
#
#    RETURNS:
#    {}
#
#
#    THEREFORE, TEST EVERYTHING BELOW:
#    1. inputError
#    - Message id is not exist
#
#    2. accessError excluding
#    - Message with message_id was sent by the authorised user making this reques
#    - The authorised user is an owner of this channel or the flockr
##########################################################################


#######################  test for input error  #########################

def test_message_remoe_wrong_msg_id():
    '''
    this test using for check if the message id given is valid
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing for channel message function for invalid message id inputError
    with pytest.raises(InputError):
        message_remove(u_token1, message_test_id + 0xf)

    auth_logout(u_token1)

def test_message_remoe_wrong_token_id():
    '''
    this test using for check if the token given is valid
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing for channel message function for invalid token inputError
    with pytest.raises(InputError):
        message_remove(u_token1 + 'abc', message_test_id)

    auth_logout(u_token1)

#######################  test for access error  #########################
def test_message_remoe_neither_sender_and_owner():
    '''
    this test using for check when the auth people is neither sender
    and channel or flockr owner
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing for channel message function for invalid message id inputError
    with pytest.raises(AccessError):
        message_remove(u_token2, message_test_id)

    auth_logout(u_token1)
    auth_logout(u_token2)

##############################  test for normal running ###################################
def test_message_remove_works_normally_for_message_sender_only():
    '''
    this test using for check if the message_remove can normal running
    if we meet above conditions
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # 1. remove the message we need
    assert isinstance(message_remove(u_token2, message_test_id), dict)

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token2, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 02'
    assert check_work_msg['messages'][1]['message'] == 'msg test 01'

    auth_logout(u_token1)
    auth_logout(u_token2)
#########################################################################################
def test_message_remove_works_normally_for_channel_owner_only():
    '''
    this test using for check if the message_remove can normal running
    if we meet above conditions
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # 1. remove the message we need
    message_remove(u_token2, message_test_id)

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 02'
    assert check_work_msg['messages'][1]['message'] == 'msg test 01'

    auth_logout(u_token1)
    auth_logout(u_token2)
#########################################################################################
def test_message_remove_works_normally_for_flocker_owner_only():
    '''
    this test using for check if the message_remove can normal running
    if we meet above conditions
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # change the permission
    other.admin_userpermission_change(u_token1, u_id2, 1)

    # 1. remove the message we need
    message_remove(u_token2, message_test_id)

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 02'
    assert check_work_msg['messages'][1]['message'] == 'msg test 01'

    auth_logout(u_token1)
    auth_logout(u_token2)

#########################################################################
#
#                     test for message_edit Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_edit function
# 23 Oct. 2020

##########################################################################
#    message_edit()
#    Given a message, update it's text with new text.
#    If the new message is an empty string, the message is deleted.
#
#    Args:
#        token: the token of the people who edit it.
#        channel_id: the channel which is the target of message.
#        message: the new message.
#
#    RETURNS:
#    { }
#
#
#    THEREFORE, TEST EVERYTHING BELOW:
#    1. inputError
#    - None
#
#    2. accessError
#    - the authorised user is the message sender
#    - the authorised user is the owener of flocker or channel
#
#    3. if the new message is empty
#    - delete the message
############################################################################

########################################################################
#######################  test for input error  #########################
def test_message_access_error_neither_owener_nor_sender():
    '''
    this test using for check the message_edit for the auther who is
    neither owener nor sender
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # create a message
    message_test = "msg test"

    #send one message
    message_test_id = message_send(u_token1, channel_test_id, message_test)['message_id']


    # testing for channel invite function for length more than 1000 words
    with pytest.raises(AccessError):
        message_edit(u_token2, message_test_id, "message_edit")

    auth_logout(u_token1)
    auth_logout(u_token2)

#######################  test for normally working  #########################
def test_message_edit_works_for_sender():
    '''
    this test using for check the message_edit works normally for the message sender
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # 1. edits the message we need
    assert isinstance(message_edit(u_token2, message_test_id, "message_edit"), dict)

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'message_edit'


    auth_logout(u_token1)
    auth_logout(u_token2)

#######################  test for normally working  #########################
def test_message_edit_works_for_owner():
    '''
    this test using for check the message_edit works normally for the channel_owner
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # 1. edits the message we need
    message_edit(u_token1, message_test_id, "message_edit")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'message_edit'


    auth_logout(u_token1)
    auth_logout(u_token2)

#######################  test for normally working  #########################
def test_message_edit_works_for_flocker_owner():
    '''
    this test using for check the message_edit works normally for the flocker_owner
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # change the permission
    other.admin_userpermission_change(u_token1, u_id2, 1)

    # 1. edits the message we need
    message_edit(u_token2, message_test_id, "message_edit")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'message_edit'


    auth_logout(u_token1)
    auth_logout(u_token2)

############  test for normally working when empty message given  ###################
def test_message_edit_works_for_empty_msg():
    '''
    this test using for check the message_edit works normally for the channel_owner
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_test_id_01 = message_send(u_token1, channel_test_id, "msg test 02")['message_id']
    message_test_id_02 = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # 1. edits the message we need
    message_edit(u_token1, message_test_id_02, "")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 02'
    assert check_work_msg['messages'][0]['message_id'] == message_test_id_01


    auth_logout(u_token1)
    auth_logout(u_token2)


#########################################################################
#
#                     test for message_sendlater Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_sendlater function
# 05 Nov. 2020

##########################################################################
#
#    message_sendlater()
#    Send a message from authorised_user to the channel specified
#    by channel_id automatically at a specified time in the future
#    Args:
#        token: the token of the people who edit it.
#        channel_id: the channel which is the target of message.
#        message: the new message.
#        time_sent: when the msg would be sent
#    RETURNS:
#    return {
#        'message_id': new_msg_id,
#    }
#
#
#   THEREFORE, TEST EVERYTHING BELOW:
#    1. inputError
#    - Channel ID is not a valid channel
#    - Message is more than 1000 characters
#    - Time sent is a time in the past
#
#    2. accessError
#    when:  the authorised user has not joined the channel they are trying to post to
#
##########################################################################

########################################################################

#######################  test for input error  #########################
def test_message_send_later_input_error1():
    '''
    this test using for check if the message_send function
    send the message which is more than 1000 characters
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
    message_test = 3000 * message_test

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(InputError):
        message_sendlater(u_token1, channel_test_id, message_test, time_furture)

    auth_logout(u_token1)


#######################  test for access error  #########################
def test_message_sendlater_access_error_token_people_wrong():
    '''
    this test using for check if the authorised user
    has not joined the channel they are trying to post to
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # create a message
    message_test = "msg test"
    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5

    # testing for channel invite function for length more than 1000 words
    with pytest.raises(AccessError):
        message_sendlater(u_token2, channel_test_id, message_test, time_furture)

    auth_logout(u_token1)
    auth_logout(u_token2)


###########################################################################################
def test_sendlater_access_error_invalid_channelid():
    '''
    This test is using for check when channel id we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message
    message_test = "msg test"
    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(AccessError):
        message_sendlater(u_token1, channel_test_id + 0xf, message_test, time_furture)

    auth_logout(u_token1)


###########################################################################################
def test_sendlater_access_error_invalid_tokenid():
    '''
    This test is using for check when token we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message
    message_test = "msg test"
    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        message_sendlater(u_token1 + 'abc', channel_test_id, message_test, time_furture)

    auth_logout(u_token1)

###########################################################################################
def test_sendlater_input_error_invalid_time():
    '''
    This test is using for check when time given is in the past

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # create a message
    message_test = "msg test"
    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp - 10

    # testing for channel message function for invalid time given
    with pytest.raises(InputError):
        message_sendlater(u_token1, channel_test_id, message_test, time_furture)

    auth_logout(u_token1)


#######################      TEST NORMALLY    ##############################
# case 1: test if we can show the correct message_send information
def test_channel_message_sendlater_correct_message_infors():
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
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # create the new time
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_furture = timestamp + 5

    #create test message we needed
    check_id = message_sendlater(u_token1, channel_test_id, "msg test 00", time_furture)
    check_id = message_sendlater(u_token1, channel_test_id, "msg test 01", time_furture)


    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][1]['message'] == 'msg test 00'
    assert check_work_msg['messages'][0]['message'] == 'msg test 01'
    assert check_work_msg['messages'][0]['time_created'] == time_furture
    assert check_work_msg['messages'][0]['message_id'] == check_id['message_id']


    auth_logout(u_token1)

#########################################################################
#
#                     test for message_react Function
#
##########################################################################


#########################################################################
#
#                     test for message_unreact Function
#
##########################################################################


#########################################################################
#
#                     test for message_pin Function
#
##########################################################################
# Xingyu TAN working on message_test.py for message_pin function
# 06 Nov. 2020

##########################################################################
#
#    message_pin()
#    Given a message within a channel, mark it as "pinned"
#    to be given special display treatment by the frontend
#    Args:
#        token: the token of the people who edit it.
#        message_id: the new message.
#
#    RETURNS:
#    return {}
#
#   THEREFORE, TEST EVERYTHING BELOW:
#    1. inputError
#    - message_id is not a valid message
#    - message is already pinned
#    - token id incorrect
#    2. accessError
#    - The authorised user is not a member of the channel that the message is within
#    - The authorised user is not an owner
#
##########################################################################
######################   INPUT ERROR    #################
def test_message_pin_wrong_msg_id():
    '''
    this test using for check if the message id given is valid
    '''
    # create 1 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing for invalid message id inputError
    with pytest.raises(InputError):
        message_pin(u_token1, message_test_id + 0xf)

    auth_logout(u_token1)
######################   INPUT ERROR 2   #################
def test_message_pin_already_pin():
    '''
    this test using for check when the message already pin
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']
    # pin the msg
    message_pin(u_token1, message_test_id)

    # testing for already pin inputError
    with pytest.raises(InputError):
        message_pin(u_token1, message_test_id)

    auth_logout(u_token1)
##################################################################
def test_message_pin_wrong_token_id():
    '''
    this test using for check if the token given is valid
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing for channel message function for invalid token inputError
    with pytest.raises(InputError):
        message_pin(u_token1 + 'abc', message_test_id)

    auth_logout(u_token1)

#######################  test for access error  #########################
def test_message_pin_non_channel_member():
    '''
    this test using for check when the auth people is not a channel member
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing when the auth people is not a channel member
    with pytest.raises(AccessError):
        message_pin(u_token2, message_test_id)

    auth_logout(u_token1)
    auth_logout(u_token2)

#######################  test for access error  #########################
def test_message_pin_non_channel_owner():
    '''
    this test using for check when the auth people is not a channel member
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")\
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token1, channel_test_id, "msg test 03")['message_id']

    # testing when the auth people is not a channel owner
    with pytest.raises(AccessError):
        message_pin(u_token2, message_test_id)

    auth_logout(u_token1)
    auth_logout(u_token2)
##############################  test for normal running ###################################
def test_message_pin_works_normally_for_channel_owner_only():
    '''
    this test using for msgpin when the token person is channel owner
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']
    u_token2 = user2['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_test_id = message_send(u_token2, channel_test_id, "msg test 03")['message_id']

    # pin the message we need
    message_pin(u_token2, message_test_id)

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token2, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 03'
    assert check_work_msg['messages'][0]['is_pinned'] == True

    auth_logout(u_token1)
    auth_logout(u_token2)
#########################################################################
#
#                     test for message_unpin Function
#
##########################################################################
