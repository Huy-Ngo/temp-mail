#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from http import HTTPStatus
from email.utils import parsedate_to_datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models import UserModel, MailModel


class Mailbox(Resource):
    """API resources for listing mails."""
    parser = RequestParser()
    parser.add_argument('sender', help='The address of the sender.')
    parser.add_argument('recipient', help='The address that receives this email.')
    parser.add_argument('mail_from', help='Header: The person who sends this.')
    parser.add_argument('rcpt_to', help='Header: The persons who receive this.')
    parser.add_argument('date', help='Header: The date and time this was sent.')
    parser.add_argument('subject', help='Header: The subject of the email.')
    parser.add_argument('text', help='Payload in text format.')
    parser.add_argument('html', help='Payload in HTML format.')

    @jwt_required
    def get(self):
        """Retrieve all mails from the mail box."""
        address = get_jwt_identity()
        if address is None:
            return {
                'message': 'The mail account does not exists or has expired.'
            }, HTTPStatus.BAD_REQUEST
        if not UserModel.find_by_address(address).check_validity():
            return {
                'message': 'Your token has expired',
                'email_address': address
            }, HTTPStatus.UNAUTHORIZED
        mails = MailModel.fetch_by_address(address)
        if len(address) == 0:
            return {
                'message': 'No mails found.',
            }, HTTPStatus.NOT_FOUND
        return {
            'mails': [mail.json() for mail in mails],
            'address': address,
            'message': 'OK'
        }, HTTPStatus.OK

    def post(self):
        """Receive an email and save it to database."""
        data = Mailbox.parser.parse_args()
        data['date'] = parsedate_to_datetime(data['date'])
        mail = MailModel(**data)
        mail.save_to_db()
        return {
            'message': 'Delivered mail successfully',
            'mail': mail.json()
        }, HTTPStatus.CREATED


class Mail(Resource):
    """API resources for mail details."""
    @jwt_required
    def get(self, _id):
        """Return content of a mail."""
        mail = MailModel.fetch_by_id(_id)
        address = get_jwt_identity()
        if mail is None:
            return {
                'message': f'No mail with id {_id} found'
            }, HTTPStatus.NOT_FOUND
        recipient = mail.json()['recipient']
        if recipient != address:
            return {
                'message': 'You are unauthorized to read this message.'
            }, HTTPStatus.UNAUTHORIZED
        mail.set_read()

        return {
           'mail': mail.json(),
           'address': address,
           'message': 'OK'
        }, HTTPStatus.OK
