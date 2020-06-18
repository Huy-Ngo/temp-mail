from string import digits, ascii_lowercase
from random import choice

from flask_restful import Resource

from models import UserModel


def generate_random_string():
    letters = ascii_lowercase + digits
    return ''.join(choice(letters) for i in range(8))


class Auth(Resource):
    """API Resource for getting a new mail address."""
    def post(self):
        # Replace abcxyz.com with appropriate host
        new_address = generate_random_string() + '@abcxyz.com'
        token = ''
        new_user = UserModel(new_address, token)
        new_user.save_to_db()
