from db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(254))
    token = db.Column(db.String(256))
    is_expired = db.Column(db.Boolean)

    def __init__(self, email_address, token):
        self.email_address = email_address
        self.token = token
        self.is_expired = False

    def json(self):
        return {'id': self.id,
                'email_address': self.email_address,
                'token': self.token,
                'is_expired': self.is_expired}

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
