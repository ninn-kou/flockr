'''http functions'''
from flask import Blueprint, request, jsonify
import src.base.standup as standup

STANDUPHTTP = Blueprint('standup', __name__)

@STANDUPHTTP.route('/start', methods = ['POST'])
def start_su():
    input_obj = request.json
    output = standup.standup_start(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        int(input_obj.get('length'))
    )
    return jsonify(output)

@STANDUPHTTP.route('/active', methods = ['GET'])
def is_active():
    input_obj = request.args
    output = standup.standup_active(
        input_obj.get('token'),
        int(input_obj.get('channel_id'))
    )
    return jsonify(output)

@STANDUPHTTP.route('/send', methods = ['POST'])
def package_send():
    input_obj = request.json
    standup.standup_send(
        input_obj.get('token'),
        int(input_obj.get('channel_id')),
        input_obj.get('message')
    )
    return {}

