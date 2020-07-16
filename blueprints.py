from requests import get, post
from json import load, dumps

from flask import Blueprint, flash, request, render_template, redirect, url_for
from test_server.client import new_address
from flask_jwt_extended import set_access_cookies, get_raw_jwt, jwt_required, get_jti

bp = Blueprint('gui', __name__, url_prefix='/')
with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    env = data['ENV']
    host = data['HOST']


@bp.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        address, token = new_address()
        response = redirect(url_for('.mailbox', address=address))
        set_access_cookies(response, token)
        return response
    return render_template('views/auth.html')


@bp.route('/<address>')
def mailbox(address):
    token = request.cookies.get('access_token_cookie')
    all_mails = get(f'http://{host_port}/api/mail/',
                    headers={'Authorization': f'Bearer {token}'}).json()
    if 'mails' not in all_mails:
        return render_template('views/error.html', message=all_mails['msg'])
    mails = all_mails['mails']
    mails = sorted(mails, reverse=True, key=lambda m: m['id'])
    return render_template('views/mailbox.html', address=address, mails=mails)


@bp.route('/<address>/<int:_id>')
def mail(address, _id):
    token = request.cookies.get('access_token_cookie')
    email = get(f'http://{host_port}/api/mail/{_id}',
                headers={'Authorization': f'Bearer {token}'}).json()
    return render_template('views/mail.html', mail=email['mail'], address=address)
