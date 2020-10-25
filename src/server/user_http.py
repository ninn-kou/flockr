""" Yuhan Yan created this on 2020.10.25"""
from flask import Blueprint, request, jsonify

import base.user as userB

USERHTTP = Blueprint('user', __name__)

@USERHTTP.route('/', methods = ['GET'])
def profile():
    ''' registers a new user'''

    # get the user from json
    token = request.args.get("token")
    u_id = request.args.get("u_id")

    success = userB.user_profile(
        token,
        u_id
    )

    return jsonify(success)

@USERHTTP.route('/setname', methods = ['PUT'])
def setname():
    ''' logs the user in'''

    # get the user from json
    user = request.json

    success = userB.user_profile_setname(
        user.get('token'),
        user.get('name_first'),
        user.get('name_last'),
    )

    return jsonify(success)

@USERHTTP.route('/setemail', methods = ['PUT'])
def setemail():
    ''' logs the user out'''

    # get the user from json
    user = request.json

    success = userB.user_profile_setemail(
        user.get('token'),
        user.get('email')
    )

    return jsonify(success)


@USERHTTP.route('/sethandle', methods = ['PUT'])
def sethandle():
    ''' logs the user out'''

    # get the user from json
    user = request.json

    success = userB.user_profile_sethandle(
        user.get('token'),
        user.get('handle_str')
    )

    # return token object as json
    return jsonify(success)

