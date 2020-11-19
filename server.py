"""
Main file to run backend server.
"""

import os
import socket
from contextlib import closing

from json import dumps, dump
from flask import Flask
from flask_cors import CORS

import src.base.auth as auth
import src.data.data as data

import src.server.auth_http as auth_http
import src.server.channel_http as channel_http
import src.server.channels_http as channels_http
import src.server.echo_http as echo_http
import src.server.message_http as message_http
import src.server.other_http as other_http
import src.server.user_http as user_http
import src.server.standup_http as standup_http

def default_handler(err):
    """System error handler."""
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

def save_port(port):
    """Saves the port that the server is currently running on."""
    # check if the file already exists
    # if not, create it
    path = os.getcwd() + '/src/data/port.json'

    # dump port into it
    with open(path, 'w') as file:
        dump({'port': port}, file)

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# Echo test:
APP.register_blueprint(echo_http.ECHOHTTP)

# All functions base:
APP.register_blueprint(auth_http.AUTHHTTP, url_prefix='/auth')
APP.register_blueprint(channel_http.CHANNELHTTP, url_prefix='/channel')
APP.register_blueprint(channels_http.CHANNELSHTTP, url_prefix='/channels')
APP.register_blueprint(message_http.MESSAGEHTTP, url_prefix='/message')
APP.register_blueprint(other_http.OTHERHTTP)
APP.register_blueprint(user_http.USERHTTP, url_prefix='/user/profile')
APP.register_blueprint(standup_http.STANDUPHTTP, url_prefix='/standup')

# Main:
if __name__ == "__main__":
    # find a free port
    port = find_free_port()
    print(port)
    save_port(port)
    auth.read_jwt_secret()  # To create the jwt_secret file.
    APP.run(port=port)
