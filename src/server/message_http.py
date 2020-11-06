'''
Hao Ren
25 October, 2020

All URL appends are prepended with "message/"
'''

from flask import Blueprint, request, jsonify
import base.message as message

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
    now = datetime.utcnow()
    timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    t = threading.Timer(time_sent - timestamp,
    output = message.message_sendlater(
    input_obj.get('token'),
    input_obj.get('channel_id'),
    input_obj.get('message'),
    input_obj.get('time_sent')
    ))
    t.start()


    return jsonify(output)

@MESSAGEHTTP.route("/pin", methods=['POST'])
def message_pin():
    input_obj = request.json
    output = message.message_pin(
        input_obj.get('token'),
        input_obj.get('message_id')
    )

    return jsonify(output)