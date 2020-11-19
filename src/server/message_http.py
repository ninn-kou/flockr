"""
message_http.py written by Hao Ren, fixed by Xingyu Tan and Yuhan Yan.

All URL appends are prepended with `message/`.
No need to add separated comments.
All features are as same as the local one, but for server.
"""

from flask import Blueprint, request, jsonify

import src.base.message as message

MESSAGEHTTP = Blueprint('message', __name__)

@MESSAGEHTTP.route("/send", methods=['POST'])
def send():
    input_obj = request.json
    output = message.message_send(
        input_obj.get('token'),
        input_obj.get('channel_id'),
        input_obj.get('message')
    )
    return jsonify(output)

@MESSAGEHTTP.route("/remove", methods=['DELETE'])
def remove():
    input_obj = request.json
    output = message.message_remove(
        input_obj.get('token'),
        int(input_obj.get('message_id'))
    )
    return jsonify(output)


@MESSAGEHTTP.route("/edit", methods=['PUT'])
def edit():
    input_obj = request.json
    output = message.message_edit(
        input_obj.get('token'),
        input_obj.get('message_id'),
        input_obj.get('message')
    )
    return jsonify(output)

@MESSAGEHTTP.route("/sendlater", methods=['POST'])
def sendlater():
    input_obj = request.json
    output = message.message_sendlater(
        input_obj.get('token'),
        input_obj.get('channel_id'),
        input_obj.get('message'),
        input_obj.get('time_sent')
    )
    return jsonify(output)

@MESSAGEHTTP.route("/react", methods=['POST'])
def react():
    input_obj = request.json
    output=message.message_react(
        input_obj.get('token'),
        input_obj.get('message_id'),
        input_obj.get('react_id')
    )
    return output

@MESSAGEHTTP.route("/unreact", methods=['POST'])
def unreact():
    input_obj = request.json
    output=message.message_unreact(
        input_obj.get('token'),
        input_obj.get('message_id'),
        input_obj.get('react_id')
    )
    return output

@MESSAGEHTTP.route("/pin", methods=['POST'])
def message_pin():
    input_obj = request.json
    output = message.message_pin(
        input_obj.get('token'),
        input_obj.get('message_id')
    )
    return jsonify(output)

@MESSAGEHTTP.route("/unpin", methods=['POST'])
def message_unpin():
    input_obj = request.json
    output = message.message_unpin(
        input_obj.get('token'),
        input_obj.get('message_id')
    )
    return jsonify(output)
