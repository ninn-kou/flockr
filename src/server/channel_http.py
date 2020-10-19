'''
Joseph Jeong 15 OCT 2020

Just experimenting with how Flask works at the moment
All url appends are prepended with auth/
'''

from flask import Blueprint, request, jsonify

import base.channel as channel

CHANNELHTTP = Blueprint('channel', __name__)

