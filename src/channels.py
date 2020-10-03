import data
import random
import auth
from other import clear
from error import InputError


################################################################################
################################################################################
##
##    Liuyuzi He's work:
##
################################################################################
################################################################################


def channels_list(token):
    """List the channel you want."""
    for i in data.users:                    # Transfer token into u_id.
        if i['token'] == token:
            user_id = i['u_id']
            break
    channel_list = []
    for i in range(len(data.channels)):     # Use loops to check if user in channel.
        for j in range(len(data.channels[i]['all_members'])):
            if data.channels[i]['all_members'][j]['u_id'] == user_id:
                channel_list.append(data.channels[i])
    return channel_list


def channels_listall(token):
    """just return all channels? sure about that?"""
    return data.channels


def create_channel_id(channels):
    """Create a random channel id."""
                                            # Randomly generated a 32 bit unsigned int.
                                            # Check if this int is unique.
    channel_id = random.randint(0, 0xFFFFFFFF)
    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel_id = create_channel_id(channels)
            break
    return channel_id


def channels_create(token, name, is_public):
    """Create a new empty channel."""
    data.init_channels()                    # Initialise the channels list.

    if len(name) > 20:                      # The length of channel name should <= 20.
        raise(InputError)

    for i in data.users:                    # Find the details of the user by token.
        if i['token'] == token:
            owner_id = i['u_id']
            owner_FN = i['name_first']
            owner_LN = i['name_last']
            break

    channel_id = create_channel_id(data.channels)
    channel_new = {                         # Initialize the new channel.
        'name': name,
        'channel_id':channel_id,
        'owner': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],
        'all_members': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],
        'is_public': is_public,
        'message':[]
    }

    data.append_channels(channel_new)       # Add this new channel into data.
    return channel_id
