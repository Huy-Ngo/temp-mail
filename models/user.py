from datetime import datetime, timedelta

from db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(254))
    token = db.Column(db.String(256))
    is_expired = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, email_address, token):
        self.email_address = email_address
        self.token = token
        self.is_expired = False

    def json(self):
        return {
            'id': self.id,
            'email_address': self.email_address,
            'token': self.token,
            'is_expired': self.is_expired,
            'create_at': self.create_at.__str__()
        }

    @classmethod
    def find_by_address(cls, address):
        return cls.query.filter_by(email_address=address).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    def check_validity(self):
        """Check if the token is still valid.

        :return: `True` if it is still valid
        `False` if it has expired."""
        expiration_time = self.create_at + timedelta(minutes=15)
        current_time = datetime.utcnow()
        is_valid = expiration_time > current_time
        self.is_expired = not is_valid
        db.session.add(self)
        db.session.commit()
        return is_valid

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
