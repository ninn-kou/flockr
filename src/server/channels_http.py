'''
Joseph Jeong 20 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with channels/
'''

from flask import Blueprint, request, jsonify

import base.channels as channels

CHANNELSHTTP = Blueprint('channels', __name__)

@CHANNELSHTTP.route('/create', methods = ['POST'])
def create():
    ''' creates a new channel'''

    input_obj = request.json

    output = channels.channels_create(
        input_obj.get('token'),
        input_obj.get('name'),
        input_obj.get('is_public')
    )

    return jsonify(output)

@CHANNELSHTTP.route('/listall', methods = ['GET'])
def listall():
    '''lists all channels that exist'''

    # I will never understand why they did this
    input_obj = request.args

    output = channels.channels_listall(
        input_obj.get('token')
    )

    return jsonify(output)

@CHANNELSHTTP.route('/list', methods = ['GET'])
def list():
    '''lists all channels that exist'''

    input_obj = request.args

    output = channels.channels_list(
        input_obj.get('token')
    )

    return jsonify(output)