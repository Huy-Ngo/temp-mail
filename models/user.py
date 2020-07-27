#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from datetime import datetime, timedelta

from db import db


class UserModel(db.Model):
    """Model for representing and storing addresses."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(254))
    access_token = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))
    is_expired = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    mails = db.relationship('MailModel', backref='user', lazy=True)

    def __init__(self, email_address: str, access_token: str, refresh_token: str):
        self.email_address = email_address
        self.access_token = access_token
        self.is_expired = False
        self.refresh_token = refresh_token

    def json(self):
        """Return the information of the object as a JSON"""
        return {
            'id': self.id,
            'email_address': self.email_address,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'is_expired': self.is_expired,
            'create_at': self.create_at.__str__()
        }

    @classmethod
    def find_by_address(cls, address: str):
        """Find the object representing the address."""
        return cls.query.filter_by(email_address=address).first()

    def check_validity(self):
        """Check if the access_token is still valid.

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
        """Save the email address to database."""
        db.session.add(self)
        db.session.commit()
