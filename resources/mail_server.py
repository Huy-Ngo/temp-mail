from smtpd import SMTPServer
from http import HTTPStatus

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import MailModel


class TempMailServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', len(data))
        for rcpt in rcpttos:
            message = MailModel(mailfrom, rcpt, data)
            message.save_to_db()
        all_mails = MailModel.fetch_all()
        print(*[mail.json() for mail in all_mails], sep='\n')


class Mailbox(Resource):
    @jwt_required
    def get(self):
        """Retrieve all mails from the mail box."""
        address = get_jwt_identity()
        mails = MailModel.fetch_by_address(address)
        if len(address) == 0:
            return {
                'message': 'No mails found.',
                'status': HTTPStatus.NOT_FOUND
            }
        return {
            'mails': [mail.json() for mail in mails],
            'status': HTTPStatus.OK
        }


class Mail(Resource):
    @jwt_required
    def get(self, _id):
        """Display content of a mail."""
        mail = MailModel.fetch_by_id(_id)
        if mail is None:
            return {
                'message': f'No mail with id {_id} found',
                'status': HTTPStatus.NOT_FOUND
            }
        return {
            'mail': mail,
            'status': HTTPStatus.OK
        }
