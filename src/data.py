# a collection of data structures used between programs


###########################################################################
"""
The User Data Structure
NOT SURE 

The Spec says to store it like this:
users = [
    user: {
        'u_id': 
        'email': ''
        'name_first':'',
        'name_last':'',
        'handle_str': '',
        'token': ''
    }
]

Issue is:
1. How to validate tokens? Are tokens stored in auth.py?
2. How to find each user in the list? Is u_id just used as a list address?

"""
users = []

# initialise the users list
def init_users():
    global users 

def append_users(user):
    users.append(user)

# def pop_users(user):
#     users.pop(user)

########################################################################################

"""
the struct using for channel 
channels = [    
    channel:  { 
        'name': 'Hayden',
        'channel_id':
        'owner': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],   
        'is public': True,
        'messages':[]  
    }
]

"""
channels = []