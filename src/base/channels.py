'''
functions of create a new channel and return the specific channel
'''
import random
import src.data.data as data
from src.base.error import InputError
from src.base.auth import decode_token

################################################################################
################################################################################
##
##    Liuyuzi He's work:
##
################################################################################
################################################################################

def owner_from_token(token):
    ''' find owner from token'''
    user = decode_token(token)
    if user is None:
        raise InputError("Couldn't Decode Token")

    return user

def channels_list(token):
    """Need to fix implementation """

    # find the token
    u_id = owner_from_token(token).get('u_id')

    channel_temp = data.return_channels()

    list_channel = []

    for i in channel_temp:
        for j in i['all_members']:
            if u_id == j['u_id']:
                temp = {
                    'channel_id': i['channel_id'],
                    'name': i['name'],
                }
                list_channel.append(temp)
    return {
        'channels': list_channel,
    }


def channels_listall(token):
    """just return all channels? sure about that?"""

    # check that token exists
    owner_from_token(token)
    channel_temp = data.return_channels()
    all_channels = []

    for i in channel_temp:
        temp = {
            'channel_id': i['channel_id'],
            'name': i['name'],
        }
        all_channels.append(temp)

    return {
        'channels': all_channels,
    }



def create_channel_id(channels):
    """Create a random channel id."""
                                            # Randomly generated a 32 bit unsigned int.
                                            # Check if this int is unique.
    channel_id = random.randint(0, 0xFFFFFFFF)
    for i in channels:
        if i['channel_id'] is channel_id:
            channel_id = create_channel_id(i)
            break

    return channel_id


def channels_create(token, name, is_public):
    """Create a new empty channel."""
    if len(name) > 20:                      # The length of channel name should <= 20.
        raise InputError('The length of channel name should <= 20')

    i = owner_from_token(token)
    owner_id = i['u_id']
    owner_fn = i['name_first']
    owner_ln = i['name_last']

    standup = {
        'finish_time':-1,
        'message_package':'',
    }

    channel_id = create_channel_id(data.return_channels())
    channel_new = {                         # Initialize the new channel.
        'name': name,
        'channel_id':channel_id,
        'owner_members': [
            {
                'u_id': owner_id,
                'name_first': owner_fn,
                'name_last': owner_ln,
                'profile_img_url':''

            }
        ],
        'all_members': [
            {
                'u_id': owner_id,
                'name_first': owner_fn,
                'name_last': owner_ln,
                'profile_img_url':''
            }
        ],
        'is_public': is_public,
        'message':[],
        'standup': standup
    }

    data.append_channels(channel_new)       # Add this new channel into data.
    return {
        'channel_id': channel_id
    }
