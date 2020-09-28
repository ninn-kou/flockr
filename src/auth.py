import data
from error import InputError
import re
import random
import string

# dict that holds token objects
# tokens stored locally in a dict

# this is implemented wrong reee
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

# check for a particular data type in users list
def check_in_users(data_type, users, item):
    focus_user = None
    for user in users:
        if user[data_type] == item:
            focus_user = user
            break
    if focus_user == None:
        raise InputError
    return focus_user


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

    # focus_user = None
    # for user in data.users:
    #     if email == user['email']:
    #         focus_user = user
    #         break
    # if focus_user == None:
    #     raise InputError

def auth_login(email, password):
    # initialise user data
    data.init_users()

    # check if email is valid
    users_email_check(email)
    
    # check if email is used by user
    # will raise InputError if user is not stored
    focus_user = check_in_users('email', data.users, email)

    # check password
    if focus_user['password'] != password:
        raise InputError
    
    # if everything checks out, create token
    token = create_token(focus_user['u_id'])

    # creates an object with u_id and token
    token_object = {
        'u_id': u_id,
        'token': token
    }

    return token_object

    """
    return {
        'u_id': 1,
        'token': '12345',
    }
    """

def auth_logout(token):

    focus_token = None

    # search for token in token dict
    for token_object in tokens:
        if token_object['token'] == token:
            focus_token = token_object
            break
    
    # Returns accordingly if token is found
    if focus_token == None:
        return {'is_success': False}
    else:
        tokens.pop(focus_token)
        return {'is_success': True}

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

# creates variable numbers at the end of the string
def handle_variabliser(handle, variabliser_num, users):

    # check if the handle is unique
    check = check_in_users('handle_str', users, handle)

    # if somehow every single handle is created
    if variabliser_num > 20:
        raise Exception("Have Made Every Single Possible Handle")

    # if not modify it further
    if check != None:
        # need to modify it further
        variabliser_num += 1

        # variabilise the string accordingly
        handle = handle[0:(-1 * variabliser_num)]
        variabliser = string.ascii_letters + string.digits
        handle.join(random.chocies(variabliser, k = variabliser_num))

        handle = handle_variabliser(handle, variabliser_num, users)
    
    return handle

# generates a unique handle
def handle_generator(name_first, name_last, users):

    # create base concatenation
    raw_concatenation = name_first + name_last
    if len(raw_concatenation) > 20:
        raw_concatenation = raw_concatenation[:20]
    
    # create a unique handle
    handle = handle_variabliser(raw_concatenation, 0, users)

    return handle


def auth_register(email, password, name_first, name_last):
    
    # checks for InputError
    auth_register_error_check(email, password, name_first, name_last)

    # create a unique u_id
    u_id = create_u_id(data.users)

    # creates a random and unique token
    token = create_token(u_id)

    # generate handle
    handle = handle_generator(name_first, name_last, data.users)

    # create and store a user object
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': ''
    }

    # creates an object with u_id and token
    token_object = {
        'u_id': u_id,
        'token': token
    }

    return token_object

data.init_users()

handle = handle_generator('BobbyMcGee','GeoffHarley', data.users)
print(len(handle))


