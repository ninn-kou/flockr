'''
Joseph Jeong 15 OCT 2020

After experimentation with Flask Blueprints, I'm setting up a server to allow auth.py
to interface with the frontend

'''

import re
from re import L
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

def register_user(email, password, name_first, name_last):
    resp = requests.post(url + 'auth/register',
    json = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

    return json.loads(resp.text)

def test_invite(url):
    ''' testing channel_invite requests '''

    # clear out the databases
    clear()

def test_details(url):
    ''' testing channel_details requests '''

    # clear out the databases
    clear()

    # register a new user
    user = register_user('test@example.com', 'emilyisshort', 'Emily', 'Luo')

    response = requests.post(url + 'channel/invite', 
    json = {
        'token': user.get('token'),
        'channel_id': 'yep'
    })
    

def test_messages(url):
    ''' testing channel_messages requests '''

    # clear out the databases
    clear()



def test_leave(url):
    ''' testing channel_leave requests '''

    # clear out the databases
    clear()

def test_join(url):
    ''' testing channel_join requests '''

    # clear out the databases
    clear()

def test_addowner(url):
    ''' testing channel_join requests '''

    # clear out the databases
    clear()

def test_removeowner(url):
    ''' testing channel_removeowner requests '''

    # clear out the databases
    clear()