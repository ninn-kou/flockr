def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
