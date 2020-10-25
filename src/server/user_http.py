'''
Hao Ren
25 October, 2020

All URL appends are prepended with "/user/profile"
'''

from flask import Blueprint, request, jsonify
import base.user as user

USERHTTP = Blueprint('user', __name__)

@USERHTTP.route("/profile", methods=['GET'])
def profile():
    input_obj = request.json
    output = user.user_profile(
        input_obj.get('token'),
        input_obj.get('u_id')
    )
    return jsonify(output)

@USERHTTP.route("/setname", methods=['PUT'])
def setname():
    input_obj = request.json
    user.user_profile_setname(
        input_obj.get('token'),
        input_obj.get('name_first'),
        input_obj.get('name_last')
    )

@USERHTTP.route("/setemail", methods=['PUT'])
def setemail():
    input_obj = request.json
    user.user_profile_setemail(
        input_obj.get('token'),
        input_obj.get('email')
    )

@USERHTTP.route("/setthandle", methods=['PUT'])
def sethandle():
    input_obj = request.json
    user.user_profile_sethandle(
        input_obj.get('token'),
        input_obj.get('handle_str')
    )
