'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with auth/
'''

from flask import Blueprint, request, jsonify

import base.channel as channel

CHANNELHTTP = Blueprint('channel', __name__)

@CHANNELHTTP.route('/invite', methods = ['POST'])
def invite():
    ''' invites user to new channel'''

    input_obj = request.json
    print(input_obj)

    channel.channel_invite(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )

    return {}

@CHANNELHTTP.route('/details', methods = ['GET'])
def details():
    ''' gets details about specific channel'''

    input_obj = request.args

    output = channel.channel_details(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )

    return jsonify(output)

@CHANNELHTTP.route('/messages', methods = ['GET'])
def messages():
    ''' gets messages from a specific channel '''

    input_obj = request.args

    output = channel.channel_messages(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        int(input_obj.get('start'))
    )

    return jsonify(output)

@CHANNELHTTP.route('/leave', methods = ['POST'])
def leave():
    ''' leaves channel for user '''

    input_obj = request.json

    channel.channel_leave(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )

    return {}

@CHANNELHTTP.route('/join', methods = ['POST'])
def join():
    ''' join channel for user '''

    input_obj = request.json

    channel.channel_join(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )

    return {}


@CHANNELHTTP.route('/addowner', methods = ['POST'])
def addowner():
    ''' add a new user as admin '''

    input_obj = request.json

    channel.channel_addowner(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )

    return {}


@CHANNELHTTP.route('/removeowner', methods = ['POST'])
def removeowner():
    ''' add a new user as admin '''

    input_obj = request.json

    channel.channel_removeowner(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('u_id')
    )

    return {}
