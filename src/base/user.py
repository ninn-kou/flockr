"""user.py written by Yuhan Yan."""

import requests
from PIL import Image

import src.data.data as data
from src.base.auth import check_in_users, regex_email_check, decode_token
from src.base.error import InputError

################################################################################
################################################################################
##
##    Yuhan Yan's work:
##    25 October, 2020
##
##      - user_profile(token, u_id));
##      - user_profile_setname(token, name_first, name_last);
##      - user_profile_setemail(token, email);
##      - user_profile_sethandle(token, handle_str);
##      - and all tests for these functions.
##
################################################################################
################################################################################

def user_profile(token, u_id):
    """For a valid user, returns information about their user_id, email, first name, last name, and handle.

    Raises:
        1. InputError
            - User with u_id is not a valid user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    # Avoid someone put a string
    try:
        u_id = int(u_id)
    except Exception as e:
        raise InputError('terrible uid') from e
    user = None

    for i in data.return_users():
        if i['u_id'] == u_id:
            user = i

    if user is None:
        raise InputError('not user')

    return {
        'user': {
            'u_id': u_id,
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            'profile_img_url': '',
        },
    }


def user_profile_setname(token, name_first, name_last):
    """Update the authorised user's first and last name.

    Raises:
        1. InputError
            - name_first is not between 1 and 50 characters inclusively in length
            - name_last is not between 1 and 50 characters inclusively in length
    """
    # decode the token
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')

    # Check first name matches requirements.
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('invalid first name')

    # Check Last Name matches requirements.
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('invalid last name')
    user=check_in_users("email",data.return_users(),email)
    user['name_first']=name_first
    user['name_last']=name_last
    data.updateByEmail(user,email)
    return {}

def user_profile_setemail(token, email):
    """Update the authorised user's email address.

    Raises:
        1. InputError
            - Email entered is not a valid email using the method provided
            - Email address is already being used by another user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email_now = person.get('email')

    regex_email_check(email)

    user = check_in_users('email', data.return_users(), email)
    if user is not None:
        raise InputError('Cannot use this email repeating :(')

    user = check_in_users('email', data.return_users(), email_now)

    user['email']=email
    data.updateByEmail(user,email_now)
    return {}


def user_profile_sethandle(token, handle_str):
    """Update the authorised user's handle (i.e. display name).

    Raises:
        1. InputError
            - handle_str must be between 3 and 20 characters
            - handle is already used by another user
    """
    person = decode_token(token)
    if person is None:
        return {'is_success': False}
    email = person.get('email')
    # handle_str must be between 3 and 20 characters
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError('1')
    user=check_in_users("email",data.return_users(),email)
    user['handle_str']=handle_str
    data.updateByEmail(user,email)
    return {}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """Upload the photo.

    Given a URL of an image on the internet, crops the image within bounds (x_start, y_start)
    and (x_end, y_end). Position (0,0) is the top left. It will save this file to be served.
    """
    # find the user specified
    user = decode_token(token)

    # get the profile picture
    r = requests.get(img_url, stream=True)

    # check whether the image is real
    if r.status_code != 200:
        raise InputError('Image did not return correctly')

    # open image
    try:
        img = Image.open(r.raw)
    except Exception as e:
        raise InputError('Input is not an image') from e
    # check if img is jpeg
    if img.format != 'JPEG':
        raise InputError('Please Input a JPEG as your Profile Picture')

    # make sure dimensions are valid
    if x_start < 0 or y_start < 0:
        raise InputError('Invalid Dimensions')
    if x_end < x_start or y_end < y_start:
        raise InputError('Invalid Dimensions')
    width, height = img.size
    if width < x_end or height < y_end:
        raise InputError('Invalid Dimensions')

    # crop the image
    cropped = img.crop((x_start, y_start, x_end, y_end))
    #  save image to directory
    data.save_image(cropped, user['u_id'])

    return {}
