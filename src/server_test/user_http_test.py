""" Yuhan Yan created this on 2020.10.25"""
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests

import pytest

import data.data as data
from base.other import clear

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

def test_profile(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    clear()

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
    assert json.loads(result.text)['email']

def test_setprofile_email(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    clear()
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
    assert user["email"]=="test23@example.com"
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
    clear()

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
    print(user)
    assert user["name_first"]=="Morb"
    assert user["name_last"]=="Old"

def test_setprofile_handle(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    clear()

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
    user=json.loads(result.text)
    assert user["handle_str"]=="ege64ydegehg"