import smtpd
import asyncore
import requests
from threading import Thread

url = 'http://127.0.0.1:5000/mail/'


def send_request(mailfrom, rcpttos, data):
    requests.post(url, {
            'sender': mailfrom,
            'recipient': rcpttos[0],
            'message': data
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
