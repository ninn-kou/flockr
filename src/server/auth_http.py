'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
'''

from flask import Blueprint, request
from json import dumps
import werkzeug
from werkzeug.exceptions import BadRequest

import time

import base.auth

AUTHHTTP = Blueprint('auth', __name__)

@AUTHHTTP.route('/login', methods = ['POST'])
def login():
    '''
    Simple function that calls the http requests for auth.py 
    And handles the relevant errors
    '''
    # get the variables
    email = request.json.get('email')
    password = request.json.get('password')

    # # if request is invalid
    # if (email is None or password is None):
    #     print("why")
    #     raise BadRequest
    
    # trigger the function
    token = auth.auth_login(email, password)

    print(token)
    time.sleep(2)
    print('this triggers')
    return dumps(token)


# @AUTHHTTP.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     ''' handle 400 HTTP errors'''
#     print('HUH')
#     return '400 Bad Request', 400