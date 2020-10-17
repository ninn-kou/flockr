'''
Sanity check for http
'''

from flask import Blueprint, request, jsonify

from base.error import InputError

ECHOHTTP = Blueprint('echo', __name__)

@ECHOHTTP.route("/echo", methods=['GET'])
def echo():
    '''
    sanity test domain for echo
    No other purpose than a basic server test
    '''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return jsonify({
        'data': data
    })
