from http import HTTPStatus
from email.parser import Parser
from email.policy import default

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models import UserModel, MailModel


class Mailbox(Resource):
    parser = RequestParser()
    parser.add_argument('sender', help='The address of the sender.')
    parser.add_argument('recipient', help='The address that receives this email.')
    parser.add_argument('message', help='The content of the mail.')

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
        return {'mails': [mail.json() for mail in mails]}, HTTPStatus.OK

    def post(self):
        """Receive an email and save it to database."""
        data = Mailbox.parser.parse_args()
        headers = Parser(policy=default).parsestr(data['message'])
        mail_from = headers['from']
        rcpt_to = headers['to']
        date = headers['date']
        subject = headers['subject']
        text = headers.get_payload(0).get_payload()
        html = headers.get_payload(1).get_payload()
        mail = MailModel(sender=data['sender'],
                         recipient=data['recipient'],
                         mail_from=mail_from,
                         rcpt_to=rcpt_to,
                         date=date, subject=subject,
                         text=text, html=html)
        mail.save_to_db()
        return {
            'message': 'Delivered mail successfully',
            'mail': mail.json()
        }, HTTPStatus.CREATED


class Mail(Resource):
    @jwt_required
    def get(self, _id):
        """Display content of a mail."""
        mail = MailModel.fetch_by_id(_id)
        user = get_jwt_identity()
        if mail is None:
            return {
                'message': f'No mail with id {_id} found'
            }, HTTPStatus.NOT_FOUND
        recipient = mail.json()['recipient']
        if recipient != user:
            return {
                'message': 'You are unauthorized to read this message.'
            }, HTTPStatus.UNAUTHORIZED
        return {'mail': mail.json()}, HTTPStatus.OK
