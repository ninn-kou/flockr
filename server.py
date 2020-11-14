'''
Main file to run in order to run server

This is an integrated server.py and frontend.py flask server using blueprints
'''

import os
import socket
from contextlib import closing

from json import dumps, dump
from flask import Flask
from flask_cors import CORS

import src_backend.base.auth as auth

import src_backend.server.auth_http as auth_http
import src_backend.server.channel_http as channel_http
import src_backend.server.channels_http as channels_http
import src_backend.server.echo_http as echo_http
import src_backend.server.message_http as message_http
import src_backend.server.other_http as other_http
import src_backend.server.user_http as user_http
import src_backend.data.data as data
import src_backend.server.standup_http as standup_http

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
    ''' a helper function which finds a free port '''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def save_port(port):
    ''' saves the port that the server is currently running on '''

    # check if the file already exists
    # if not, create it
    path = os.getcwd() + '/src_backend/data/port.json'

    # dump port into it
    with open(path, 'w') as file:
        dump({'port': port}, file)

APP = Flask(__name__, static_folder='prebundle')
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
APP.register_blueprint(standup_http.STANDUPHTTP, url_prefix='/standup')

if __name__ == "__main__":
    # find a free port
    port = find_free_port()
    print(port)
    save_port(port)
    auth
    APP.run(port=port, threaded=True)
