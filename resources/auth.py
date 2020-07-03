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
    def get(self):
        """Fetch the list of the emails.

        This is for testing and debugging purpose only.
        """
        mails = UserModel.fetch_all()
        for mail in mails:
            mail.check_validity()
        return {
            'mails': [mail.json() for mail in mails]
        }, HTTPStatus.OK

    def post(self):
        # Replace abcxyz.com with appropriate host
        new_address = generate_random_string() + '@103.56.158.148'
        while UserModel.find_by_address(new_address) is not None:
            # There is already an account with this address
            new_address = generate_random_string() + '@103.56.158.148'
        token = create_access_token(identity=new_address)
        new_user = UserModel(new_address, token)
        new_user.save_to_db()
        return {
            'account': new_user.json(),
        }, HTTPStatus.CREATED
