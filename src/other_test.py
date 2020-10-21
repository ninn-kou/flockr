import data
import other
import data
from error import InputError
import pytest

def test_users_all():
    clear()
    # initialise the users list
    data.init_users()
    #check empty
    assert other.users_all(u1_token) == []
    #create a user
    user1 = auth.auth_register('12345@test.com', 'password', 'FirstN', 'LastN')
    user1 = auth.auth_login('12345@test.com', 'password')
    u1_token = user1['token']
    u1_id = user1['u_id']
    u1_hdstr = user1['handle_str']
    assert other.users_all(u1_token) == [
        {
            'u_id': u1_id
            'email': '12345@test.com'
            'name_first':'FirstN',
            'name_last':'LastN',
            'handle_str': u1_hdstr,
            'token': u1_token,
            'password': 'password'
        }
    ]
    #create another user
    user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
    user2 = auth.auth_login('2345@test.com', 'password')
    u2_id = user2['u_id']
    u2_token = user2['token']
    u2_hdstr = user2['handle_str']
    assert other.users_all(u1_token) == [
        {
            'u_id': u1_id
            'email': '12345@test.com'
            'name_first':'FirstN',
            'name_last':'LastN',
            'handle_str': u1_hdstr,
            'token': u1_token,
            'password': 'password'
        },
        {
            'u_id': u2_id
            'email': '2345@test.com'
            'name_first':'FirstN2',
            'name_last':'LastN2',
            'handle_str': u2_hdstr,
            'token': u2_token,
            'password': 'password'
        }
    ]
