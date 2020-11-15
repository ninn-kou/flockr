'''
Sanity check for http
'''

from flask import Blueprint, request, jsonify

<<<<<<< HEAD:src/server/echo_http.py
from base.error import InputError
=======
from src.base.error import InputError
>>>>>>> deployment:src_backend/server/echo_http.py

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
