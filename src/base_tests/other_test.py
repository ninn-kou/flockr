import base.auth as auth
import base.other as other
import data.data as data
import base.message as message
import base.channel as channel
import base.channels as channels
from base.error import InputError, AccessError
import pytest
import random


def test_users_all_initial():
    '''check the list when there is only one user'''
    other.clear()
    # initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']

    i = other.users_all(u1_token)
    i_user1 = i[0]
    assert len(i) == 1    
    assert i_user1['u_id'] == u1_id
    assert i_user1['email'] == '12345@test.com'
    assert i_user1['name_first'] == 'FirstN'
    assert i_user1['name_last'] == 'LastN'

def test_users_all_add_new():
    '''check the list after a new user adding in'''
    other.clear()
    # initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']

    i = other.users_all(u1_token)
    i_user1 = i[0]
    i_user2 = i[1]
    assert len(i) == 2
    assert i_user1['u_id'] == u1_id
    assert i_user1['email'] == '12345@test.com'
    assert i_user1['name_first'] == 'FirstN'
    assert i_user1['name_last'] == 'LastN'    
    assert i_user2['u_id'] == u2_id
    assert i_user2['email'] == '2345@test.com'
    assert i_user2['name_first'] == 'FirstN2'
    assert i_user2['name_last'] == 'LastN2'
    
def test_admin_userpermission_change_permission_id():
    '''check the initial permission_id of the users is true'''
    other.clear()
    #initialise the users list
    #create the first user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    
    #create another 2 users
    user2 = auth.auth_register('23456@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('23456@test.com', 'password')
    user3 = auth.auth_register('34567@test.com', 'password', 'FirstN3', 'LastN3')
    user3 = auth.auth_login('34567@test.com', 'password')
    
    #check the default value
    assert user1['permission_id'] == 1
    assert user2['permission_id'] == 2
    assert user3['permission_id'] == 2
    
        
def test_admin_ERROR_not_owner():
    '''check the AccessError when the admin is not a owner'''
    other.clear()
    #initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_id = user1['u_id']
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_token = user2['token']
    
    #check the error when the token is from a user who is not a owner
    with pytest.raises(AccessError):
        other.admin_userpermission_change(u2_token, u1_id, 2)

def test_admin_ERROR_invalid_permission_id():
    other.clear()
    #initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']

    #check the error when the permission_id is not valid
    with pytest.raises(InputError):
        other.admin_userpermission_change(u1_token, u2_id, 3)
        
def test_admin_incalid_userid():
    other.clear()
    #initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    
    #create a u_id which is not exit in data
    uid_temp = random.randint(0, 0xFFFFFFFF)
    
    #check the error when the user id is not exit    
    with pytest.raises(InputError):
        other.admin_userpermission_change(u1_token, uid_temp, 2)
        
def test_admin_userpermission_change():
    other.clear()
    #initialise the users list
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
        
    #run the function and test
    other.admin_userpermission_change(u1_token, u2_id, 1)
    
    assert user1['permission_id'] == 1
    assert user2['permission_id'] == 1


def test_search_basic():
    '''check if the function can collect all the message with query_str'''
    other.clear()
    #initialise the channels list
    #create the first user and take their token
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']

    # create a channel for testing
    channel_test_id1 = channels.channels_create(u1_token,"channel_test1",True).get('channel_id')
    #add some message to one channel
    message.message_send(u1_token, channel_test_id1, 'Today, I am the winner.')         #true
    message.message_send(u1_token, channel_test_id1, 'What about you?')                 #false(no query_str)
    message.message_send(u1_token, channel_test_id1, 'Yesterday, I was the winner.')    #true
    message.message_send(u1_token, channel_test_id1, 'Cool!')                           #false(no query_str)
    message.message_send(u1_token, channel_test_id1, 'Tomorrow, I will be the winner.') #true
    
    i = other.search(u1_token, 'the winner')
    assert len(i) == 3
    assert i[0]['message'] == 'Tomorrow, I will be the winner.'
    assert i[1]['message'] == 'Yesterday, I was the winner.'
    assert i[2]['message'] == 'Today, I am the winner.'

def test_search_in_several_channel():
    '''check how is the function working when there is more than one channel'''
    other.clear()
    #initialise the channels list
    #create two users and take their token
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_token = user2['token']
    # create 2 channels for testing
    channel_test_id1 = channels.channels_create(u1_token,"channel_test1",True).get('channel_id')
    channel_test_id2 = channels.channels_create(u2_token,"channel_test2",True).get('channel_id')
    #add some message to one channel
    message.message_send(u1_token, channel_test_id1, 'Today, I am the winner.')         #true
    message.message_send(u1_token, channel_test_id1, 'What about you?')                 #false(no query_str)
    message.message_send(u1_token, channel_test_id1, 'Yesterday, I was the winner.')    #true
    message.message_send(u1_token, channel_test_id1, 'Cool!')                           #false(no query_str)
    message.message_send(u1_token, channel_test_id1, 'Tomorrow, I will be the winner.') #true
    
    #add some message to another channel
    message.message_send(u2_token, channel_test_id2, 'We are the winner.')              #false(the message is sent by user2)
    message.message_send(u2_token, channel_test_id2, 'I heard he is the winner')        #false(the message is sent by user2)
    message.message_send(u1_token, channel_test_id2, 'the winner.')                     #true
    message.message_send(u2_token, channel_test_id2, 'I am pretty sure about that')     #false(the message is sent by user2 and no query_str)
    message.message_send(u1_token, channel_test_id2, 'Our team is the winner.')         #true
    
    i = other.search(u1_token, 'the winner')
    assert len(i) == 5
    assert i[0]['message'] == 'Our team is the winner.'
    assert i[1]['message'] == 'the winner.'
    assert i[2]['message'] == 'Tomorrow, I will be the winner.'
    assert i[3]['message'] == 'Yesterday, I was the winner.'
    assert i[4]['message'] == 'Today, I am the winner.'
    
