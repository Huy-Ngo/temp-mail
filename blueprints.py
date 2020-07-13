from flask import Blueprint, flash, request, render_template, redirect, url_for
from test_server.client import new_address, send_mail, receive_mail

bp = Blueprint('gui', __name__, url_prefix='')


@bp.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        address, token = new_address()
        return redirect(url_for('.mailbox', address=address, token=token))
    return render_template('views/auth.html')


@bp.route('/<address>/<token>')
def mailbox(address, token):
    all_mails = receive_mail(token)
    if 'mails' not in all_mails:
        return render_template('views/error.html', message=all_mails['message'])
    return render_template('views/mailbox.html', address=address, token=token, mails=all_mails['mails'])


@bp.route('/<address>/<token>/<int:_id>')
def mail(address, token, _id):
    all_mails = receive_mail(token)
    if 'mails' not in all_mails:
        return render_template('views/error.html', message=all_mails['message'])
    for email in all_mails['mails']:
        if email['id'] == _id and email['recipient'] == address:
            return render_template('views/mail.html', mail=email, address=address, token=token)
