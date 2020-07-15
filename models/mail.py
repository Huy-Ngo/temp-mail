from db import db


class MailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(254))
    recipient = db.Column(db.String(254), db.ForeignKey('user_model.email_address'), nullable=False)

    # headers
    mail_from = db.Column(db.String(300))
    rcpt_to = db.Column(db.String(300))
    date = db.Column(db.DateTime)
    subject = db.Column(db.String(150))

    # payload
    text = db.Column(db.String)
    html = db.Column(db.String)

    # status check
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, sender, recipient, mail_from, rcpt_to, date, subject, text, html):
        self.sender = sender
        self.recipient = recipient
        self.mail_from = mail_from
        self.rcpt_to = rcpt_to
        self.date = date
        self.subject = subject
        self.text = text
        self.html = html
        self.is_read = False

    def json(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'headers': {
                'from': self.mail_from,
                'to': self.rcpt_to,
                'date': self.date.__str__(),
                'subject': self.subject
            },
            'payload': {
                'text': self.text,
                'html': self.html
            },
            'is_read': self.is_read
        }

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_address(cls, address):
        return cls.query.filter_by(recipient=address).all()

    @classmethod
    def fetch_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_read(self):
        """Set the email as read."""
        self.is_read = True
        db.session.add(self)
        db.session.commit()
