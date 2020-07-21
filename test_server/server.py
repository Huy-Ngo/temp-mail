import smtpd
import asyncore
import requests
from threading import Thread
from json import load

from quopri import decodestring

from email.parser import Parser
from email.policy import default

with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    host = data['HOST']

url = f'http://{host_port}/api/mail/'


def send_request(mailfrom, rcpttos, data):
    if type(data) == bytes:
        data = data.decode()
    headers = Parser(policy=default).parsestr(data)
    content = headers.get_payload()
    text = ''
    html = ''
    if type(content) == list:
        for part in content:
            if part['content-type'] == 'text/plain':
                text = part.get_payload()
            elif part['content-type'] == 'text/html':
                html = part.get_payload()
        html = decodestring(html).decode()
    else:
        text = content
        html = ''
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


server = CustomSMTPServer((host, 1025), None)

asyncore.loop()
