import base.auth as auth
import base.other as other
import data.data as data
import base.message as message
import base.channel as channel
import base.channels as channels
from base.error import InputError, AccessError
import pytest
import random

def test_users_all():
    other.clear()
    # initialise the users list
    #data.init_users()
    
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
    #assert i_user1['permission_id'] == 1
    
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    
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
    
    
def test_admin_userpermission_change():
    other.clear()
    # initialise the users list
    data.init_users()
    
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
    
    #check the default value
    assert user1['permission_id'] == 1
    assert user2['permission_id'] == 2
    
    #check the error when the token is from a user who is not a owner
    with pytest.raises(AccessError):
        other.admin_userpermission_change(u2_token, u1_id, 2)
        
    #create some value which is not exit in data
    token_temp = auth.create_token('temp1@temp.com')
    uid_temp = random.randint(0, 0xFFFFFFFF)
    
    #check the error when the token is not exit
    with pytest.raises(InputError):
        other.admin_userpermission_change(token_temp, u1_id, 2)
    
    #check the error when the user id is not exit    
    with pytest.raises(InputError):
        other.admin_userpermission_change(u1_token, uid_temp, 2)
        
    #run the function and test
    other.admin_userpermission_change(u1_token, u2_id, 1)
    
    assert user1['permission_id'] == 1
    assert user2['permission_id'] == 1

def test_search():
    other.clear()
    #initialise the channels list
    data.init_channels()
    #create two users and take their id and token
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    # create 2 channels for testing
    channel_test_id1 = channels_create(u_token1,"channel_test1",True)
    channel_test_id2 = channels_create(u_token2,"channel_test2",True)
    #add some message to one channel
    message.message_send(u_token1, channel_test_id1, 'Today, I am the winner.')
    message.message_send(u_token1, channel_test_id1, 'What about you?')
    message.message_send(u_token1, channel_test_id1, 'Yesterday, I was the winner.')
    message.message_send(u_token1, channel_test_id1, 'Cool!')
    message.message_send(u_token1, channel_test_id1, 'Tomorrow, I will be the winner.')
    
    i = search(u1_token, 'the winner')
    assert len(i) == 3
    assert i[0]['message'] == 'Today, I am the winner.'
    assert i[1]['message'] == 'Yesterday, I was the winner.'
    assert i[2]['message'] == 'Tomorrow, I will be the winner.'
    
    #add some message to another channel
    message.message_send(u_token2, channel_test_id2, 'We are the winner.')
    message.message_send(u_token2, channel_test_id2, 'I heard he is the winner')
    message.message_send(u_token2, channel_test_id2, 'the winner.')
    message.message_send(u_token2, channel_test_id2, 'I am pretty sure about that')
    message.message_send(u_token2, channel_test_id2, 'Our team is the winner.')
    
    i = search(u1_token, 'the winner')
    assert len(i) == 7
    assert i[0]['message'] == 'Today, I am the winner.'
    assert i[1]['message'] == 'Yesterday, I was the winner.'
    assert i[2]['message'] == 'Tomorrow, I will be the winner.'
    assert i[3]['message'] == 'We are the winner.'
    assert i[4]['message'] == 'I heard he is the winner'
    assert i[5]['message'] == 'the winner.'
    assert i[6]['message'] == 'Our team is the winner.'
    
    
