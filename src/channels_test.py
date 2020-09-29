import auth
import channels
import pytest
import data

def test_channels_list():
data = {
    'user': [
        { 
            'u_id': ,
            'name_first':'',
            'name_last':'',
            'token':'',
        }
    ]
    'channels': [
        {
            'name':'',
            'channel_id':'',
            'is public' = ,
            'owner_members':[
                {
                    'u_id': ,
                    'name_first': '',
                    'name_last': '',
                }
            ]
            'all_members':[
                {
                    'u_id': ,
                    'name_first': '',
                    'name_last': '',
                }
            ]
            'messages':[
                
            ]
        }  
    ]
}
    token = '12345'
    channels = test_channels_list(token)
    assert channels == [{'channel_id': 1,'name': 'My Channel'}]
    
def test_channels_listall():
    token = '12345'
    channels = test_channels_listall(token)
    assert channels == [{'channel_id': 1,'name': 'My Channel'}]
    
def channels_create():
    token = '12345'
    name = 'name'
    is_public = True
    channel_id = channels_create(token, name, is_public)
    assert channel_id == 1
