import smtplib
import email.utils
from email.mime.text import MIMEText
import requests

# Get a new email
r = requests.post('http://127.0.0.1:5000/auth/')

data = r.json()
print(data)
recipient = data['account']['email_address']
token = data['account']['token']
print(recipient)
print(token)

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient',
                                    recipient))
msg['From'] = email.utils.formataddr(('Author',
                                      'author@example.com'))
msg['Subject'] = 'Simple test message'

server = smtplib.SMTP('127.0.0.1', 1025)
server.set_debuglevel(True)  # show communication with the server
try:
    server.sendmail('author@example.com',
                    [recipient],
                    msg.as_string())
finally:
    server.quit()
