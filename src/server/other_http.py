"""
other_http.py written by Hao Ren.

All URL appends are prepended with `other/`.
"""

from flask import Blueprint, request, jsonify

import src.base.other as other
import src.data.data as data

OTHERHTTP = Blueprint('other', __name__)

@OTHERHTTP.route("/clear", methods=['DELETE'])
def clear():
    return jsonify(other.clear())

@OTHERHTTP.route("/users/all", methods=['GET'])
def users_all():
    input_obj = request.args
    output = other.users_all(
        input_obj.get('token')
    )
    for i in output['users']:
        i['profile_img_url'] = data.get_profile_photo_url(i['u_id'])
    return jsonify(output)

@OTHERHTTP.route("/admin/userpermission/change", methods=['POST'])
def userpermission_change():
    input_obj = request.json
    output = other.admin_userpermission_change(
        input_obj.get('token'),
        input_obj.get('u_id'),
        input_obj.get('permission_id')
    )
    return jsonify(output)


@OTHERHTTP.route("/search", methods=['GET'])
def search():
    input_obj = request.args
    output = other.search(
        input_obj.get('token'),
        input_obj.get('query_str')
    )
    return jsonify(output)
