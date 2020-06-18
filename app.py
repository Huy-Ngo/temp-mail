from asyncore import loop

from flask import Flask
from flask_restful import Api

from db import db
from resources import TempMailServer, MailStorage

app = Flask(__name__)
app.config.from_json('config.json')

api = Api(app)

server = TempMailServer(('127.0.0.1', 1025), None)
loop()

api.add_resource(MailStorage, '/mail/')


@app.before_first_request
def create_database():
    db.create_all()


if __name__ == '__main__':
    app.run()
