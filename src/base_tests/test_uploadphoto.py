''' file to test the uploadphoto function '''

from subprocess import Popen, PIPE
from time import sleep
import signal
import re

from PIL import Image
import pytest
import requests

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

def test_invalid_token():
    pass
