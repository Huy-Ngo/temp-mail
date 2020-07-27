#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from string import digits, ascii_lowercase
from random import choice
from http import HTTPStatus
from json import load

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)

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
        access_token = create_access_token(identity=address)
        refresh_token = create_refresh_token(identity=address)
        new_user = UserModel(address, access_token, refresh_token)
        new_user.save_to_db()
        return {
            'account': new_user.json(),
            'message': 'A temporary mail created'
        }, HTTPStatus.CREATED

    @jwt_refresh_token_required
    def put(self):
        """Update an email address, i.e. delay its expiration."""
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        user_object: UserModel = UserModel.find_by_address(current_user)
        user_object.refresh_tokens(access_token=new_access_token)
        user_object.save_to_db()
