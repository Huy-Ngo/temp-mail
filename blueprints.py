#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from requests import get, post, put
from json import load, dumps
from time import sleep
from http import HTTPStatus
from typing import Tuple

from flask import (Blueprint, Response, request,
                   render_template, redirect, url_for)
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, decode_token

bp = Blueprint('gui', __name__, url_prefix='/')
with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    env = data['ENV']
    host = data['HOST']


def set_tokens(access_token, refresh_token, response):
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    payload = decode_token(access_token)
    exp = payload['exp']
    response.set_cookie('exp', str(exp))
    return response


def refresh(refresh_token: str) -> Tuple[dict, int]:
    response = put(f'http://{host_port}/api/auth/',
                   headers={'Authorization': f'Bearer {refresh_token}'})
    return response.json(), response.status_code


def fetch_mail(token: str):
    """Send GET request to the API server to get mails or return error."""
    all_mails = get(f'http://{host_port}/api/mail/',
                    headers={'Authorization': f'Bearer {token}'}).json()
    if 'mails' not in all_mails or 'address' not in all_mails:
        message = all_mails['message']
        if message == 'Token has expired':
            message = 'Your email has expired. Please make a new one.'
        return False, message
    else:
        return True, all_mails


def stream_mail(token: str):
    """A function to stream mail into SSE stream."""
    sleep(5)
    success, response = fetch_mail(token)
    if not success:
        return render_template('views/error.html', message=response)
    return dumps(response['mails'])


@bp.route('/mail/stream')
def mail_sse_stream():
    """Route for SSE stream, serve for mailbox updating."""
    token = request.cookies.get('access_token_cookie')

    def event_stream():
        while True:
            yield f'data: {stream_mail(token)}\n\n'

    return Response(event_stream(), mimetype="text/event-stream")


@bp.route('/', methods=['GET', 'POST'])
def auth():
    """Route for home page, handling requests for new mail addresses."""
    if request.method == 'POST':
        address = request.form['address'] or None
        response = post(f'http://{host_port}/api/auth/',
                        data={'address': address})
        message = response.json()['message']
        if response.status_code == HTTPStatus.BAD_REQUEST:
            message += " A random email is generated instead."
            response = post(f'http://{host_port}/api/auth/')
        elif response.status_code != HTTPStatus.OK:
            render_template('views/error.html', message=message)
        account_info = response.json()
        access_token = account_info['account']['access_token']
        refresh_token = account_info['account']['refresh_token']
        response = redirect(url_for('.mailbox', message=message))
        response = set_tokens(access_token, refresh_token, response)
        return response
    return render_template('views/auth.html')


@bp.route('/mail', methods=['GET', 'POST'])
def mailbox():
    """Route for mailbox, render emails received to client."""
    access_token = request.cookies.get('access_token_cookie')
    refresh_token = request.cookies.get('refresh_token_cookie')
    if request.method == 'POST':
        response, status = refresh(refresh_token)
        if status != HTTPStatus.OK:
            return render_template('views/error.html',
                                   message='Refresh duration failed.')
        access_token = response['access_token']
        response = redirect(url_for('.mailbox', message=response['message']))
        response = set_tokens(access_token, refresh_token, response)
        return response
    success, response = fetch_mail(access_token)
    message = request.args.get('message')
    if not success:
        return render_template('views/error.html', message=response)
    mails = response['mails']
    address = response['address']
    mails = sorted(mails, reverse=True, key=lambda m: m['id'])
    return render_template('views/mailbox.html',
                           address=address, mails=mails, message=message)


@bp.route('/mail/<int:_id>', methods=['GET', 'POSt'])
def mail(_id: int):
    """Route for specific mail with id."""
    access_token = request.cookies.get('access_token_cookie')
    refresh_token = request.cookies.get('refresh_token_cookie')
    if request.method == 'POST':
        response, status = refresh(refresh_token)
        if status != HTTPStatus.OK:
            return render_template('views/error.html',
                                   message='Refresh duration failed.')
        access_token = response['access_token']
        response = redirect(url_for('.mailbox', message=response['message']))
        response = set_tokens(access_token, refresh_token, response)
        return response
    email = get(f'http://{host_port}/api/mail/{_id}',
                headers={'Authorization': f'Bearer {access_token}'}).json()
    if 'mail' not in email or 'address' not in email:
        message = email['message']
        if message == 'Token has expired':
            message = 'Your email has expired. Please make a new one.'
        return render_template('views/error.html', message=message)
    return render_template('views/mail.html',
                           mail=email['mail'],
                           address=email['address'])
