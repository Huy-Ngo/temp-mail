#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from string import digits, ascii_lowercase
from random import choice
from http import HTTPStatus
from json import load

from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import UserModel

with open('config.json', 'r') as f:
    data = load(f)
    host = data['HOST']


def generate_random_string():
    """Create a random string with 8 letters for users."""
    letters = ascii_lowercase + digits
    return ''.join(choice(letters) for i in range(8))


class Auth(Resource):
    """API Resource for getting a new mail address."""
    def post(self, address=None):
        """Create a new email address"""
        if address is None:
            address = f'{generate_random_string()}@{host}'
            while UserModel.find_by_address(address) is not None:
                address = f'{generate_random_string()}@{host}'
        else:
            if UserModel.find_by_address(address) is not None:
                return {
                    'message': 'Failed to create an email address'
                }, HTTPStatus.BAD_REQUEST
        token = create_access_token(identity=address)
        new_user = UserModel(address, token)
        new_user.save_to_db()
        return {
            'account': new_user.json(),
            'message': 'A temporary mail created'
        }, HTTPStatus.CREATED
