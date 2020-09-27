'''
    the file using for channel testing
'''
import pytest
import data
import channel
from error import InputError 

###########################################################################################
##                                test of channel_addowner                               ##
###########################################################################################
# Standard situation
def test_channel_addowner0():
    # Need the get functions
    # Where to put
    token = get_token()
    channel_id = get_cid()
    u_id = get_uid()

    assert(channel.channel_addowner(token, channel_id, u_id)) is True

# Channel ID is not a valid channel
def test_channel_addowner1():
    token = get_token()
    channel_id = "XXXXXXXX"
    u_id = get_uid()

    with pytest.raises(InputError):
        channel.channel_addowner(token, channel_id, u_id)

# user(u_id) is already the owner
#### Need array in Dict


# user(u_id) is not a valid flocker

###########################################################################################
##                             test of channel_removeowner                               ##
###########################################################################################

# Standard situation
def test_channel_removeowner0():
    channel_detail = {token = "XXXX", channel_id = "XXXXXXXX", u_id = "XXX"}
    pop_token = channel_detail.pop('token')
    pop_cid = channel_detail.pop('channel_id')
    pop_uid = channel_detail.pop('u_id')

    assert(channel_detail = {token = "", channel_id = "", u_id = ""})

# Channel ID is not a valid channel

# user(u_id) is not the owner

# user(u_id) is not in the channel