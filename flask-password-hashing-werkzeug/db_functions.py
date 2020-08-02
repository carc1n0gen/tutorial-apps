"""
Use a real database in a real app, this is all for demonstration purposes.
"""

import random
import string

# Every time the app restarts this list will be wiped.  Use a real database
# in a real app.  This also is not thread safe.
users = [

]

def get_random_string(length=11):
    alphabet = string.ascii_lowercase
    random_str = ''.join(random.choice(alphabet) for i in range(length))
    return random_str

def insert_user(username, password):
    user = {
        'id': get_random_string(),
        'username': username,
        'password': password
    }
    users.append(user)

def get_user(user_name=None, user_id=None):
    for user in users:
        if user['username'] == user_name or user['id'] == user_id:
            return user
    return None
