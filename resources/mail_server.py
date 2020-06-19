from smtpd import SMTPServer

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
