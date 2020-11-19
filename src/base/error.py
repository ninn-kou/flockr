"""
File to outline exception types
"""
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    """Access Error"""
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    """Input Error"""
    code = 400
    message = 'No message specified'
