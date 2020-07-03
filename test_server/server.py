import smtpd
import asyncore
import requests
from threading import Thread

url = 'http://103.56.158.148:5000/mail/'


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
        print('Message', data, sep='\n')
        api_thread = Thread(target=send_request,
                            args=(mailfrom, rcpttos, data,))
        api_thread.start()
        api_thread.join()
        return


server = CustomSMTPServer(('103.56.158.148', 25), None)

asyncore.loop()
