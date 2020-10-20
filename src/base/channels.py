'''
functions of create a new channel and return the specific channel
'''
import random
import jwt
import data.data as data
from base.error import InputError

################################################################################
################################################################################
##
##    Liuyuzi He's work:
##
################################################################################
################################################################################

def owner_from_token(token):
    ''' find owner from token'''
    # Adding in a little bit here to improve token handling
    with open('src/data/JWT_SECRET.txt', 'r') as file:
        jwt_secret = file.read()

    try:
        email = jwt.decode(token, jwt_secret, algorithms=['HS256']).get('email')
    except jwt.DecodeError as error :
        raise InputError("Couldn't Decode Token") from error

    au_id = None
    for i in data.return_users():
        if i['email'] == email:
            au_id = i

    # make sure user is actually returned
    if au_id is None:
        raise InputError

    return au_id

def channels_list(token):
    """Need to fix implementation """

    # find the token
    i = owner_from_token(token)
    user_id = i['u_id']

    channel_list = []
    for channel in data.return_channels():
        for user in 



    for i in range(len(data.return_channels())):     # Use loops to check if user in channel.
        for j in range(len(data.return_channels()[i]['all_members'])):
            if data.return_channels()[i]['all_members'][j]['u_id'] == user_id:
                channel_list.append(data.return_channels()[i])
    return channel_list


def channels_listall(token):
    """just return all channels? sure about that?"""

    # check that token exists
    owner_from_token(token)

    return data.return_channels()

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
    if len(name) > 20:                      # The length of channel name should <= 20.
        raise InputError

    i = owner_from_token(token)
    owner_id = i['u_id']
    owner_fn = i['name_first']
    owner_ln = i['name_last']

    channel_id = create_channel_id(data.return_channels())
    channel_new = {                         # Initialize the new channel.
        'name': name,
        'channel_id':channel_id,
        'owner': [
            {
                'u_id': owner_id,
                'name_first': owner_fn,
                'name_last': owner_ln,
            }
        ],
        'all_members': [
            {
                'u_id': owner_id,
                'name_first': owner_fn,
                'name_last': owner_ln,
            }
        ],
        'is_public': is_public,
        'message':[]
    }

    data.append_channels(channel_new)       # Add this new channel into data.
    return {'channel_id': channel_id}
