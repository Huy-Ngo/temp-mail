#  Copyright (c) 2020  Ngô Ngọc Đức Huy

import smtpd
import asyncore
import requests
from threading import Thread
from json import load
from typing import Dict, List

from quopri import decodestring

from email.message import Message
from email.parser import Parser
from email.policy import default

with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    host = data['HOST']
    env = data['ENV']

url = f'http://{host_port}/api/mail/'


def parse_payload_tree(mime_data: Message):
    """Take a MIME data package and return a dict of terminal payloads.

    For now, the payloads returned are only text/plain and text/html.
    """
    flat_data = {}
    if 'text/plain' in mime_data['content-type']:
        flat_data['text/plain'] = mime_data.get_payload(decode=True)
    elif 'text/html' in mime_data['content-type']:
        flat_data['text/html'] = mime_data.get_payload(decode=True)
    elif 'image' in mime_data['content-type']:
        cid = mime_data['content-id']
        cid = cid[1:-1]
        image_data = mime_data.get_payload()
        if 'images' not in flat_data:
            flat_data['images'] = {}
        flat_data['images'][cid] = image_data
    elif 'multipart' in mime_data['content-type']:
        payload_list = mime_data.get_payload()
        for payload in payload_list:
            flat_data.update(parse_payload_tree(payload))
    return flat_data


def replace_image(html: str, images: Dict[str, str]):
    """Take a HTML code that uses CID and replace it
    with the base64 encoded image."""
    for cid in images:
        image_data = images[cid]
        html = html.replace(f'cid:{cid}',
                            f'data:image/jpeg;base64,{image_data}')
    return html


def deliver_mail(mailfrom: str, rcpttos: List[str], mime_data):
    """Send a request to save received emails to the database."""
    if type(mime_data) == bytes:
        mime_data = mime_data.decode()
    mime_data = Parser(policy=default).parsestr(mime_data)
    parsed_data = parse_payload_tree(mime_data)
    text = (parsed_data['text/plain']
            if 'text/plain' in parsed_data
            else 'Plain text not available')
    html = (decodestring(parsed_data['text/html']).decode()
            if 'text/html' in parsed_data
            else 'HTML not available')
    if 'images' in parsed_data:
        html = replace_image(html, parsed_data['images'])
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
        api_thread = Thread(target=deliver_mail,
                            args=(mailfrom, rcpttos, data,))
        api_thread.start()
        api_thread.join()
        return


if __name__ == '__main__':
    port = 1025 if env == 'development' else 25
    server = CustomSMTPServer((host, port), None)

    asyncore.loop()
