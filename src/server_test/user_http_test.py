""" Yuhan Yan created this on 2020.10.25"""
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests
import pytest
from server_test.channel_http_test import send_request_json
from base_tests.user_test import compare_images
import data.data as data
import base.auth as auth
from PIL import Image

# copy-pasted this straight out of echo_http_test.py
# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    ''' start server and create url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
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

def clear(url):
    send_request_json('DELETE', url, 'clear', {})

def register_user(url, email, password, name_first, name_last):
    ''' register a new user '''
    return send_request_json('POST', url, 'auth/register', {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

def test_profile(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    user = requests.post(url + 'auth/register',
                         json={
                             'email': 'test@example.com',
                             'password': 'emilyisshort',
                             'name_first': 'Emily',
                             'name_last': 'Luo?'
                         })


    user=json.loads(user.text)
    token=user["token"]
    u_id=user['u_id']

    # log that user out with returned jwt
    result = requests.get(url + 'user/profile/?token='+token+"&u_id="+str(u_id))
    # make sure logging out user was successful
    assert json.loads(result.text)['user']['email']

def test_setprofile_email(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register the user
    user = requests.post(url + 'auth/register',
                         json={
                             'email': 'test@example.com',
                             'password': 'emilyisshort',
                             'name_first': 'Emily',
                             'name_last': 'Luo?'
                         })


    user=json.loads(user.text)
    token=user["token"]
    u_id=user["u_id"]
    result = requests.put(url + 'user/profile/setemail',
    json = {
        'token': token,
        "email": 'test23@example.com'
    })


    # log that user out with returned jwt
    # make sure logging out user was successful
    assert json.loads(result.text) is not None
    result = requests.get(url + 'user/profile/?token='+token+"&u_id="+str(u_id))
    user=json.loads(result.text)
    assert user['user']["email"]=="test23@example.com"
#
#
#
#
#
#
def test_setprofile_name(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register the user
    user = requests.post(url + 'auth/register',
                         json={
                             'email': 'test@example.com',
                             'password': 'emilyisshort',
                             'name_first': 'Emily',
                             'name_last': 'Luo?'
                         })


    user=json.loads(user.text)
    token=user["token"]
    u_id=user['u_id']

    result = requests.put(url + 'user/profile/setname',
    json = {
        'token': token,
        "name_first": 'Morb',
        "name_last": 'Old'
    })

    # log that user out with returned jwt
    # make sure logging out user was successful
    assert json.loads(result.text) is not None

    result = requests.get(url + 'user/profile/?token='+token+"&u_id="+str(u_id))
    user=json.loads(result.text)

    assert user['user']["name_first"]=="Morb"
    assert user['user']["name_last"]=="Old"

def test_setprofile_handle(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})


    # register the user
    user = requests.post(url + 'auth/register',
                         json={
                             'email': 'test@example.com',
                             'password': 'emilyisshort',
                             'name_first': 'Emily',
                             'name_last': 'Luo?'
                         })


    user=json.loads(user.text)
    token=user["token"]
    u_id=user['u_id']

    result = requests.put(url + 'user/profile/sethandle',
    json = {
        'token': token,
        "handle_str": 'ege64ydegehg',
    })

    assert json.loads(result.text) is not None

    result = requests.get(url + 'user/profile/?token='+token+"&u_id="+str(u_id))
    user=json.loads(result.text).get('user')
    assert user["handle_str"]=="ege64ydegehg"
    # clear out the databases
    requests.delete(url + 'clear', json={})

@pytest.fixture
def example():
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

def test_uploadphoto(url, example):
    ''' test to see if uploaded crop is correct '''
    clear(url)

    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')

    # get the url for the image from local image server
    url_test = example + 'one'
    url_cropped = url_test + '/crop'

    # get the first already cropped image from the test server
    r = requests.get(url_cropped, stream=True)
    test_image = Image.open(r.raw)

    # get the first image cropped
    r = requests.post(url + 'user/profile/uploadphoto', json = {
        'token': user1.get('token'),
        'img_url': url_test,
        'x_start': 0,
        'y_start': 0,
        'x_end': 10,
        'y_end': 10
    }, stream=True )
    saved_image = Image.open(r.raw)

    # check that image was cropped correctly
    assert compare_images(test_image, saved_image) == True

def test_uploadphoto_two(url, example):
    ''' test to see if uploaded crop is correct '''
    clear(url)

    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')

    # get the url for the image from local image server
    url_test = example + 'two'
    url_cropped = url_test + '/crop'

    # get the first already cropped image from the test server
    r = requests.get(url_cropped, stream=True)
    test_image = Image.open(r.raw)

    # get the first image cropped
    r = requests.post(url + 'user/profile/uploadphoto', json = {
        'token': user1.get('token'),
        'img_url': url_test,
        'x_start': 400,
        'y_start': 400,
        'x_end': 800,
        'y_end': 800
    }, stream=True )
    saved_image = Image.open(r.raw)

    # check that image was cropped correctly
    assert compare_images(test_image, saved_image) == True

def test_return_photo(url, example):
    ''' test that the photos returned are correct '''
    clear(url)

    user1 = register_user(url, 'test@example.com', 'emilyisshort', 'Emily', 'Luo')

    # get the url for the image from local image server
    url_test = example + 'two'

    # get the first image cropped
    r = requests.post(url + 'user/profile/uploadphoto', json = {
        'token': user1.get('token'),
        'img_url': url_test,
        'x_start': 400,
        'y_start': 400,
        'x_end': 800,
        'y_end': 800
    }, stream=True )
    saved_image = Image.open(r.raw)

    image_url = auth.decode_token(user1['token'])['profile_img_url']
    r = requests.get(image_url, stream=True)
    returned_image = Image.open(r.raw)

    # check that image was saved correctly
    assert compare_images(returned_image, saved_image) == True
    clear(url)
