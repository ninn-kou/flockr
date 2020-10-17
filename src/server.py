'''
Main file to run in order to run backend server
'''

from json import dumps
from flask import Flask, request
from flask_cors import CORS
from base.error import InputError

import server.auth_http as auth_http
import server.echo_http as echo_http

def default_handler(err):
    ''' system error handler '''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# echo test
APP.register_blueprint(echo_http.ECHOHTTP)

# all functions from auth.py
APP.register_blueprint(auth_http.AUTHHTTP, url_prefix='/auth')

if __name__ == "__main__":
    APP.run(port=45411) # Do not edit this port
