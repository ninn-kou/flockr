'''
Hao Ren
25 October, 2020

All URL appends are prepended with "other/"
'''

from flask import Blueprint, request, jsonify
import base.other as other

OTHERHTTP = Blueprint('other', __name__)

@OTHERHTTP.route("/clear", methods=['DELETE'])
def clear():
    other.clear()

@OTHERHTTP.route("/users_all", methods=['GET'])
def users_all():
    input_obj = request.json

    output = other.users_all(
        input_obj.get('token')
    )
    return jsonify(output)

@OTHERHTTP.route("/permission_change", methods=['POST'])
def userpermission_change():
    input_obj = request.json

    other.admin_userpermission_change(
        input_obj.get('token'),
        input_obj.get('u_id'),
        input_obj.get('permission_id')
    )

@OTHERHTTP.route("/search", methods=['GET'])
def search():
    input_obj = request.json

    output = other.search(
        input_obj.get('token'),
        input_obj.get('query_str')
    )
    return jsonify(output)
