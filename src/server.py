'''
Main file to run in order to run backend server
'''

import socket
from contextlib import closing

from json import dumps
from flask import Flask
from flask_cors import CORS

import server.auth_http as auth_http
import server.channel_http as channel_http
import server.channels_http as channels_http
import server.echo_http as echo_http
import server.message_http as message_http
import server.other_http as other_http
import server.user_http as user_http
import data.data as data

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

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# echo test
APP.register_blueprint(echo_http.ECHOHTTP)

# all functions base
APP.register_blueprint(auth_http.AUTHHTTP, url_prefix='/auth')
APP.register_blueprint(channel_http.CHANNELHTTP, url_prefix='/channel')
APP.register_blueprint(channels_http.CHANNELSHTTP, url_prefix='/channels')
APP.register_blueprint(message_http.MESSAGEHTTP, url_prefix='/message')
APP.register_blueprint(other_http.OTHERHTTP)
APP.register_blueprint(user_http.USERHTTP, url_prefix='/user/profile')

if __name__ == "__main__":
    # find a free port
    port = find_free_port()
    data.save_port(port)
    APP.run(port=port)
