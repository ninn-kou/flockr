# About the Assumption
* It is assumed that **tokens** are produced randomly with possible numbers and characters. Each token is a string with 20 chars.
* It uses all chars a-z, A-Z, 0-9, and !@#$%^&*()-_=+,./? using the ASCII spec
* It is assumed that **user IDs** are unique and random with min 0 and max 4,294,967,295 (0xFFFFFFFF)
* It is assumed that **channel IDs** are unique and random with min 0 and max 4,294,967,295 (0xFFFFFFFF)



* It is assumed that user struct is like this:
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle
    }
* It is assumed that token struct is like this:
    token_object = {
        'u_id': u_id,
        'token': token
    }

# Channel

* when the user create the channel, the user became the owenr automaticlly.
* It is assumed that the channel struct is like this:
    channel = { 
        'name': 'Hayden',
        'channel_id':' '
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

* channl message: for each channel, the new message is inserted in the begaining of message list.
