'''
Joseph Jeong 15 OCT 2020

After experimentation with Flask Blueprints, I'm setting up a server to allow auth.py
to interface with the frontend

'''

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import json
import requests

import pytest

import src.data.data as data

# copy-pasted this straight out of echo_http_test.py
# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    ''' start server and create url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
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

def test_register(url):
    '''
    Test whether requests sent to auth_http for auth_register come back
    '''
    # clear out the databases
    requests.delete(url + 'other/clear', json={})

    resp = requests.post(url + 'auth/register',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort',
        'name_first': 'Emily',
        'name_last': 'Luo?'
        })

    text = json.loads(resp.text)

    focus_user = None

    for user in data.return_users():
        if user['u_id'] == text.get('u_id'):
            focus_user = user
            break

    assert focus_user is not None
    assert focus_user.get('email') == 'test@example.com'


def test_login(url):
    '''
    Test whether requests sent to auth_http for auth_register come back
    '''
    # clear out the databases

    requests.delete(url + 'clear', json={})

    register_text = requests.post(url + 'auth/register',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort',
        'name_first': 'Emily',
        'name_last': 'Luo?'
        })
    auth_text = requests.post(url + 'auth/login',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort'
    })

    # make sure u_id are matching both times
    assert json.loads(register_text.text).get('u_id') == json.loads(auth_text.text).get('u_id')

def test_logout(url):
    '''
    Test whether request actually logs the person out
    '''
    # clear out the databases
    requests.delete(url + 'clear', json={})


    # register the user
    user = requests.post(url + 'auth/register',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort',
        'name_first': 'Emily',
        'name_last': 'Luo?'
    })

    # log that user out with returned jwt
    token = requests.post(url + 'auth/logout',
    json = {
        'token': json.loads(user.text).get('token')
    })

    # make sure logging out user was successful
    assert json.loads(token.text).get('is_success')

def test_passwordreset_request(url):
    ''' test whether the request is sent '''
    # clear out the databases
    requests.delete(url + 'clear', json={})

    # register the user
    requests.post(url + 'auth/register',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort',
        'name_first': 'Emily',
        'name_last': 'Luo?'
    })

    r = requests.post(url + 'auth/passwordreset/request',
    json = {
        'email': 'test@example.com'
    })

    assert r.status_code == 200

def get_reset_code(u_id):
    ''' helper function to get the password code '''

    for user in data.return_users():
        if user['u_id'] == u_id:
            return user.get('password_reset')

def test_passwordreset_reset(url):
     # clear out the databases
    requests.delete(url + 'clear', json={})

    # register the user
    user = requests.post(url + 'auth/register',
    json = {
        'email': 'test@example.com',
        'password': 'emilyisshort',
        'name_first': 'Emily',
        'name_last': 'Luo?'
    })

    # ask for the code
    requests.post(url + 'auth/passwordreset/request',
    json = {
        'email': 'test@example.com'
    })

    # find the code
    code = get_reset_code(json.loads(user.text).get('u_id')).get('code')

    # reset the code
    r = requests.post(url + 'auth/passwordreset/reset',
    json = {
        'reset_code': code,
        'new_password': 'validpassword'
    })

    assert r.status_code == 200
