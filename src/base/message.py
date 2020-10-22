'''
    channel.py written by Xingyu Tan.
'''
import jwt
import data.data as data
from base.error import InputError, AccessError
from datetime import timezone, datetime
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

