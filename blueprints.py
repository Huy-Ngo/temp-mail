#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from requests import get, post
from json import load, dumps
from time import sleep

from flask import Blueprint, Response, request, render_template, redirect, url_for
from flask_jwt_extended import set_access_cookies

bp = Blueprint('gui', __name__, url_prefix='/')
with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    env = data['ENV']
    host = data['HOST']


def fetch_mail(token):
    """Send GET request to the API server."""
    all_mails = get(f'http://{host_port}/api/mail/',
                    headers={'Authorization': f'Bearer {token}'}).json()
    if 'mails' not in all_mails or 'address' not in all_mails:
        message = all_mails['message']
        if message == 'Token has expired':
            message = 'Your email has expired. Please make a new one.'
        return False, message
    else:
        return True, all_mails


def stream_mail(token):
    sleep(5)
    success, response = fetch_mail(token)
    if not success:
        return render_template('views/error.html', message=response)
    return dumps(response['mails'])


@bp.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        account_info = post(f'http://{host_port}/api/auth/').json()

        token = account_info['account']['token']
        response = redirect(url_for('.mailbox'))
        set_access_cookies(response, token)
        return response
    return render_template('views/auth.html')


@bp.route('/mail')
def mailbox():
    token = request.cookies.get('access_token_cookie')
    success, response = fetch_mail(token)
    if not success:
        return render_template('views/error.html', message=response)
    mails = response['mails']
    address = response['address']
    mails = sorted(mails, reverse=True, key=lambda m: m['id'])
    return render_template('views/mailbox.html', address=address, mails=mails)


@bp.route('/mail/stream')
def mail_stream():
    token = request.cookies.get('access_token_cookie')

    def event_stream():
        while True:
            yield f'data: {stream_mail(token)}\n\n'

    return Response(event_stream(), mimetype="text/event-stream")


@bp.route('/mail/<int:_id>')
def mail(_id):
    token = request.cookies.get('access_token_cookie')
    email = get(f'http://{host_port}/api/mail/{_id}',
                headers={'Authorization': f'Bearer {token}'}).json()
    if 'mail' not in email or 'address' not in email:
        message = email['message']
        if message == 'Token has expired':
            message = 'Your email has expired. Please make a new one.'
        return render_template('views/error.html', message=message)
    return render_template('views/mail.html', mail=email['mail'], address=email['address'])
