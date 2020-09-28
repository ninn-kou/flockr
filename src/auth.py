import data
from error import InputError
import re
import random
import string

# dict that holds token objects
#tokens stored locally in a dict
"""
{
    'u_id': u_id,
    'token': token
}
"""
tokens = {}

# checks that the email is validly formatted email
def regex_email_check(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)) == False:  
        raise InputError
    
    return
# Check if email is already in database
# assuming every user object has an email

"""
expecting users data structure looking like:
users = [
    user: {
        'u_id': 
        'email': ''
        'name_first':'',
        'name_last':'',
        'handle_str': ''
    }
]
"""
def users_email_check(email, users):
    for user in users:
        if user['email'] == email:
            raise InputError
    return


def auth_login(email, password):
    # initialise user data
    data.init_users()
    print(data.users)



    """
    return {
        'u_id': 1,
        'token': '12345',
    }
    """

def auth_logout(token):
    return {
        'is_success': True,
    }

#handles error checking for auth_register
def auth_register_error_check(email, password, name_first, name_last):
    # initialise user data
    data.init_users()

    # check for valid input
    regex_email_check(email)
    
    # check if email is already used
    users_email_check(email, data.users)

    # check len(password) >= 6
    if len(password) < 6:
        raise InputError

    #check first name matches requirements
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError

    #check Last Name matches requirements
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    return

# create a random 32 bit unsigned integer to use as a u_id
def create_u_id(users):
    # create a random 32 bit unsigned integer
    u_id = random.randint(0, 0xFFFFFFFF)
    print(u_id)

    # simple recursive function to check whether u_id is unique
    for user in users:
        if user['u_id'] == u_id:
            u_id = create_u_id(u_id, users)
            break
    
    return u_id

# create a 20 character long ascii string for token    
def create_token(u_id):

    # create list of random characters and length of token
    valid_characters = string.ascii_letters + string.digits + string.punctuation
    token_length = 20

    # create a random token
    token = "".join(random.choices(valid_characters, k = token_length))

    # check that token is unique
    for token_object in tokens:
        if token_object[u_id] != u_id and token_object['token'] == token:
            token = create_token(u_id)
            break

    return token

def auth_register(email, password, name_first, name_last):
    
    # checks for InputError
    auth_register_error_check(email, password, name_first, name_last)

    # create a unique u_id
    u_id = create_u_id(data.users)

    # creates a random and unique token
    token = create_token(u_id)

    # creates an object with u_id and token
    token_object = {
        'u_id': u_id,
        'token': token
    }

    return token_object

print(auth_register('hello@gmail.com', 'password', 'hello', 'there'))



