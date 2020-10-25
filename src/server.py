'''
Main file to run in order to run backend server
'''

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

# all functions base
APP.register_blueprint(auth_http.AUTHHTTP, url_prefix='/auth')
APP.register_blueprint(channel_http.CHANNELHTTP, url_prefix='/channel')
APP.register_blueprint(channels_http.CHANNELSHTTP, url_prefix='/channels')
APP.register_blueprint(message_http.MESSAGEHTTP, url_prefix='/meg')
APP.register_blueprint(other_http.OTHERHTTP, url_prefix='/other')
APP.register_blueprint(user_http.USERHTTP, url_prefix='/user/profile')

if __name__ == "__main__":
    APP.run(port=45411) # Do not edit this port
