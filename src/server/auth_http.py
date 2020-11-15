'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with auth/
'''

from flask import Blueprint, request, jsonify

<<<<<<< HEAD:src/server/auth_http.py
import base.auth as auth
=======
import src.base.auth as auth
>>>>>>> deployment:src_backend/server/auth_http.py

AUTHHTTP = Blueprint('auth', __name__)

@AUTHHTTP.route('/register', methods = ['POST'])
def register():
    ''' registers a new user'''

    # get the user from json
    user = request.json

    token = auth.auth_register(
        user.get('email'),
        user.get('password'),
        user.get('name_first'),
        user.get('name_last')
    )

    # return token object as json
    return jsonify(token)

@AUTHHTTP.route('/login', methods = ['POST'])
def login():
    ''' logs the user in'''

    # get the user from json
    user = request.json

    token = auth.auth_login(
        user.get('email'),
        user.get('password')
    )

    # return token object as json
    return jsonify(token)

@AUTHHTTP.route('/logout', methods = ['POST'])
def logout():
    ''' logs the user out'''

    # get the user from json
    user = request.json

    success = auth.auth_logout(
        user.get('token')
    )

    # return token object as json
    return jsonify(success)

@AUTHHTTP.route('/passwordreset/request', methods = ['POST'])
def passwordreset_request():
    ''' requests a reset email '''

    # get the user from json
    user = request.json

    success = auth.passwordreset_request(
        user.get('email')
    )

    # return token object as json
    return jsonify(success)

@AUTHHTTP.route('/passwordreset/reset', methods = ['POST'])
def passwordreset_reset():
    ''' resets password '''

    # get the user from json
    user = request.json

    success = auth.passwordreset_reset(
        user.get('reset_code'),
        user.get('new_password')
    )

    # return token object as json
    return jsonify(success)