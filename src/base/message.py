'''
    channel.py written by Xingyu Tan.

from datetime import timezone, datetime
import jwt
import data.data as data
from base.error import InputError, AccessError

################################################################################
################################################################################
##
##    Xingyu TAN's work:
##    22 October, 2020
##
##      - some helper functions;
##      - message_send(token, channel_id, message);
##      - message_remove(token, message_id);
##      - message_edit(token, message_id, message);
##      - and all tests for these functions.
##
################################################################################
################################################################################


############################################################
#      Helper Functions
############################################################
def if_auth_channel_owner(u_id, channel_id):
    """check if the u_id is the owner of the channel"""
    test = False
    channel_got = find_channel(channel_id)
    for i in channel_got['owner']:
        if i['u_id'] == u_id:
            test = True
            break
    return test

def delete_msg_in_list(msg):
    """Interate the messages list by its id, return the message we need."""
    data.init_messages()
    data.messages.remove(msg)
    data.init_channels()
    for i in data.channels:
        if i['channel_id'] == msg['channel_id']:
            i['message'].remove(msg)
            break

def find_message(msg_id):
    """Interate the messages list by its id, return the message we need."""
    return_message = None
    for i in data.messages:
        if i['message_id'] == msg_id:
            return_message = i
            break
    return return_message

def add_one_in_channel(channel_id, user):
    """Adding a member into the channel."""
    for i in data.channels:
        if i['channel_id'] == channel_id:
            i['all_members'].append(user)
            break

def token_into_user_id(token):
    """Transfer the token into the user id."""

    # Adding in a little bit here to improve token handling
    with open('src/data/JWT_SECRET.txt', 'r') as file:
        jwt_secret = file.read()

    try:
        email = jwt.decode(token, jwt_secret, algorithms=['HS256']).get('email')
    except jwt.DecodeError:
        return -1

    au_id = -1
    for i in data.return_users():
        if i['email'] == email:
            au_id = i['u_id']
    return au_id

def find_channel(channel_id):
    """Interate the channels list by its id, return the channel we need."""
    answer = None
    for i in data.channels:
        if i['channel_id'] == channel_id:
            answer = i
            break
    return answer

def find_user(user_id):
    """Find user's info by search one's id."""
    u_id = -1
    for i in data.return_users():
        if i['u_id'] == user_id:
            u_id = i
            break
    return u_id

def find_one_in_channel(channel, u_id):
    """Return a boolean variable to indicate if someone we want in the channel."""
    for i in channel['all_members']:
        if i['u_id'] == u_id:
            return True
    return False


############################################################
#       message_send(token, channel_id, message)
############################################################
def message_send(token, channel_id, message):
    """
    message_send()
    Send a message from authorised_user to the channel specified by channel_id

    Args:
        token: the token of the sender.
        channel_id: the channel which is the target of message.
        message: the message we send.

    RETURNS:
    { message_id }


    THEREFORE, TEST EVERYTHING BELOW:
    1. inputError
    - Message is more than 1000 characters

    2. accessError
    - the authorised user has not joined the channel they are trying to post to
    - cannot find the channel_id

    """
    # Global variables.
    data.init_channels()
    data.init_messages()
    # InputError 1: invalid token.
    auth_id = token_into_user_id(token)
    if auth_id == -1:
        raise InputError(description='invalid token.')

    # InputError 2: Message is more than 1000 characters.
    if len(message) > 1000:
        raise InputError(description='Message is more than 1000 characters.')

    # AccessError 3: invalid channel_id.
    channel_got = find_channel(channel_id)
    if channel_got is None:
        raise AccessError(description='invalid channel_id.')

    # AccessError 4: if the auth not in channel.
    if not find_one_in_channel(channel_got, auth_id):
        raise AccessError(description='auth not in channel')

    # Case 5: no error, add the message
    new_msg_id = 1
    if len(data.messages) != 0:
        new_msg_id = data.messages[0]['message_id'] + 1

    # record the time rightnow
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())

    # create the message struct
    return_message = {
        'message_id': new_msg_id,
        'channel_id': channel_id,
        'u_id': auth_id,
        'message': message,
        'time_created': timestamp,
    }

    # insert the message in the top of messages in the channel.
    channel_got['message'].insert(0, return_message)
    data.messages.insert(0, return_message)
    return {
        'message_id': new_msg_id,
    }
############################################################
#       message_remove(token, message_id)
############################################################
def message_remove(token, message_id):
    """
    message_remove()
    Given a message_id for a message, this message is removed from the channel

    Args:
        token: the token of the people who authority.
        channel_id: the channel which is the target of message.

    RETURNS:
    {}


    THEREFORE, TEST EVERYTHING BELOW:
    1. inputError
    - Message id is not exist

    2. accessError excluding
    - Message with message_id was sent by the authorised user making this reques
    - The authorised user is an owner of this channel or the flockr
    """
    # Global variables.
    data.init_channels()
    data.init_messages()

    # InputError 1: invalid token.
    auth_id = token_into_user_id(token)
    if auth_id == -1:
        raise InputError(description='invalid token.')

    # InputError 2: Message id is not exist
    message_using = find_message(message_id)
    if message_using is None:
        raise InputError(description='invalid message id.')

    # AccessError 3: excluding message sender and channel_owner
    test_owener = if_auth_channel_owner(auth_id, message_using['channel_id'])
    # if it is neither channel owner nor messager sender
    # raise for access error
    if test_owener == False and message_using['u_id'] != auth_id:
        raise AccessError(description='neither message sender nor channel_owner.')

    # Case 4: no error, delete the message
    delete_msg_in_list(message_using)

    return {}

def message_edit(token, message_id, message):
    return {
    }
'''
