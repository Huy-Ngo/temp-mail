#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from string import digits, ascii_lowercase
from random import choice
from http import HTTPStatus
from json import load

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
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
    parser = RequestParser()
    parser.add_argument('address')

    def post(self):
        """Create a new email address"""
        args = Auth.parser.parse_args()
        address = args['address']
        if address is None:
            address = f'{generate_random_string()}@{host}'
            while UserModel.find_by_address(address) is not None:
                address = f'{generate_random_string()}@{host}'
        else:
            address = f'{address}@{host}'
            if UserModel.find_by_address(address) is not None:
                return {
                    'message': 'Email address has already been used.'
                }, HTTPStatus.BAD_REQUEST
        token = create_access_token(identity=address)
        new_user = UserModel(address, token)
        new_user.save_to_db()
        return {
            'account': new_user.json(),
            'message': 'A temporary mail created'
        }, HTTPStatus.CREATED
