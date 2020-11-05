""" Yuhan Yan created this on 2020.10.25"""
from os import path
from flask import Blueprint, request, jsonify
from flask.helpers import send_file
from PIL import Image

import base.user as userB
from base.auth import decode_token

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

@USERHTTP.route('/uploadphoto', methods = ['POST'])
def uploadphoto():
    ''' uploads a photo '''

    # get the request json
    r = request.json
    user = decode_token(r.get('token'))
    u_id = str(user.get('u_id'))

    # crop the uploaded photo
    userB.user_profile_uploadphoto(
        r.get('token'),
        r.get('img_url'),
        r.get('x_start'),
        r.get('y_start'),
        r.get('x_end'),
        r.get('y_end')
    )
    
    # get the cropped photo path and return it
    cropped = 'data/profiles/' + u_id + '.jpg'
    return send_file(cropped, mimetype='image/gif')
