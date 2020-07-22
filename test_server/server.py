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


def parse_payload_tree(mime_data):
    """Take a MIME data package and return a dict of terminal payloads.

    For now, the payloads returned are only text/plain and text/html.
    """
    flat_data = {}
    if 'text/plain' in mime_data['content-type']:
        flat_data['text/plain'] = mime_data.get_payload()
    elif 'text/html' in mime_data['content-type']:
        flat_data['text/html'] = mime_data.get_payload()
    elif 'multipart' in mime_data['content-type']:
        payload_list = mime_data.get_payload()
        for payload in payload_list:
            flat_data.update(parse_payload_tree(payload))
    return flat_data


def send_request(mailfrom, rcpttos, mime_data):
    if type(mime_data) == bytes:
        mime_data = mime_data.decode()
    mime_data = Parser(policy=default).parsestr(mime_data)
    parsed_data = parse_payload_tree(mime_data)
    print(parsed_data)
    text = parsed_data['text/plain']
    html = parsed_data['text/html']
    html = decodestring(html).decode()
    requests.post(url, {
            'sender': mailfrom,
            'recipient': rcpttos[0],
            'mail_from': mime_data['from'],
            'rcpt_to': mime_data['to'],
            'date': mime_data['date'],
            'subject': mime_data['subject'],
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
