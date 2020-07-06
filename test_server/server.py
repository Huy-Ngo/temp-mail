import smtpd
import asyncore
import requests
from threading import Thread

from email.parser import Parser, BytesParser
from email.policy import default

url = 'http://127.0.0.1:5000/mail/'


def send_request(mailfrom, rcpttos, data):
    if type(data) == bytes:
        data = data.decode()
    headers = Parser(policy=default).parsestr(data)
    content = headers.get_payload()
    print('DEBUG:', content)
    if type(content) == list:
        text = content[0].get_payload()
        html = content[1].get_payload()
        print('DEBUG:', text, 'END DEBUG')
    else:
        text = content
        html = ''
    print(headers)
    requests.post(url, {
            'sender': mailfrom,
            'recipient': rcpttos[0],
            'mail_from': headers['from'],
            'rcpt_to': headers['to'],
            'date': headers['date'],
            'subject': headers['subject'],
            'text': text,
            'html': html
        })


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        api_thread = Thread(target=send_request,
                            args=(mailfrom, rcpttos, data,))
        api_thread.start()
        api_thread.join()
        return


server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
