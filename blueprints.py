from flask import Blueprint, flash, request, render_template, redirect, url_for
from test_server.client import new_address, send_mail, receive_mail

bp = Blueprint('gui', __name__, url_prefix='/gui')


@bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        address, token = new_address()
        return redirect(url_for('.mailbox', address=address, token=token))
    return render_template('views/auth.html')


@bp.route('/mail/<address>/<token>')
def mailbox(address, token):
    url_for('mailbox', address=address, token=token)
    all_mails = receive_mail(token)
    return render_template('views/mailbox.html', address=address, mails=all_mails['mails'])


@bp.route('/mail/<address>/<token>/<int:_id>')
def mail(address, token, _id):
    all_mails = receive_mail(token)['mails']
    for email in all_mails:
        if email['id'] == _id and email['recipient'] == address:
            return render_template('views/mail.html', mail=email)
    flash('Invalid mail ID or unauthorized')


@bp.route('/send', methods=['GET', 'POST'])
def send_view():
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        message = request.form['message']
        send_mail(recipient, subject, message)
    return render_template('views/send_mail.html')
