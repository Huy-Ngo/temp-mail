from sqlalchemy import Column, Integer, String
from db import Base


class MailModel(Base):
    id = Column(Integer, primary_key=True)
    sender = Column(String(254))
    recipient = Column(String(254))
    message = Column(String)

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
        session.add(self)
        session.commit()
