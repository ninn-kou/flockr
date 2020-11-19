"""
channel_http.py written by Xingyu Tan, Yuhan Yan, Liuyuzi He, Hao Ren and Joseph Jeong.

Just experimenting with how Flask works at the moment.
All url appends are prepended with `auth/`,
"""

from flask import Blueprint, request, jsonify

import src.base.channel as channel
import src.data.data as data

CHANNELHTTP = Blueprint('channel', __name__)

@CHANNELHTTP.route('/invite', methods = ['POST'])
def invite():
    """Invites user to new channel."""
    input_obj = request.json

    channel.channel_invite(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )
    return {}

@CHANNELHTTP.route('/details', methods = ['GET'])
def details():
    """Gets details about specific channel."""
    input_obj = request.args

    output = channel.channel_details(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )
    for i in output['owner_members']:
        i['profile_img_url'] = data.get_profile_photo_url(i['u_id'])
    for i in output['all_members']:
        i['profile_img_url'] = data.get_profile_photo_url(i['u_id'])
    return jsonify(output)

@CHANNELHTTP.route('/messages', methods = ['GET'])
def messages():
    """Gets messages from a specific channel."""
    input_obj = request.args

    output = channel.channel_messages(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        int(input_obj.get('start'))
    )
    return jsonify(output)

@CHANNELHTTP.route('/leave', methods = ['POST'])
def leave():
    """Leaves channel for user."""
    input_obj = request.json

    channel.channel_leave(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )
    return {}

@CHANNELHTTP.route('/join', methods = ['POST'])
def join():
    """Join channel for user."""
    input_obj = request.json

    channel.channel_join(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )
    return {}


@CHANNELHTTP.route('/addowner', methods = ['POST'])
def addowner():
    """Add a new user as admin."""
    input_obj = request.json

    channel.channel_addowner(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )
    return {}


@CHANNELHTTP.route('/removeowner', methods = ['POST'])
def removeowner():
    """Remove the owner user."""
    input_obj = request.json

    channel.channel_removeowner(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )
    return {}
