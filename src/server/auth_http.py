'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with auth/
'''

from flask import Blueprint, request, jsonify

import base.auth as auth

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

    print(email)
    print(password)
    # # trigger the function
    token = auth.auth_login(email, password)

    print(token)

    # return dumps(token)
    return dumps({'hi': 'boo', 'thing': 'colour!'})


@AUTHHTTP.route('/register', methods = ['POST'])
def register():

    user = request.json
    print(user)

    token = auth.auth_register(
        user.get('email'),
        user.get('password'),
        user.get('name_first'),
        user.get('name_last')
    )
    print(token)
    token['u_id'] = str(token['u_id'])
    return jsonify(token)
    # return dumps({'hi': 'boo', 'thing': 'colour!'})