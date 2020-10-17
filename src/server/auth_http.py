'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with auth/
'''

from flask import Blueprint, request, jsonify

import base.auth as auth

AUTHHTTP = Blueprint('auth', __name__)

@AUTHHTTP.route('/register', methods = ['POST'])
def register():

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

    # get the user from json
    user = request.json

    success = auth.auth_logout(
        user.get('token')
    )
    
    # return token object as json
    return jsonify(success)