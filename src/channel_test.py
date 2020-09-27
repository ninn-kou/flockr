'''
    the file using for channel testing
'''
import pytest
import data
import channel
from error import InputError 

# Standard situation
def test_channel_addowner0():
    token = get_token()
    channel_id = get_cid()
    u_id = get_uid()

    assert(channel.channel_addowner(token, channel_id, u_id)) is True

# Channel ID is not a valid channel
def test_channel_addowner1():
    token = get_token()
    channel_id = get_cid()
    u_id = get_uid()

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

