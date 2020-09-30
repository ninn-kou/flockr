import auth
import channels 
import pytest
import data


def test_channels_create():
    #create a user and take its  id and token
    user1 = auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth_login('12345@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']
    
    #create a channel in channels and return its channel id
    channel_1_id = channels_create(u1_token,'team',True)
    assert channel_1_id is int
 
def test_channels_listall = channels_listall(u1_token):
    #create two user and take their id and token
    user1 = auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth_login('12345@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']
    
    user2 = auth_register('23456@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth_login('23456@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    
    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels_create(u1_token,'team',True)
    
    #create a channel by user2 in channels and return its channel id
    channel_2_id = channels_create(u2_token,'team2',True)
    
    #check if the function return them all
    channel_listall = channels_listall(u1_token)
    
    assert channel_listall == [
        {
            'name':'team',
            'channel_id':channel_1_id,
            'public':'True',
            'owner':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ],
            'all_members':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ]
        } , {
            'name':'team2',
            'channel_id':channel_2_id,
            'public':'True',
            'owner':[
                {
                    'u_id': u2_id,
                    'name_first': 'FirstN2',
                    'name_last': 'LastN2'
                }
            ],
            'all_members':[
                {
                    'u_id': u2_id,
                    'name_first': 'FirstN2',
                    'name_last': 'LastN2'
                }
            ]
        }
    ]

def test_channels_list = channels_list(u1_token):
    #create two user and take their id and token
    user1 = auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth_login('12345@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']
    
    user2 = auth_register('23456@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth_login('23456@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    
    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels_create(u1_token,'team',True)
    
    #create a channel by user2 in channels and return its channel id
    channel_2_id = channels_create(u2_token,'team2',True)
    #channel_listall = channels_listall(u1_token)
    
    #check if it only return the autherised one
    channel_list1 = channels_list(u1_token)
    assert channel_list1 == [
        {
            'name':'team',
            'channel_id':channel_1_id,
            'public':'True',
            'owner':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ],
            'all_members':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ]
        }
    ]

