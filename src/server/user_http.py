""" Yuhan Yan created this on 2020.10.25"""
from os import path
from flask import Blueprint, request, jsonify
from flask.helpers import send_file

<<<<<<< HEAD:src/server/user_http.py
import base.user as userB
from base.auth import decode_token
import data.data as data
=======
import src.base.user as userB
from src.base.auth import decode_token
import src.data.data as data
>>>>>>> deployment:src_backend/server/user_http.py

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
    success['user']['profile_img_url'] = data.get_profile_photo_url(u_id)
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
<<<<<<< HEAD:src/server/user_http.py
    cropped = 'data/profiles/' + u_id + '.jpg'
=======
    cropped = 'src/data/profiles/' + u_id + '.jpg'
>>>>>>> deployment:src_backend/server/user_http.py

    # updata the user profile_img_url
    user = decode_token(r.get('token'))
    user['profile_img_url'] = data.get_profile_photo_url(user['u_id'])
    data.updateByEmail(user, user['email'])

    return send_file(cropped, mimetype='image/gif')

@USERHTTP.route('/photo/<u_id>', methods = ['GET'])
def photo(u_id):
    ''' return the photo involved '''

    # check the photo path
    path = data.get_profile_photo_path(u_id)

    # send the path
    return send_file(path, mimetype='image/gif')