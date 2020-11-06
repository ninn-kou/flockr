'''
Test Server to deliver cropped and uncropped images
'''

from json import dumps
from flask import Flask, send_file
from flask_cors import CORS

from pathlib import Path
import os

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
def jpg_one():
    '''lists all channels that exist'''
    path = 'test_one.jpg'
    return send_file(path, mimetype='image/gif')

@APP.route('/one/crop', methods = ['GET'])
def jpg_one_crop():
    '''lists all channels that exist'''
    path = 'test_one_cropped.jpg'
    return send_file(path, mimetype='image/gif')

@APP.route('/two', methods = ['GET'])
def jpg_two():
    '''lists all channels that exist'''
    path = 'test_two.jpg'
    return send_file(path, mimetype='image/gif')

@APP.route('/two/crop', methods = ['GET'])
def jpg_two_crop():
    '''lists all channels that exist'''
    path = 'test_two_cropped.jpg'
    return send_file(path, mimetype='image/gif')

@APP.route('/png')
def png():
    '''lists all channels that exist'''
    path = 'ttm.png'
    return send_file(path, mimetype='image/gif')

@APP.route('/txt')
def txt():
    '''lists all channels that exist'''
    path = 'test.txt'
    return send_file(path)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
