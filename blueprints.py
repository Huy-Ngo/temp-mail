from requests import get, post
from json import load, dumps

from flask import Blueprint, flash, request, render_template, redirect, url_for
from test_server.client import new_address

bp = Blueprint('gui', __name__, url_prefix='')

with open('config.json', 'r') as f:
    data = load(f)
    host_port = data['HOST_PORT']
    env = data['ENV']
    host = data['HOST']


@bp.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        address, token = new_address()
        return redirect(url_for('.mailbox', address=address, token=token))
    return render_template('views/auth.html')


@bp.route('/<address>/<token>')
def mailbox(address, token):
    all_mails = get(f'http://{host_port}/mail/',
                    headers={'Authorization': f'Bearer {token}'}).json()
    if 'mails' not in all_mails:
        return render_template('views/error.html', message=all_mails['msg'])
    mails = all_mails['mails']
    mails = sorted(mails, reverse=True, key=lambda m: m['id'])
    return render_template('views/mailbox.html', address=address, token=token, mails=mails)


@bp.route('/<address>/<token>/<int:_id>')
def mail(address, token, _id):
    email = get(f'http://{host_port}/mail/{_id}',
                headers={'Authorization': f'Bearer {token}'}).json()
    print(dumps(email, indent=2))
    return render_template('views/mail.html', mail=email['mail'], address=address, token=token)
