from string import digits, ascii_lowercase
from random import choice
from http import HTTPStatus

from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import UserModel


def generate_random_string():
    letters = ascii_lowercase + digits
    return ''.join(choice(letters) for i in range(8))


class Auth(Resource):
    """API Resource for getting a new mail address."""
    def post(self):
        # Replace abcxyz.com with appropriate host
        new_address = generate_random_string() + '@abcxyz.com'
        while UserModel.find_by_address(new_address) is not None:
            # There is already an account with this address
            new_address = generate_random_string() + '@abcxyz.com'
        token = create_access_token(identity=new_address)
        new_user = UserModel(new_address, token)
        new_user.save_to_db()
        return {
            'account': new_user.json(),
            'status': HTTPStatus.CREATED
        }
