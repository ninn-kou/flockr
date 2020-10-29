'''
Main file to run in order to run backend server
'''

from json import dumps
from flask import Flask, send_file
from flask_cors import CORS

from pathlib import Path

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

@APP.route('/one', methods = ['GET'])
def list():
    '''lists all channels that exist'''
    path = 'test_one_cropped.jpg'
    return send_file(path, mimetype='image/gif')

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
