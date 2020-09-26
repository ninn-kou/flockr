from channels_create import *

def test_channels_list():
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
