from db import db


class MailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(254))
    recipient = db.Column(db.String(254))
    message = db.Column(db.String)

    def __init__(self, sender, recipient, message):
        self.sender = sender
        self.recipient = recipient
        self.message = message

    def json(self):
        return {'id': self.id,
                'sender': self.sender,
                'recipient': self.recipient,
                'message': self.message}

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
