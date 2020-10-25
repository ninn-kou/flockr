'''
Hao Ren
25 October, 2020

All URL appends are prepended with "message/"
'''

from flask import Blueprint, request, jsonify
import base.message as meg

MESSAGEHTTP = Blueprint('meg', __name__)

@MESSAGEHTTP.route("/send", methods=['POST'])
def send():
    input_obj = request.json

    output = meg.message_send(
        input_obj.get('token'),
        input_obj.get('channel_id'),
        input_obj.get('message')
    )

    return jsonify(output)

@MESSAGEHTTP.route("/remove", methods=['DELETE'])
def remove():
    input_obj = request.json

    meg.message_remove(
        input_obj.get('token'),
        input_obj.get('message_id')
    )


@MESSAGEHTTP.route("/edit", methods=['PUT'])
def edit():
    input_obj = request.json

    meg.message_edit(
        input_obj.get('token'),
        input_obj.get('message_id'),
        input_obj.get('message')
    )
