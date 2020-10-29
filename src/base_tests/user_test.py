from subprocess import Popen, PIPE
from time import sleep
import signal
import re

from PIL import Image
import pytest
import requests

import data.data as data
import base.user as user
from base.error import InputError
from base.other import clear
import base.auth as auth

def test_user_profile_correct_return():
    ''' checks correct return from login'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Test Person', 'Bam')

    token = registration['token']
    u_id = registration["u_id"]

    result = user.user_profile(token,u_id).get('user')

    # - Dict structure -> {u_id, token}
    assert isinstance(result, dict)
    # - u_id is an integer
    assert isinstance(result['email'], str)

    # - token is a string
    assert isinstance(result['name_first'], str)

    assert isinstance(result['name_first'], str)

    assert isinstance(result['name_last'], str)

    assert isinstance(result['handle_str'], str)

def test_user_profile_input_error_invalid_token():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    u_id = registration["u_id"]

    # # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')
    is_success = user.user_profile(invalid_token,u_id)
    assert is_success['is_success'] is False

def test_user_profile_input_error_invalid_u_id():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    with pytest.raises(InputError):
        user.user_profile(token, "3263fdhr")
    with pytest.raises(InputError):
        user.user_profile(token, 26157890314)

def test_user_profile_setname_correct_return():
    ''' checks correct return from login'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    result = user.user_profile_setname(token, "Mate1","Old2")

    # - Dict structure -> {u_id, token}
    assert isinstance(result, dict)

def test_user_profile_setname_invalid_token():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']

    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')
    is_success = user.user_profile_setname(invalid_token, "Mate","Old")
    assert is_success['is_success'] is False

def test_user_profile_setname_invalid_name():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']

    with pytest.raises(InputError):
        user.user_profile_setname(token, '', 'Old')
    with pytest.raises(InputError):
        user.user_profile_setname(token, 'Mate', '')

##################################################################################
def test_user_profile_setemail_correct_return():
    ''' checks correct return from login'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    email = "236ggg@example.com"
    result = user.user_profile_setemail(token, email)

    # - Dict structure -> {u_id, token}
    assert isinstance(result, dict)

def test_user_profile_email_input_error_invalid_token():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    email = "valid@example.com"

    # # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')
    is_success = user.user_profile_setemail(invalid_token, email)
    assert is_success['is_success'] is False

def test_user_profile_input_error_invalid_email():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    with pytest.raises(InputError):
        user.user_profile_setemail(token, "invalid@example")

def test_user_profile_input_error_existing_email():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    with pytest.raises(InputError):
        user.user_profile_setemail(token, "valid@example.com")

#####################################################################################################


def test_user_profile_sethandle_correct_return():
    ''' checks correct return from login'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    handle_str = "rhj53453h"
    result = user.user_profile_sethandle(token, handle_str)

    # - Dict structure -> {u_id, token}
    assert isinstance(result, dict)

def test_user_profile_handle_input_error_invalid_token():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    handle_str = "rhj53453h"

    # # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')
    is_success = user.user_profile_sethandle(invalid_token, handle_str)
    assert is_success['is_success'] is False


def test_user_profile_handle_input_error_invalid_handle():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "27")
    with pytest.raises(InputError):
        user.user_profile_setemail(token, "2367brehjrtjehjtrghjtjrtjtjk")

@pytest.fixture
def url():
    ''' start server and create url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/base_tests/uploadphoto_test/upload_server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_user_profile_uploadphoto(url):
    '''
    Given a URL of an image on the internet, crops the image within bounds (x_start, y_start)
    and (x_end, y_end). Position (0,0) is the top left.

    (token, img_url, x_start, y_start, x_end, y_end)

    {}

    InputError when any of:
    img_url returns an HTTP status other than 200.
    any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
    Image uploaded is not a JPG
    '''

    # get the first test image from the test server
    url_time = url + '/one'
    r = requests.get(url_time, stream=True)
    test_image = Image.open(r.raw)

