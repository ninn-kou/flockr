import base.auth as auth
import base.channels as channels
import pytest
import data.data as data
from base.error import InputError
import random
from base.other import clear

def test_channels_create():
    clear()
    #initialise the channels list
    data.init_channels()
    #create a user and take its  id and token
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    u1_id = user1['u_id']
    u1_token = user1['token']

    #check the error when the channelname is too long
    with pytest.raises(InputError):
        channels.channels_create(u1_token,'A_very_very_very_ver_long_name',True)

    #create a channel in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True)
    #assert channel_1_id is int
    assert data.channels[-1]['name'] == 'team'
    assert data.channels[-1]['channel_id'] == channel_1_id
    assert data.channels[-1]['is_public'] == True
    assert data.channels[-1]['owner'] == [{'u_id':u1_id,'name_first':'FirstN','name_last':'LastN'}]
    assert data.channels[-1]['all_members'] == [{'u_id':u1_id,'name_first':'FirstN','name_last':'LastN'}]

def test_channels_listall():
    clear()
    #initialise the channels list
    data.init_channels()
    #create two user and take their id and token
    user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('1234@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']

    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']

    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True)

    #create a channel by user2 in channels and return its channel id
    channel_2_id = channels.channels_create(u2_token,'team2',True)

    #check if the function return them all

    assert channels.channels_listall(u1_token) == [
        {
            'name':'team',
            'channel_id':channel_1_id,
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
            ],
            'is_public':True,
            'message':[]

        } , {
            'name':'team2',
            'channel_id':channel_2_id,
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
            ],
            'is_public':True,
            'message':[]
        }
    ]

def test_channels_list():
    clear()
    #initialise the channels list
    data.init_channels()
    #create two user and take their id and token
    user1 = auth.auth_register('45@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('45@test.com', 'password')
    u1_id = user1['u_id']
    u1_token = user1['token']



    #create a channel by user1 in channels and return its channel id
    channel_1_id = channels.channels_create(u1_token,'team',True)

    #check if it only return the autherised one
    channel_list1 = channels.channels_list(u1_token)
    assert channel_list1 == [
        {
            'name':'team',
            'channel_id':channel_1_id,
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
            ],
            'is_public':True,
            'message':[]
        }
    ]

