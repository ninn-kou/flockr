# this file is using for pytest of channel.py .
import auth
import channel
import channels
import pytest
from error import InputError, AccessError
import data


# Xingyu TAN working on channel_test.py for channel_invite fuction
# 29 SEP 2020

"""
channel_invite()
the fuction Invites a user (with user id u_id) to join a channel with ID channel_id. 

RETURNS:
none


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- the user id we had is invalid

2. accessError
- the auth user is not in this channel.

"""
