import smtplib
from email.utils import format_datetime, localtime
from email.message import EmailMessage
import requests
from json import dump, load, dumps
from sys import argv


def new_address():
    # Get a new email
    r = requests.post('http://127.0.0.1:5000/auth/')

    data = r.json()
    print(data)
    address = data['account']['email_address']
    token = data['account']['token']
    print(address)
    print(token)
    with open('token.json', 'w') as f:
        dump({'email_address': address, 'token': token}, f)
    return address, token


def send_mail(recipient, subject='Simple test message', message='This is the body of the message.'):
    # Create the message
    msg = EmailMessage()
    msg['content-type'] = 'text/plain'
    msg.set_content(message)
    html = message.split('\n')
    html = [f'<div>{line}</div>' for line in html]
    html = ''.join(html)

    html_msg = EmailMessage()
    html_msg['content-type'] = 'text/html'
    html_msg.set_content(html)

    envelope = EmailMessage()
    envelope['content-type'] = 'multipart/alternative'
    envelope['from'] = 'Foo Bar <foo@bar.com>'
    envelope['to'] = recipient
    envelope['date'] = format_datetime(localtime())
    envelope['subject'] = subject
    envelope.set_payload([msg, html_msg])

    server = smtplib.SMTP('127.0.0.1', 1025)
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('author@example.com',
                        [recipient],
                        envelope.as_string())
    finally:
        server.quit()


def receive_mail(token):
    r = requests.get('http://127.0.0.1:5000/mail/',
                     headers={'Authorization': f'Bearer {token}'})
    return r.json()


if __name__ == '__main__':
    cmd = argv[1]
    if cmd == 'new':
        new_address()
    elif cmd == 'send':
        with open('token.json', 'r') as f:
            receiver = load(f)['email_address']
        send_mail(receiver)
    elif cmd == 'read':
        with open('token.json', 'r') as f:
            tok = load(f)['token']
        mails = receive_mail(tok)
        print(dumps(mails, indent=2))
    else:
        print('Invalid option')
